# Právny Rámec & Compliance

Tento dokument popisuje implementáciu právneho rámca a compliance opatrení v ILUMINATI SYSTEM.

## 1. Dokumenty na webe

### 1.1. Terms of Service (VOP)
**Cesta:** `/vop`  
**Súbor:** `frontend/src/pages/TermsOfService.jsx`

**Kľúčové prvky:**
- ✅ Vylúčenie zodpovednosti: "Poskytovateľ negarantuje správnosť dát, dáta majú len informatívny charakter"
- ✅ Fair Use Policy pre scraping externých zdrojov
- ✅ Zákaz scrapovania Platformy
- ✅ Zdrojovanie dát - vždy uvádzame zdroj

### 1.2. Privacy Policy (GDPR)
**Cesta:** `/privacy`  
**Súbor:** `frontend/src/pages/PrivacyPolicy.jsx`

**Kľúčové prvky:**
- ✅ Právny základ: Oprávnený záujem (Legitimate Interest) pre osoby v grafoch
- ✅ Právo na výmaz - detailný postup
- ✅ Doba uchovávania údajov
- ✅ Kontakt pre ochranu údajov

### 1.3. Disclaimer
**Cesta:** `/disclaimer`  
**Súbor:** `frontend/src/pages/Disclaimer.jsx`

**Komponent:** `frontend/src/components/Disclaimer.jsx`  
Zobrazuje sa pod grafmi, reportmi a analýzami.

## 2. Disclaimer Komponent

### 2.1. Použitie

```jsx
import Disclaimer from '../components/Disclaimer';

// Kompaktná verzia (pre malé grafy)
<Disclaimer compact={true} />

// Plná verzia (pre reporty)
<Disclaimer 
  sources={[
    { name: 'Obchodný register SR', url: 'https://www.orsr.sk' },
    { name: 'ARES (ČR)', url: 'https://wwwinfo.mfcr.cz' },
  ]}
  showFullText={true}
/>
```

### 2.2. Props

| Prop | Typ | Default | Popis |
|------|-----|---------|-------|
| `sources` | `Array<{name: string, url?: string}>` | `[]` | Zoznam zdrojov dát |
| `compact` | `boolean` | `false` | Kompaktná verzia (menšia) |
| `showFullText` | `boolean` | `false` | Zobraziť plný text disclaimeru |

### 2.3. Východzie zdroje

Ak nie sú poskytnuté vlastné zdroje, komponent automaticky zobrazí:
- Obchodný register SR (ORSR)
- Živnostenský register SR (ZRSR)
- Register účtovných závierok (RUZ)
- ARES (ČR)
- Finančná správa SR

## 3. Rizikový Manažment

### 3.1. Zdrojovanie Dát

**Pravidlo:** Vždy uvádzame zdroj dát pri zobrazení informácií.

**Implementácia:**
- Disclaimer komponent automaticky zobrazuje zdroje
- V Terms of Service je sekcia "Zdrojovanie Dát"
- Každý graf/report obsahuje Disclaimer s zdrojmi

**Hlavné zdroje:**
- **Slovensko:** ORSR, ZRSR, RUZ, Finančná správa SR
- **Česká republika:** ARES
- **Poľsko:** KRS
- **Maďarsko:** Cégközlöny

### 3.2. Fair Use Policy pre Scraping

**Pravidlá:**
- ✅ Nepreťažujeme štátne servery - používame rozumné rate limiting
- ✅ Používame rotujúce proxy a User-Agent hlavičky
- ✅ Respektujeme robots.txt a oficiálne API endpointy
- ✅ Cache mechanizmy znižujú počet požiadaviek
- ✅ Vždy uvádzame zdroj dát

**Implementácia v kóde:**
- `backend/services/sk_orsr_provider.py` - rate limiting
- `backend/services/sk_zrsr_provider.py` - retry mechanizmus
- `backend/services/sk_ruz_provider.py` - API prioritne, HTML fallback

## 4. GDPR Compliance

### 4.1. Právny Základ

**Pre registrovaných užívateľov:**
- Súhlas (Consent)
- Výkon zmluvy (Contract)

**Pre osoby v grafoch:**
- Oprávnený záujem (Legitimate Interest) - čl. 6(1)(f) GDPR
  - Prevencia podvodov
  - Due Diligence
  - Zvýšenie transparentnosti

### 4.2. Právo na Výmaz

**Postup:**
1. Pošlite e-mail na `privacy@crossbordernexus.com`
2. Predmet: "Žiadosť o výmaz údajov"
3. Uveďte: meno, dátum narodenia, IČO spoločnosti
4. Odozva do 30 dní
5. Výmaz do 7 dní po schválení

**Dôležité:**
- Výmaz z ILUMINATI SYSTEM nezabráni zobrazeniu v pôvodných registroch
- Pre úplné odstránenie kontaktujte príslušný obchodný register

### 4.3. Doba Uchovávania

- **Registrovaní užívatelia:** Počas trvania účtu + 3 roky po zrušení
- **Osoby v dátach:** Počas trvania zverejnenia v zdrojovom registri
- **Cache dát:** TTL 24 hodín

## 5. Implementácia v Aplikácii

### 5.1. Kde zobrazovať Disclaimer

**Povinné:**
- ✅ Analytics Dashboard (už implementované)
- ✅ Company Detail Reports
- ✅ Risk Score Reports
- ✅ PDF Exporty

**Odporúčané:**
- Search Results
- Graph Visualizations
- API Response Headers (pre Enterprise klientov)

### 5.2. Príklad použitia v nových komponentoch

```jsx
import Disclaimer from '../components/Disclaimer';

function MyReport() {
  return (
    <div>
      {/* Váš obsah */}
      <h2>Risk Analysis Report</h2>
      <Chart data={data} />
      
      {/* Disclaimer na konci */}
      <Disclaimer 
        sources={[
          { name: 'Obchodný register SR', url: 'https://www.orsr.sk' },
        ]}
        showFullText={true}
      />
    </div>
  );
}
```

## 6. Kontakty

**Právne otázky:**
- E-mail: `legal@crossbordernexus.com`

**Ochrana údajov:**
- E-mail: `privacy@crossbordernexus.com`

**Technická podpora:**
- E-mail: `support@crossbordernexus.com`

## 7. Aktualizácie

Tento dokument sa aktualizuje pri zmene právneho rámca alebo compliance požiadaviek.

**Posledná aktualizácia:** December 2024  
**Verzia:** 1.0

