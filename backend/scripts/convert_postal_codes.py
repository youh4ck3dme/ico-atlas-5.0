"""
Skript na konverziu Excel súborov s PSČ na CSV formát pre RegionResolver.
Spracováva OBCE.xlsx, ULICE.xlsx a POBoxy.xlsx z PSC-2025.
"""

import os
import sys
from pathlib import Path

import pandas as pd

# Pridaj backend do path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Mapping kódov krajov na názvy (podľa skutočných kódov v OBCE.xlsx)
KRAJ_CODES = {
    "BC": "Banskobystrický",
    "BL": "Bratislavský",  # BL nie BA!
    "KI": "Košický",  # KI nie KE!
    "NI": "Nitriansky",  # NI nie NR!
    "PV": "Prešovský",
    "TA": "Trnavský",
    "TC": "Trenčiansky",
    "ZI": "Žilinský",  # ZI nie ZA!
}

# Cesty k súborom
PSC_2025_DIR = Path("/Users/youh4ck3dme/Downloads/PSC-2025")
OUTPUT_CSV = Path(__file__).parent.parent / "data" / "postal_codes_sk.csv"


def normalize_postal_code(psc: str) -> str:
    """Normalizuje PSČ: odstráni medzery a formátuje na 5 číslic."""
    if pd.isna(psc):
        return ""
    psc_str = str(psc).strip().replace(" ", "")
    # Zajisti, že má 5 číslic
    if len(psc_str) == 4:
        psc_str = "0" + psc_str
    return psc_str


def get_kraj_name(kraj_code: str) -> str:
    """Konvertuje kód kraja na názov."""
    if pd.isna(kraj_code):
        return ""
    kraj_code = str(kraj_code).strip().upper()
    return KRAJ_CODES.get(kraj_code, "")


def process_obce() -> pd.DataFrame:
    """Spracuje OBCE.xlsx a vráti DataFrame s PSČ, kraj, okres."""
    print("📖 Načítavam OBCE.xlsx...")
    df = pd.read_excel(PSC_2025_DIR / "OBCE.xlsx")

    # Vyber relevantné stĺpce
    df = df[["PSC", "KRAJ", "OKRES"]].copy()

    # Normalizuj PSČ
    df["postal_code"] = df["PSC"].apply(normalize_postal_code)

    # Konvertuj kód kraja na názov
    df["kraj"] = df["KRAJ"].apply(get_kraj_name)

    # Normalizuj okres (odstráni prázdne hodnoty)
    df["okres"] = df["OKRES"].astype(str).str.strip()

    # Filtruj prázdne hodnoty
    df = df[
        (df["postal_code"] != "")
        & (df["kraj"] != "")
        & (df["okres"] != "")
        & (df["okres"] != "nan")
    ].copy()

    # Vyber len potrebné stĺpce
    result = df[["postal_code", "kraj", "okres"]].copy()

    print(f"  ✅ Načítaných {len(result)} záznamov z OBCE.xlsx")
    return result


def process_ulice() -> pd.DataFrame:
    """Spracuje ULICE.xlsx a vráti DataFrame s PSČ (potrebuje lookup z OBCE pre kraj/okres)."""
    print("📖 Načítavam ULICE.xlsx...")
    df = pd.read_excel(PSC_2025_DIR / "ULICE.xlsx")

    # Načítaj OBCE pre lookup (podľa PSČ a podľa názvu obce)
    obce_df = pd.read_excel(PSC_2025_DIR / "OBCE.xlsx")
    
    # Lookup podľa PSČ (pre PSČ, ktoré majú hodnotu v OBCE)
    obce_psc_lookup = obce_df[obce_df["PSC"].notna()].drop_duplicates(subset=["PSC"], keep="first")
    obce_psc_dict = obce_psc_lookup.set_index("PSC")[["KRAJ", "OKRES"]].to_dict("index")
    
    # Lookup podľa názvu obce (pre Bratislavu a iné mestá, kde PSC môže byť NaN)
    obce_name_lookup = obce_df[obce_df["OBEC"].notna()].drop_duplicates(subset=["OBEC"], keep="first")
    obce_name_dict = obce_name_lookup.set_index("OBEC")[["KRAJ", "OKRES"]].to_dict("index")

    # Normalizuj PSČ
    df["postal_code"] = df["PSC"].apply(normalize_postal_code)

    # Lookup kraj a okres z OBCE (najprv podľa PSČ, potom podľa názvu obce, potom špeciálne pravidlá)
    def get_kraj_okres(row):
        psc_original = row["PSC"]
        obec_name = row.get("OBCE", "")
        
        # Skús lookup podľa PSČ
        if pd.notna(psc_original):
            psc_key = str(psc_original).strip()
            if psc_key in obce_psc_dict:
                kraj_code = obce_psc_dict[psc_key]["KRAJ"]
                okres = obce_psc_dict[psc_key]["OKRES"]
                return get_kraj_name(kraj_code), str(okres).strip()
        
        # Skús lookup podľa názvu obce (presný match)
        if pd.notna(obec_name):
            obec_key = str(obec_name).strip()
            if obec_key in obce_name_dict:
                kraj_code = obce_name_dict[obec_key]["KRAJ"]
                okres = obce_name_dict[obec_key]["OKRES"]
                return get_kraj_name(kraj_code), str(okres).strip()
        
        # Špeciálne pravidlá pre Bratislavu (PSČ prefix → okres)
        if pd.notna(psc_original):
            psc_normalized = normalize_postal_code(psc_original)
            if psc_normalized.startswith("811"):
                return "Bratislavský", "Bratislava I"
            elif psc_normalized.startswith("821"):
                return "Bratislavský", "Bratislava II"
            elif psc_normalized.startswith("831"):
                return "Bratislavský", "Bratislava III"
            elif psc_normalized.startswith("841"):
                return "Bratislavský", "Bratislava IV"
            elif psc_normalized.startswith("851"):
                return "Bratislavský", "Bratislava V"
        
        # Skús lookup podľa názvu obce (začína s)
        if pd.notna(obec_name):
            obec_key = str(obec_name).strip()
            for obec_name_key, value in obce_name_dict.items():
                if obec_name_key.startswith(obec_key) or obec_key.startswith(obec_name_key):
                    kraj_code = value["KRAJ"]
                    okres = value["OKRES"]
                    return get_kraj_name(kraj_code), str(okres).strip()
        
        return None, None

    df[["kraj", "okres"]] = df.apply(lambda x: pd.Series(get_kraj_okres(x)), axis=1)

    # Filtruj prázdne hodnoty
    df = df[
        (df["postal_code"] != "")
        & (df["kraj"].notna())
        & (df["kraj"] != "")
        & (df["okres"].notna())
        & (df["okres"] != "")
    ].copy()

    # Vyber len potrebné stĺpce
    result = df[["postal_code", "kraj", "okres"]].copy()

    print(f"  ✅ Načítaných {len(result)} záznamov z ULICE.xlsx")
    return result


def process_poboxy() -> pd.DataFrame:
    """Spracuje POBoxy.xlsx a vráti DataFrame s PSČ, kraj, okres."""
    print("📖 Načítavam POBoxy.xlsx...")
    df = pd.read_excel(PSC_2025_DIR / "POBoxy.xlsx")

    # Normalizuj PSČ
    df["postal_code"] = df["PSČ pre P.O.BOXy"].apply(normalize_postal_code)

    # Konvertuj kód kraja na názov
    df["kraj"] = df["Kraj"].apply(get_kraj_name)

    # Normalizuj okres
    df["okres"] = df["Okres"].astype(str).str.strip()

    # Filtruj prázdne hodnoty
    df = df[
        (df["postal_code"] != "")
        & (df["kraj"] != "")
        & (df["okres"] != "")
        & (df["okres"] != "nan")
    ].copy()

    # Vyber len potrebné stĺpce
    result = df[["postal_code", "kraj", "okres"]].copy()

    print(f"  ✅ Načítaných {len(result)} záznamov z POBoxy.xlsx")
    return result


def main():
    """Hlavná funkcia - spracuje všetky súbory a vytvorí CSV."""
    print("🚀 Konverzia PSČ súborov na CSV...")
    print("=" * 60)

    # Spracuj všetky súbory
    obce_df = process_obce()
    ulice_df = process_ulice()
    poboxy_df = process_poboxy()

    # Zkombinuj všetky DataFrames
    print("\n🔗 Kombinujem dáta...")
    combined = pd.concat([obce_df, ulice_df, poboxy_df], ignore_index=True)

    # Odstráň duplikáty (zachovaj prvý výskyt)
    print("🧹 Odstraňujem duplikáty...")
    before_count = len(combined)
    combined = combined.drop_duplicates(subset=["postal_code"], keep="first")
    after_count = len(combined)
    print(f"  ✅ Odstránených {before_count - after_count} duplikátov")

    # Zoraď podľa PSČ
    combined = combined.sort_values("postal_code").reset_index(drop=True)

    # Ulož do CSV
    print(f"\n💾 Ukladám do {OUTPUT_CSV}...")
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    combined.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")

    print("=" * 60)
    print(f"✅ Hotovo! Vytvorený CSV súbor s {len(combined)} jedinečnými PSČ")
    print(f"📁 Súbor: {OUTPUT_CSV}")
    print("\n📊 Štatistiky:")
    print(f"  • Celkový počet PSČ: {len(combined)}")
    print(f"  • Počet krajov: {combined['kraj'].nunique()}")
    print(f"  • Počet okresov: {combined['okres'].nunique()}")
    print("\n📋 Prvých 10 záznamov:")
    print(combined.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
