# 🎨 ILUMINATI SYSTEM v5.0 - Design Prompt

## Prehľad
Kompletný redesign landing page pre ILUMINATE SYSTEM s novým korporátnym dizajnom v štýle "Slovak Enterprise Edition".

## Téma a Štýl

### Názov
**ILUMINATI SYSTEM v5.0 - SLOVAK ENTERPRISE EDITION**

### Farbová Paleta
- **Hlavná farba (Slovak Blue):** `#0B4EA2`
- **Akcent (Slovak Red):** `#EE1C25`
- **Pozadie:** `#F8FAFC` (slate-50)
- **Text:** `#1E293B` (slate-800)
- **Sekundárny text:** `#64748B` (slate-500)

### Typografia
- **Nadpisy:** `Playfair Display` (serif, bold)
- **Telo textu:** `Inter` (sans-serif)
- **Google Fonts:** 
  ```html
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
  ```

### Logo
- **Názov:** ILUMINATI (nie ILUMINATE)
- **Dizajn:** Trojuholník s okom (All-seeing eye)
  - Trojuholník: Slovak Blue (#0B4EA2)
  - Uzly: Slovak Red (#EE1C25)
  - Vnútorné oko: Slovak Blue

## Komponenty a Štruktúra

### 1. Navbar (Fixed Top)
```
- Výška: 80px (h-20)
- Pozadie: Biele (bg-white)
- Border: Spodný border (border-b border-slate-200)
- Shadow: Subtle (shadow-sm)
- Logo: Vľavo (IluminatiLogo + text)
- Menu: Vpravo (Desktop: Monitoring, Legislatíva, Cenník, Klientska zóna)
- Mobile: Hamburger menu
```

### 2. Hero Section
```
- Pozadie: Biele
- Padding: py-24
- Centrovanie: text-center
- Badge: "Oficiálny register obchodných vzťahov V4" (blue-50, blue-800)
- H1: "Transparentnosť pre slovenské podnikanie" (Playfair Display, 5xl/6xl)
- Podnadpis: Text slate-600, text-lg/xl
- Search Bar: 
  - Biele pozadie, shadow-corp
  - Input: slate-50, focus: blue-500 border
  - Button: Slovak Blue bg, white text
- Trust indicators: ShieldCheck, Lock ikony
```

### 3. Features Section
```
- Grid: 3 stĺpce (md:grid-cols-3)
- Karty: Biele, shadow-corp, border slate-100
- Ikony: V slate-50 boxe
- Farba ikon: Slovak Blue alebo Slovak Red
- Hover: border-blue-200
```

### 4. Results Dashboard
```
- Layout: 12-column grid
- Ľavý panel (4 cols):
  - Main Card: Biela, border-top-4 red-500
  - Risk badge: red-100, red-800
  - Score circle: red-50, red-600
  - Data rows: border-t/b slate-100
  - Analytical note: blue-50, blue-900
  - Related entities: Biela karta s personálnymi prepojeniami
- Pravý panel (8 cols):
  - Graph container: Biela, shadow-corp
  - Header: slate-50 bg, border-b
  - Graph area: slate-50 bg, grid pattern (opacity 5%)
  - SVG graf s uzlami
  - Legend: bottom-right, white/90 bg
```

### 5. Legal Docs Section
```
- Layout: Sidebar (1/4) + Content (3/4)
- Sidebar: Biela karta, buttons s ikonami
- Active state: Slovak Blue bg, white text
- Content: Biela karta, prose styling
- Footer: Landmark ikona, approval text
```

### 6. Footer
```
- Pozadie: slate-900
- Text: slate-400
- Grid: 4 stĺpce
- Logo: IluminatiLogo + text white
- Links: hover:text-white
```

## Funkčnosť

### Integrácia s Backendom
- Použiť existujúci API endpoint: `http://localhost:8000/api/search?q={query}`
- Loading state: "Spracovávam..."
- Error handling: Zobraziť chybu v corporate štýle
- Results: Zobraziť v Results Dashboard

### Graf Vizualizácia
- Použiť existujúci `ForceGraph` komponent
- Alebo jednoduchý SVG graf (ako v mocku)
- Farbové kódovanie:
  - Vysoké riziko: Červená (#EE1C25)
  - Stredné riziko: Oranžová
  - Nízke riziko: Modrá (#0B4EA2)

### Routing
- Home: `/` - Landing page
- Results: Automaticky po vyhľadaní
- Legal: `/vop`, `/privacy`, `/disclaimer`, `/cookies`, `/dpa`
- Použiť React Router

## CSS Utility Classes

```css
.font-heading { font-family: 'Playfair Display', serif; }
.font-sans { font-family: 'Inter', sans-serif; }
.slovak-blue-bg { background-color: #0B4EA2; }
.slovak-blue-text { color: #0B4EA2; }
.slovak-red-bg { background-color: #EE1C25; }
.slovak-red-text { color: #EE1C25; }
.shadow-corp { 
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 
              0 2px 4px -1px rgba(0, 0, 0, 0.06); 
}
```

## Interaktívne Prvky

### Buttons
- Primary: Slovak Blue bg, white text, hover: blue-800
- Secondary: White bg, border slate-300, hover: slate-50
- Danger: Red bg (pre high risk actions)

### Cards
- Biele pozadie
- Shadow: shadow-corp
- Border: slate-100/200
- Hover: border-blue-200 alebo scale-105

### Inputs
- Pozadie: slate-50
- Border: slate-200
- Focus: blue-500 border + ring-1

## Responsive Design

### Breakpoints
- Mobile: < 768px (md)
- Tablet: 768px - 1024px
- Desktop: > 1024px (lg)

### Mobile Adaptácie
- Hamburger menu namiesto desktop menu
- Stacked layout pre features
- Full-width search bar
- Single column pre results

## Animácie

- Fade-in pre výsledky
- Slide-in-from-bottom pre dashboard
- Hover transitions (scale, color)
- Smooth scrolling

## Štandardy

### Accessibility
- WCAG 2.1 AA compliance
- Keyboard navigation
- Screen reader support
- Proper contrast ratios

### Performance
- Lazy loading pre obrázky
- Code splitting pre routes
- Optimized bundle size

## Implementačné Poznámky

1. **Zachovať existujúci backend API** - len zmeniť frontend
2. **Použiť existujúci ForceGraph** - alebo jednoduchý SVG
3. **Zachovať routing** - React Router už existuje
4. **Legal docs** - použiť existujúce stránky, len upraviť styling
5. **Logo komponent** - vytvoriť nový IluminatiLogo.jsx

## Checklist Implementácie

- [ ] Vytvoriť IluminatiLogo komponent
- [ ] Aktualizovať HomePage.jsx s novým dizajnom
- [ ] Pridať Google Fonts (Inter, Playfair Display)
- [ ] Implementovať Navbar s novým logom
- [ ] Vytvoriť Hero section s corporate search bar
- [ ] Pridať Features section
- [ ] Implementovať Results Dashboard
- [ ] Integrovať s backendom API
- [ ] Pridať graf vizualizáciu (ForceGraph alebo SVG)
- [ ] Aktualizovať Footer
- [ ] Pridať responsive design
- [ ] Testovať na mobile/tablet/desktop
- [ ] Optimalizovať performance

---

**Dátum vytvorenia:** December 2024  
**Verzia:** 5.0  
**Téma:** Slovak Enterprise Edition

