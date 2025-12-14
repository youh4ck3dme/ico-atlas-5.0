# 🗺️ IČO ATLAS 5.0 - ROADMAP

## 📍 Aktuálny Stav: Fáza 1 & 2 ✅ Dokončená

---

## 🔮 Fáza 3: API & Funkčnosť (Odporúčaná)

### 1. 🔌 Integrácia API

#### Laravel API Routes
- [ ] Vytvoriť API routes v `routes/api.php`
- [ ] RESTful endpoints pre vyhľadávanie firiem
- [ ] GET `/api/companies/search?q={query}`
- [ ] GET `/api/companies/{ico}`
- [ ] GET `/api/companies` (list s pagination)
- [ ] Laravel API Resources pre formátovanie odpovedí

#### Integrácia so Slovenským obchodným registrom
- [ ] Research dostupných API (Ministry of Justice, etc.)
- [ ] Implementácia API klienta
- [ ] Error handling a fallback mechanisms
- [ ] Data normalization

#### Performance & Caching
- [ ] Laravel Cache pre často hľadané firmy
- [ ] Rate limiting (Laravel Throttle)
- [ ] Database indexing
- [ ] Query optimization

#### API Dokumentácia
- [ ] Laravel API Documentation (Scribe/Swagger)
- [ ] Postman collection
- [ ] API examples v dokumentácii

---

### 2. 🔐 Autentifikácia

#### Laravel Sanctum / Breeze
- [ ] Inštalácia Laravel Sanctum alebo Breeze
- [ ] User model a migration
- [ ] Registrácia používateľov
- [ ] Email verification
- [ ] Password reset flow

#### OAuth2 Integrácia
- [ ] Google OAuth (Laravel Socialite)
- [ ] Facebook OAuth
- [ ] GitHub OAuth (pre vývojárov)
- [ ] Custom OAuth provider setup

#### User Management
- [ ] User profil stránka
- [ ] Editácia profilu
- [ ] Zmena hesla
- [ ] Avatar upload
- [ ] Account settings

#### Authorization
- [ ] Role-based access control (RBAC)
- [ ] Permission system
- [ ] Admin panel (voliteľné)

---

### 3. ⚡ Vyhľadávanie v reálnom čase

#### Autocomplete
- [ ] Debounced search input
- [ ] Dropdown s výsledkami
- [ ] Keyboard navigation
- [ ] Highlight matching text
- [ ] Loading states

#### WebSocket Support
- [ ] Laravel Echo setup
- [ ] Pusher/Ably integrácia
- [ ] Real-time notifications
- [ ] Live search updates
- [ ] Broadcast events

#### Search Features
- [ ] Search history (localStorage + DB)
- [ ] Favorites/bookmarks
- [ ] Recent searches
- [ ] Popular searches
- [ ] Search suggestions

#### Advanced Search
- [ ] Multi-criteria search
- [ ] Advanced filters UI
- [ ] Save search queries
- [ ] Share search results

---

### 4. 📊 Export údajov

#### CSV Export
- [ ] Laravel Excel (Maatwebsite)
- [ ] CSV generation
- [ ] Custom column selection
- [ ] Batch export

#### PDF Export
- [ ] DomPDF alebo Barryvdh PDF
- [ ] Company detail PDF
- [ ] Search results PDF
- [ ] Custom PDF templates
- [ ] Branding (Slovak Enterprise Luxury)

#### Excel Export
- [ ] Excel file generation
- [ ] Multiple sheets support
- [ ] Formatted cells
- [ ] Charts (voliteľné)

#### Print Functionality
- [ ] Print-friendly CSS
- [ ] Print preview
- [ ] Browser print dialog
- [ ] PDF generation from print

---

### 5. 🔍 Pokročilé filtrovanie

#### Basic Filters
- [ ] Filter by IČO
- [ ] Filter by company name
- [ ] Filter by address
- [ ] Filter by city/region
- [ ] Filter by industry

#### Advanced Filters
- [ ] Filter by company size
- [ ] Filter by registration date
- [ ] Filter by status (active/inactive)
- [ ] Multiple filter combination
- [ ] Filter presets

#### UI Components
- [ ] Filter sidebar/drawer
- [ ] Active filters display
- [ ] Clear filters button
- [ ] Filter chips/tags
- [ ] Mobile-friendly filter UI

#### Saved Searches
- [ ] Save filter combinations
- [ ] Named searches
- [ ] Quick access to saved searches
- [ ] Edit/delete saved searches
- [ ] Share saved searches

#### Comparison
- [ ] Select multiple companies
- [ ] Compare side-by-side
- [ ] Comparison table
- [ ] Export comparison

---

## 🚀 Fáza 4: Pokročilé funkcie (Future)

### Notifications
- [ ] Email notifications
- [ ] Push notifications
- [ ] In-app notifications
- [ ] Notification preferences

### Analytics
- [ ] Search analytics
- [ ] User activity tracking
- [ ] Popular companies
- [ ] Dashboard with stats

### Mobile App
- [ ] React Native / Flutter app
- [ ] iOS app
- [ ] Android app
- [ ] Push notifications

### Integrations
- [ ] API for third-party apps
- [ ] Webhook support
- [ ] Zapier integration
- [ ] Slack integration

---

## 📅 Timeline (Odporúčané)

### Q1 2024
- ✅ Fáza 1 & 2 (Dokončená)
- 🔄 Fáza 3 začiatok

### Q2 2024
- 🔄 API integrácia
- 🔄 Autentifikácia
- 🔄 Základné vyhľadávanie

### Q3 2024
- 🔄 Real-time search
- 🔄 Export funkcie
- 🔄 Pokročilé filtrovanie

### Q4 2024
- 🔮 Fáza 4 plánovanie
- 🔮 Analytics a notifikácie

---

## 🤝 Prispievanie

Chceš pomôcť s implementáciou Fázy 3? 

1. Pozri si [CONTRIBUTING.md](CONTRIBUTING.md)
2. Vyber úlohu z roadmapu
3. Vytvor Pull Request

---

## 📝 Poznámky

- Tento roadmap je flexibilný a môže sa meniť
- Priorita úloh sa môže upraviť podľa potrieb
- Navrhni zmeny cez Issues alebo Pull Requests

---

**Last Updated:** December 2024  
**Version:** 5.0  
**Status:** Phase 1 & 2 Complete ✅

