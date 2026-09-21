import React from 'react';
import { Cookie, ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';

const CookiePolicy = () => {
  return (
    <div className="min-h-screen bg-slate-50">
      <div className="max-w-4xl mx-auto px-8 py-12">
        <Link to="/" className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 mb-6">
          <ArrowLeft size={18} />
          Späť na hlavnú stránku
        </Link>

        <div className="bg-white rounded-lg shadow-sm p-8">
          <div className="flex items-center gap-3 mb-6">
            <Cookie className="text-blue-600" size={32} />
            <h1 className="text-3xl font-bold text-slate-900">
              Cookie Policy
            </h1>
          </div>

          <div className="prose prose-slate max-w-none">
            <p className="text-sm text-slate-500 mb-8">
              <strong>Platné od:</strong> December 2024<br />
              <strong>Verzia:</strong> 1.1
            </p>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">1. Čo sú cookies?</h2>
              <p className="text-slate-700 leading-relaxed">
                Cookies sú malé textové súbory, ktoré sa ukladajú vo vašom prehliadači pri návšteve 
                webovej stránky. Umožňujú Platforme rozpoznať váš prehliadač a zapamätať si určité 
                informácie o vašej návšteve.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">2. Typy cookies používaných na ILUMINATE SYSTEM</h2>
              
              <h3 className="text-xl font-semibold text-slate-800 mb-3">2.1. Technické cookies (Nutné)</h3>
              <div className="bg-green-50 border-l-4 border-green-400 p-4 mb-4">
                <p className="text-green-800 font-semibold mb-2">
                  Tieto cookies sú nevyhnutné pre fungovanie Platformy. Bez nich by Platforma nemohla 
                  fungovať správne. <strong>Nevyžadujú súhlas.</strong>
                </p>
              </div>
              <ul className="list-disc list-inside text-slate-700 space-y-2 ml-4">
                <li><strong>Session cookies:</strong> Umožňujú prihlásenie a udržiavanie prihláseného stavu</li>
                <li><strong>Security cookies:</strong> Ochrana pred útokmi (CSRF tokeny)</li>
                <li><strong>Load balancing cookies:</strong> Rozdelenie zaťaženia medzi servery</li>
                <li><strong>Doba platnosti:</strong> Do ukončenia relácie alebo do 24 hodín</li>
              </ul>

              <h3 className="text-xl font-semibold text-slate-800 mb-3 mt-6">2.2. Analytické cookies (Vyžadujú súhlas)</h3>
              <div className="bg-blue-50 border-l-4 border-blue-400 p-4 mb-4">
                <p className="text-blue-800 font-semibold mb-2">
                  Tieto cookies nám pomáhajú pochopiť, ako užívatelia používajú Platformu. 
                  <strong> Vyžadujú váš súhlas.</strong>
                </p>
              </div>
              <ul className="list-disc list-inside text-slate-700 space-y-2 ml-4">
                <li><strong>Google Analytics:</strong> Sledovanie návštevnosti, správanie užívateľov (anonymizované)</li>
                <li><strong>Hotjar (plánované):</strong> Heatmaps, session recordings (len s explicitným súhlasom)</li>
                <li><strong>Doba platnosti:</strong> 2 roky (Google Analytics), 1 rok (Hotjar)</li>
                <li><strong>Účel:</strong> Zlepšenie používateľskej skúsenosti, identifikácia problémov</li>
              </ul>

              <h3 className="text-xl font-semibold text-slate-800 mb-3 mt-6">2.3. Marketingové cookies (Vyžadujú súhlas)</h3>
              <p className="text-slate-700 leading-relaxed mb-4">
                V súčasnosti ILUMINATE SYSTEM nepoužíva marketingové cookies. V budúcnosti môžeme používať:
              </p>
              <ul className="list-disc list-inside text-slate-700 space-y-2 ml-4">
                <li>Retargeting cookies (Facebook Pixel, Google Ads)</li>
                <li>Conversion tracking</li>
                <li>Vždy len s explicitným súhlasom užívateľa</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">3. Správa cookies</h2>
              <p className="text-slate-700 leading-relaxed mb-4">
                Môžete spravovať svoje cookie preferencie:
              </p>
              <ul className="list-disc list-inside text-slate-700 space-y-2 ml-4">
                <li><strong>V nastaveniach účtu:</strong> Po prihlásení môžete zmeniť preferencie v sekcii "Nastavenia"</li>
                <li><strong>V prehliadači:</strong> Väčšina prehliadačov umožňuje blokovanie alebo mazanie cookies</li>
                <li><strong>Cookie lišta:</strong> Pri prvej návšteve sa zobrazí lišta s možnosťou výberu</li>
              </ul>
              <div className="bg-amber-50 border-l-4 border-amber-400 p-4 mt-4">
                <p className="text-amber-800 text-sm">
                  <strong>Upozornenie:</strong> Blokovanie technických cookies môže spôsobiť, že 
                  Platforma nebude fungovať správne (napr. nebudete sa môcť prihlásiť).
                </p>
              </div>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">4. Cookies tretích strán</h2>
              <p className="text-slate-700 leading-relaxed mb-4">
                ILUMINATE SYSTEM používa služby tretích strán, ktoré môžu ukladať vlastné cookies:
              </p>
              <ul className="list-disc list-inside text-slate-700 space-y-2 ml-4">
                <li><strong>Google Analytics:</strong> Sledovanie návštevnosti (anonymizované)</li>
                <li><strong>Stripe:</strong> Platobná brána (len pri platbe)</li>
                <li><strong>Cloudflare:</strong> CDN a ochrana (technické cookies)</li>
              </ul>
              <p className="text-slate-700 leading-relaxed mt-4">
                Tieto služby majú vlastné zásady ochrany súkromia. Odkazy na ich zásady nájdete 
                v našej <Link to="/privacy" className="text-blue-600 hover:underline">Privacy Policy</Link>.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">5. Zmeny v Cookie Policy</h2>
              <p className="text-slate-700 leading-relaxed">
                Túto Cookie Policy môžeme meniť. O zmene budeme informovať registrovaných užívateľov 
                e-mailom a zverejníme novú verziu na tejto stránke.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">6. Kontakt</h2>
              <p className="text-slate-700 leading-relaxed">
                Pre otázky týkajúce sa cookies kontaktujte:{" "}
                <a href="mailto:privacy@crossbordernexus.com" className="text-blue-600 hover:underline">
                  privacy@crossbordernexus.com
                </a>
              </p>
            </section>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CookiePolicy;

