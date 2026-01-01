# ORSR Data Template

## Príklad: IČO 57206236

**Zdroj:** https://www.orsr.sk

### Očakávané dáta z ORSR:

```json
{
  "ico": "57206236",
  "obchodne_meno": "BEKA COMPANY, s. r. o.",
  "sidlo": {
    "ulica": "Jedľová 5407/29",
    "mesto": "Poprad",
    "psc": "058 01"
  },
  "den_zapisu": "19.09.2025",
  "pravna_forma": "Spoločnosť s ručením obmedzeným",
  "oddiel": "Sro",
  "vlozka": "50653/P",
  "sud": "Okresný súd Prešov",
  
  "predmet_cinnosti": [
    "Vedenie účtovníctva",
    "Prípravné práce k realizácii stavby",
    "Dokončovacie stavebné práce pri realizácii exteriérov a interiérov",
    "Sprostredkovateľská činnosť v oblasti obchodu, služieb a výroby",
    "Kúpa tovaru na účely jeho predaja konečnému spotrebiteľovi",
    "Skladové, pomocné a prepravné služby v doprave",
    "Ubytovacie služby bez poskytovania pohostinských činností",
    "Vydavateľská činnosť, polygrafická výroba a knihárske práce",
    "Služby súvisiace s produkciou filmov, videozáznamov a zvukových nahrávok",
    "Počítačové služby a služby súvisiace s počítačovým spracovaním údajov",
    "Služby v oblasti administratívnej správy",
    "Prenájom nehnuteľností",
    "Prenájom, úschova a požičiavanie hnuteľných vecí",
    "Čistiace a upratovacie služby",
    "Činnosť podnikateľských, organizačných a ekonomických poradcov",
    "Reklamné, marketingové, fotografické a informačné služby",
    "Prevádzkovanie kultúrnych, spoločenských, zábavných, športových zariadení",
    "Organizovanie športových, kultúrnych a iných spoločenských podujatí",
    "Poskytovanie služieb osobného charakteru"
  ],
  
  "spolocnici": [
    {
      "meno": "Ing. Jozef Benko",
      "adresa": "Jedľová 5407/29, Poprad 058 01",
      "vklad": 2500,
      "mena": "EUR",
      "splatene": 2500,
      "od": "19.09.2025"
    },
    {
      "meno": "Marek Jakubčák",
      "adresa": "Rázusova 2672/21, Poprad 058 01",
      "vklad": 2500,
      "mena": "EUR",
      "splatene": 2500,
      "od": "19.12.2025"
    }
  ],
  
  "konatelia": [
    {
      "meno": "Ing. Jozef Benko",
      "adresa": "Jedľová 5407/29, Poprad 058 01",
      "vznik_funkcie": "19.09.2025"
    },
    {
      "meno": "Marek Jakubčák",
      "adresa": "Rázusova 2672/21, Poprad 058 01",
      "vznik_funkcie": "12.12.2025"
    }
  ],
  
  "konanie": "Konatelia konajú v mene spoločnosti samostatne.",
  
  "zakladne_imanie": {
    "vyska": 5000,
    "mena": "EUR",
    "splatene": 5000
  },
  
  "datum_aktualizacie": "18.12.2025"
}
```

### Mapovanie na Graph Format:

```json
{
  "nodes": [
    {
      "id": "company-57206236",
      "label": "BEKA COMPANY, s. r. o.",
      "type": "company",
      "country": "SK",
      "ico": "57206236",
      "dic": "",
      "founded": "19.09.2025",
      "legalForm": "Spoločnosť s ručením obmedzeným",
      "status": "Aktívna",
      "risk_score": 2,
      "virtual_seat": false
    },
    {
      "id": "address-57206236",
      "label": "Poprad",
      "type": "address",
      "details": "Jedľová 5407/29, 058 01 Poprad",
      "postalCode": "058 01",
      "virtual_seat": false
    },
    {
      "id": "person-jozef-benko",
      "label": "Ing. Jozef Benko",
      "type": "person",
      "details": "Konateľ, Spoločník (50%)"
    },
    {
      "id": "person-marek-jakubcak",
      "label": "Marek Jakubčák",
      "type": "person",
      "details": "Konateľ, Spoločník (50%)"
    }
  ],
  "edges": [
    { "source": "company-57206236", "target": "address-57206236", "type": "LOCATED_AT" },
    { "source": "company-57206236", "target": "person-jozef-benko", "type": "MANAGED_BY" },
    { "source": "company-57206236", "target": "person-jozef-benko", "type": "OWNED_BY" },
    { "source": "company-57206236", "target": "person-marek-jakubcak", "type": "MANAGED_BY" },
    { "source": "company-57206236", "target": "person-marek-jakubcak", "type": "OWNED_BY" }
  ]
}
```

### ORSR URL Pattern:
```
https://www.orsr.sk/hladaj_ico.asp?ICO={ICO}&SID=0
```
