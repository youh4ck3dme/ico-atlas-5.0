# 🧪 Frontend Unit Tests - Dokumentácia

## ✅ Implementované testy

### Testovací framework
- **Vitest** - Moderný, rýchly test runner pre Vite
- **React Testing Library** - Testovanie React komponentov
- **jsdom** - DOM simulácia pre testy

### Testované komponenty

#### 1. Footer (`Footer.test.jsx`)
- ✅ Renderovanie footer komponenty
- ✅ Zobrazenie právnych dokumentov (5 linkov)
- ✅ Kontaktné informácie
- ✅ Copyright informácie
- ✅ Správne link atribúty

#### 2. LoadingSkeleton (`LoadingSkeleton.test.jsx`)
- ✅ Default skeleton renderovanie
- ✅ Search skeleton (type="search")
- ✅ Card skeleton (type="card")
- ✅ Graph skeleton (type="graph")
- ✅ Rôzne typy skeletonov

#### 3. ErrorBoundary (`ErrorBoundary.test.jsx`)
- ✅ Renderovanie children bez chyby
- ✅ Zachytenie chýb a zobrazenie error fallback
- ✅ Zobrazenie error správy

#### 4. IluminatiLogo (`IluminatiLogo.test.jsx`)
- ✅ Renderovanie SVG loga
- ✅ Správne SVG atribúty (width, height)
- ✅ Aplikovanie className
- ✅ Default size handling

#### 5. Performance Utilities (`performance.test.js`)
- ✅ Debounce funkcionalita
- ✅ Throttle funkcionalita
- ✅ PerformanceMonitor tracking

## 📊 Test Coverage

**Aktuálny stav:**
- **Test súbory:** 5
- **Testy:** 23
- **Úspešnosť:** 100% (23/23)

## 🚀 Spustenie testov

```bash
# Všetky testy
cd frontend
npm test

# Watch mode (pre development)
npm test -- --watch

# UI mode
npm run test:ui

# Coverage report
npm run test:coverage
```

## 📝 Testovacia konfigurácia

### `vitest.config.js`
- Environment: jsdom
- Setup file: `src/test/setup.js`
- Coverage provider: v8

### `src/test/setup.js`
- Automatický cleanup po každom teste
- Jest DOM matchers

## 🎯 Ďalšie testy na pridanie

### Komponenty
- [ ] ForceGraph - graf vizualizácia
- [ ] Layout - layout wrapper
- [ ] SEOHead - SEO meta tagy

### Pages
- [ ] HomePageNew - hlavná stránka
- [ ] TermsOfService - VOP stránka
- [ ] PrivacyPolicy - Privacy stránka

### Hooks
- [ ] useTheme - theme switching
- [ ] useOffline - offline detection
- [ ] useKeyboardShortcuts - keyboard shortcuts

### Utils
- [ ] export.js - export funkcionalita

## 📚 Best Practices

1. **Testovanie správania, nie implementácie**
2. **Použitie React Testing Library queries**
3. **Mocking externých závislostí**
4. **Cleanup po každom teste**
5. **Popisné test názvy**

---

*Posledná aktualizácia: December 2024*

