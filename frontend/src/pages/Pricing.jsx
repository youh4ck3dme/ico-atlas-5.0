import React from 'react';
import { Check, Star, Crown, Zap, Building2, Users, Shield, Sparkles, Globe, TrendingUp, Award, Infinity } from 'lucide-react';

const pricingTiers = [
    {
        name: 'STARTER',
        price: { monthly: '€0', yearly: '€0' },
        description: 'Pre malých podnikateľov a študentov',
        icon: Star,
        color: 'from-gray-600 to-gray-800',
        features: [
            '✓ 50 podrobných informácií o firmách',
            '✓ Monitorovanie 10 firiem',
            '✓ Email upozornenia na zmeny',
            '✓ Vyhľadávanie firiem',
            '✓ Export do PDF (max. 5 záznamov/mesiac)',
            '✓ 1 prístupový účet',
            '✓ Základná podpora emailom'
        ],
        popular: false
    },
    {
        name: 'BUSINESS',
        price: { monthly: '€29', yearly: '€229' },
        description: 'Pre malé a stredné podniky',
        icon: Building2,
        color: 'from-[#D4AF37] to-[#FFD700]',
        features: [
            '✓ Neobmedzený monitoring firiem',
            '✓ Neobmedzené podrobné informácie',
            '✓ Export účtovných závierok do Excelu',
            '✓ Export kontaktov (max. 500/mesiac)',
            '✓ Vyhľadávanie s kontaktnými informáciami',
            '✓ Kontrolný panel s analytickými prehľadmi',
            '✓ 5 prístupových účtov',
            '✓ Základné API služby (100 volaní/den)',
            '✓ Prioritná email podpora',
            '✓ Pravidelné reporty o zmene stavu sledovaných firiem',
            '✓ Analýza finančných ukazovateľov',
            '✓ Rizikové skóre firiem',
            '✓ História zmien vedenia',
            '✓ Možnosť exportu do CSV'
        ],
        popular: true
    },
    {
        name: 'PROFESSIONAL',
        price: { monthly: '€69', yearly: '€599' },
        description: 'Pre stredné a veľké firmy',
        icon: TrendingUp,
        color: 'from-blue-600 to-blue-800',
        features: [
            '✓ Všetky funkcie BUSINESS balíka',
            '✓ Neobmedzený export kontaktov',
            '✓ Pokročilé API služby (1,000 volaní/den)',
            '✓ Hromadné vyhľadávanie a export',
            '✓ Pokročilá analýza rizík',
            '✓ Kreditné skóre a ratingy',
            '✓ Monitorovanie dodávateľov a odberateľov',
            '✓ Export do všetkých formátov (Excel, CSV, PDF, XML)',
            '✓ 15 prístupových účtov',
            '✓ Telefónna podpora (pracovné dni 9:00-17:00)',
            '✓ Prispôsobené reporty',
            '✓ Integrácia s ERP systémami (Money S3, Pohoda, SAP)',
            '✓ Prediktívna analýza rizík',
            '✓ Analýza odvetvových ukazovateľov',
            '✓ Prístup k historickým dátam (5 rokov späť)'
        ],
        popular: false
    },
    {
        name: 'ENTERPRISE',
        price: { monthly: '€199', yearly: '€1,999' },
        description: 'Pre veľké korporácie a štátne inštitúcie',
        icon: Crown,
        color: 'from-purple-600 to-purple-800',
        features: [
            '✓ Všetky funkcie PROFESSIONAL balíka',
            '✓ Neobmedzené API volania',
            '✓ Vlastná databáza prepojená s informačným systémom',
            '✓ Real-time synchronizácia dát',
            '✓ Prispôsobené finančné ukazovatele a predikcie',
            '✓ Hlbocejšia analýza rizík a kreditných skóre',
            '✓ 50 prístupových účtov',
            '✓ 24/7 podpora',
            '✓ Vývoj vlastných reportov a analytických nástrojov',
            '✓ Pravidelné školenia pre používateľov',
            '✓ SLA záruka dostupnosti 99.9%',
            '✓ Prístup k medzinárodným dátam (EU trh)',
            '✓ Analýza medzinárodných dodávateľov',
            '✓ Komplexná analýza trhových rizík',
            '✓ Vlastné algoritmy na vyhodnocovanie rizík'
        ],
        popular: false
    },
    {
        name: 'CUSTOM',
        price: { monthly: 'Dohodou', yearly: 'Dohodou' },
        description: 'Pre veľké medzinárodné spoločnosti',
        icon: Infinity,
        color: 'from-red-600 to-red-800',
        features: [
            '✓ Komplexná integrácia s existujúcimi systémami',
            '✓ Vývoj špecifických analytických nástrojov',
            '✓ Prístup k exkluzívnym dátam a zdrojom',
            '✓ Vlastné API endpointy a formáty',
            '✓ Dedikovaný account manager',
            '✓ Prispôsobené SLA podmienky',
            '✓ Bezplatné školenia a konzultácie',
            '✓ Prístup k beta funkciam'
        ],
        popular: false
    }
];

const comparisonData = [
    { feature: 'Počet podrobných informácií', starter: '50', business: 'Neobmedzene', professional: 'Neobmedzene', enterprise: 'Neobmedzene', custom: 'Neobmedzene' },
    { feature: 'Monitorovanie firiem', starter: '10', business: 'Neobmedzene', professional: 'Neobmedzene', enterprise: 'Neobmedzene', custom: 'Neobmedzene' },
    { feature: 'Export kontaktov', starter: '-', business: '500/mesiac', professional: 'Neobmedzene', enterprise: 'Neobmedzene', custom: 'Neobmedzene' },
    { feature: 'API volania', starter: '-', business: '100/den', professional: '1,000/den', enterprise: 'Neobmedzene', custom: 'Neobmedzene' },
    { feature: 'Prístupové účty', starter: '1', business: '5', professional: '15', enterprise: '50', custom: 'Neobmedzene' },
    { feature: 'Podpora', starter: 'Email', business: 'Email', professional: 'Telefón', enterprise: '24/7', custom: 'Dedikovaný' },
    { feature: 'ERP integrácie', starter: '-', business: '-', professional: '✓', enterprise: '✓', custom: '✓' },
    { feature: 'Medzinárodné dáta', starter: '-', business: '-', professional: '-', enterprise: '✓', custom: '✓' }
];

const Pricing = () => {
    const [billingPeriod, setBillingPeriod] = React.useState('yearly');

    return (
        <div className="min-h-screen bg-gradient-to-br from-[#0A0A0A] via-[#1a1a2e] to-[#16213e] relative overflow-hidden">
            {/* Animated Stars Background */}
            <div className="fixed inset-0 overflow-hidden pointer-events-none">
                {Array.from({ length: 150 }).map((_, i) => (
                    <div
                        key={i}
                        className="absolute rounded-full bg-[#D4AF37] animate-pulse"
                        style={{
                            left: `${Math.random() * 100}%`,
                            top: `${Math.random() * 100}%`,
                            width: `${Math.random() * 4 + 1}px`,
                            height: `${Math.random() * 4 + 1}px`,
                            opacity: Math.random() * 0.8 + 0.2,
                            animationDelay: `${Math.random() * 3}s`,
                            animationDuration: `${Math.random() * 4 + 2}s`,
                        }}
                    />
                ))}
            </div>

            <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                {/* Header */}
                <div className="text-center mb-16 animate-fade-in">
                    <h1 className="text-5xl font-bold text-[#D4AF37] mb-6" style={{ textShadow: '0 0 20px rgba(212, 175, 55, 0.5)' }}>
                        Cenové Plány ILUMINATE
                    </h1>
                    <p className="text-xl text-gray-300 max-w-3xl mx-auto mb-10">
                        Vyberte si balík, ktorý najlepšie vyhovuje vašim potrebám. Každý plán obsahuje pokročilé analytické nástroje a prístup k dátam zo 4 krajín V4 regiónu.
                    </p>

                    {/* Billing Toggle */}
                    <div className="flex justify-center items-center gap-4 mb-4">
                        <span className={`text-sm font-bold ${billingPeriod === 'monthly' ? 'text-white' : 'text-gray-400'}`}>Mesačne</span>
                        <button
                            onClick={() => setBillingPeriod(billingPeriod === 'monthly' ? 'yearly' : 'monthly')}
                            className="w-16 h-8 bg-[#D4AF37]/20 rounded-full p-1 relative transition-colors duration-300 border border-[#D4AF37]/50"
                        >
                            <div
                                className={`w-5 h-5 rounded-full bg-[#D4AF37] transition-transform duration-300 transform ${billingPeriod === 'yearly' ? 'translate-x-8' : 'translate-x-0'}`}
                            />
                        </button>
                        <span className={`text-sm font-bold ${billingPeriod === 'yearly' ? 'text-white' : 'text-gray-400'}`}>
                            Ročne <span className="text-[#D4AF37] text-xs ml-1">(-35%)</span>
                        </span>
                    </div>

                    {/* Money Back Guarantee Badge */}
                    <div className="flex justify-center mb-4 animate-fade-in delay-200">
                        <div className="inline-flex items-center gap-2 bg-green-500/10 border border-green-500/30 rounded-full px-4 py-1.5 backdrop-blur-sm shadow-[0_0_15px_rgba(34,197,94,0.2)]">
                            <Shield className="text-green-400 w-4 h-4" />
                            <span className="text-green-100 text-xs font-bold tracking-wide uppercase">
                                30-dňová garancia vrátenia peňazí
                            </span>
                        </div>
                    </div>
                </div>

                {/* Pricing Cards */}
                <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6 mb-16">
                    {pricingTiers.map((tier, index) => (
                        <div
                            key={tier.name}
                            className={`relative bg-[#0A0A0A]/80 backdrop-blur-md border-2 rounded-2xl p-6 transition-all duration-300 hover:transform hover:scale-105 hover:shadow-[0_0_40px_rgba(212,175,55,0.3)] ${tier.popular ? 'border-[#D4AF37] shadow-[0_0_30px_rgba(212,175,55,0.4)]' : 'border-[#D4AF37]/30'
                                }`}
                            style={{ animationDelay: `${index * 0.1}s` }}
                        >
                            {tier.popular && (
                                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                                    <span className="bg-gradient-to-r from-[#D4AF37] to-[#FFD700] text-[#0A0A0A] px-4 py-1 rounded-full text-sm font-bold">
                                        Odporúčané
                                    </span>
                                </div>
                            )}

                            <div className="text-center mb-6">
                                <div className={`inline-flex items-center justify-center w-16 h-16 rounded-full bg-gradient-to-r ${tier.color} mb-4`}>
                                    <tier.icon className="w-8 h-8 text-white" />
                                </div>
                                <h3 className="text-2xl font-bold text-[#D4AF37] mb-2">{tier.name}</h3>
                                <p className="text-gray-400 text-sm mb-4">{tier.description}</p>
                                <div className="flex flex-col items-center justify-center">
                                    {billingPeriod === 'yearly' && tier.price.yearly !== '€0' && tier.price.yearly !== 'Dohodou' && (
                                        <span className="text-gray-500 line-through text-sm font-semibold">
                                            €{Math.round(parseInt(tier.price.yearly.replace(/[^0-9]/g, '')) * 1.53)}
                                        </span>
                                    )}
                                    <div className="flex items-baseline justify-center">
                                        <span className="text-4xl font-bold text-white">{tier.price[billingPeriod]}</span>
                                        {tier.name !== 'CUSTOM' && (
                                            <span className="text-gray-400 ml-1">{billingPeriod === 'monthly' ? '/mesiac' : '/rok'}</span>
                                        )}
                                    </div>
                                </div>
                            </div>

                            <ul className="space-y-3 mb-6">
                                {tier.features.map((feature, i) => (
                                    <li key={i} className="flex items-start gap-2 text-sm text-gray-300">
                                        <Check className="w-4 h-4 text-[#D4AF37] mt-0.5 flex-shrink-0" />
                                        <span>{feature}</span>
                                    </li>
                                ))}
                            </ul>

                            <button className={`w-full py-3 px-4 rounded-xl font-bold transition-all duration-300 ${tier.popular
                                ? 'bg-gradient-to-r from-[#D4AF37] to-[#FFD700] text-[#0A0A0A] hover:from-[#FFD700] hover:to-[#D4AF37] hover:shadow-[0_0_30px_rgba(212,175,55,0.6)]'
                                : 'bg-[#D4AF37]/20 border-2 border-[#D4AF37]/50 text-[#D4AF37] hover:bg-[#D4AF37]/30'
                                }`}>
                                {tier.name === 'CUSTOM' ? 'Kontaktujte nás' : 'Začať teraz'}
                            </button>
                        </div>
                    ))}
                </div>

                {/* Comparison Table */}
                <div className="bg-[#0A0A0A]/80 backdrop-blur-md border-2 border-[#D4AF37]/30 rounded-2xl p-8 mb-16">
                    <h2 className="text-3xl font-bold text-[#D4AF37] text-center mb-8" style={{ textShadow: '0 0 10px rgba(212, 175, 55, 0.5)' }}>
                        Porovnanie funkcií
                    </h2>

                    <div className="overflow-x-auto">
                        <table className="w-full text-sm">
                            <thead>
                                <tr className="border-b border-[#D4AF37]/30">
                                    <th className="text-left py-4 px-4 text-[#D4AF37] font-bold">Funkcia</th>
                                    <th className="text-center py-4 px-4 text-gray-300 font-bold">STARTER</th>
                                    <th className="text-center py-4 px-4 text-[#D4AF37] font-bold">BUSINESS</th>
                                    <th className="text-center py-4 px-4 text-gray-300 font-bold">PROFESSIONAL</th>
                                    <th className="text-center py-4 px-4 text-gray-300 font-bold">ENTERPRISE</th>
                                    <th className="text-center py-4 px-4 text-gray-300 font-bold">CUSTOM</th>
                                </tr>
                            </thead>
                            <tbody>
                                {comparisonData.map((row, index) => (
                                    <tr key={index} className="border-b border-[#D4AF37]/10 hover:bg-[#D4AF37]/5">
                                        <td className="py-3 px-4 text-gray-300 font-medium">{row.feature}</td>
                                        <td className="py-3 px-4 text-center text-gray-400">{row.starter}</td>
                                        <td className="py-3 px-4 text-center text-[#D4AF37] font-bold">{row.business}</td>
                                        <td className="py-3 px-4 text-center text-gray-400">{row.professional}</td>
                                        <td className="py-3 px-4 text-center text-gray-400">{row.enterprise}</td>
                                        <td className="py-3 px-4 text-center text-gray-400">{row.custom}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>

                {/* Call to Action */}
                <div className="text-center">
                    <div className="bg-gradient-to-r from-[#D4AF37]/20 via-[#FFD700]/20 to-[#D4AF37]/20 rounded-2xl p-8 backdrop-blur-md border-2 border-[#D4AF37]/30">
                        <h3 className="text-3xl font-bold text-[#D4AF37] mb-4">Máte otázky?</h3>
                        <p className="text-gray-300 mb-6 max-w-2xl mx-auto">
                            Kontaktujte náš tím odborníkov a získajte bezplatnú konzultáciu. Pomôžeme vám vybrať ten správny balík pre vaše potreby.
                        </p>
                        <button className="bg-gradient-to-r from-[#D4AF37] to-[#FFD700] hover:from-[#FFD700] hover:to-[#D4AF37] text-[#0A0A0A] px-8 py-4 rounded-xl font-bold text-lg transition-all duration-300 transform hover:scale-105 hover:shadow-[0_0_30px_rgba(212,175,55,0.6)]">
                            Kontaktujte nás
                        </button>
                    </div>
                </div>
            </div>

            {/* Custom Animations */}
            <style>{`
        @keyframes fade-in {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in {
          animation: fade-in 0.8s ease-out;
        }
      `}</style>
        </div>
    );
}

export default Pricing;