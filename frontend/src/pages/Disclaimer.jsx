import React from 'react';
import { AlertTriangle, ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';

const DisclaimerPage = () => {
  return (
    <div className="min-h-screen bg-slate-50">
      <div className="max-w-4xl mx-auto px-8 py-12">
        <Link to="/" className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 mb-6">
          <ArrowLeft size={18} />
          Späť na hlavnú stránku
        </Link>

        <div className="bg-white rounded-lg shadow-sm p-8">
          <div className="flex items-center gap-3 mb-6">
            <AlertTriangle className="text-amber-600" size={32} />
            <h1 className="text-3xl font-bold text-slate-900">
              Vyhlásenie o odmietnutí zodpovednosti
            </h1>
          </div>

          <div className="prose prose-slate max-w-none">
            <div className="bg-amber-50 border-l-4 border-amber-400 p-6 mb-8">
              <p className="text-amber-900 font-semibold text-lg leading-relaxed">
                Dáta zobrazené na portáli ILUMINATE SYSTEM sú agregované z verejných zdrojov 
                (Obchodné registre, Finančné správy V4) automatizovaným spôsobom. ILUMINATE SYSTEM nevytvára tieto 
                dáta a nenesie zodpovednosť za ich aktuálnosť, správnosť či úplnosť. Informácie slúžia 
                výhradne na podporu rozhodovania (business intelligence) a nenahrádzajú oficiálne právne 
                úkony alebo úradné výpisy. Rizikové skóre je výsledkom štatistického modelu, nie obvinením 
                z trestnej činnosti.
              </p>
            </div>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">1. Povaha dát</h2>
              <p className="text-slate-700 leading-relaxed">
                Všetky dáta zobrazené na Platforme sú získavané z oficiálnych, verejne dostupných 
                zdrojov. ILUMINATE SYSTEM funguje ako agregátor a vizualizátor týchto dát, nie ako ich tvorca. 
                Dáta môžu obsahovať chyby, ktoré vznikli už v zdrojových systémoch (štátne registry).
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">2. Aktuálnosť dát</h2>
              <p className="text-slate-700 leading-relaxed">
                ILUMINATE SYSTEM sa snaží udržiavať dáta aktuálne, ale vzhľadom na povahu agregácie z viacerých 
                zdrojov a cache mechanizmy môže dôjsť k oneskoreniu v aktualizácii. Dáta sa aktualizujú 
                pravidelne, ale nie v reálnom čase. Pre oficiálne a právne záväzné informácie vždy 
                použite pôvodné zdroje (oficiálne registry).
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">3. Rizikové skóre a analýzy</h2>
              <p className="text-slate-700 leading-relaxed mb-4">
                Rizikové skóre a všetky analýzy poskytované ILUMINATE SYSTEM sú výsledkom štatistických modelov 
                a algoritmov. Tieto skóre:
              </p>
              <ul className="list-disc list-inside text-slate-700 space-y-2 ml-4">
                <li>Nie sú právnym obvinením z trestnej činnosti</li>
                <li>Nie sú úradným posudkom</li>
                <li>Slúžia len na podporu rozhodovania</li>
                <li>Môžu obsahovať chyby alebo nepresnosti</li>
                <li>Nenahrádzajú profesionálne právne alebo finančné poradenstvo</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">4. Obchodné rozhodnutia</h2>
              <p className="text-slate-700 leading-relaxed">
                ILUMINATE SYSTEM nenesie zodpovednosť za akékoľvek obchodné rozhodnutia, ktoré užívateľ urobí 
                na základe dát zobrazených na Platforme. Užívateľ používa Platformu na vlastné riziko 
                a je zodpovedný za vlastné rozhodnutia.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">5. PDF reporty</h2>
              <p className="text-slate-700 leading-relaxed">
                Všetky PDF reporty generované cez Platformu obsahujú toto vyhlásenie na každej strane. 
                Reporty slúžia len na interné použitie a nemôžu byť použité ako oficiálne dokumenty 
                v právnych procesoch bez overenia v pôvodných zdrojoch.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">6. Odporúčania</h2>
              <p className="text-slate-700 leading-relaxed mb-4">
                Pre kritické obchodné rozhodnutia odporúčame:
              </p>
              <ul className="list-disc list-inside text-slate-700 space-y-2 ml-4">
                <li>Overiť informácie v oficiálnych registroch</li>
                <li>Konzultovať právneho alebo finančného poradcu</li>
                <li>Použiť viacero zdrojov informácií</li>
                <li>Nepokladať ILUMINATE SYSTEM za jediný zdroj pravdy</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">7. Kontakt</h2>
              <p className="text-slate-700 leading-relaxed">
                Pre otázky týkajúce sa tohto vyhlásenia kontaktujte:{" "}
                <a href="mailto:support@crossbordernexus.com" className="text-blue-600 hover:underline">
                  support@crossbordernexus.com
                </a>
              </p>
            </section>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DisclaimerPage;

