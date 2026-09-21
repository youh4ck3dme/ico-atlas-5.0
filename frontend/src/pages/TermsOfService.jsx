import React from 'react';
import { FileText, ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';
import SEOHead from '../components/SEOHead';
import Logo from '../components/Logo';

const TermsOfService = () => {
  return (
    <>
      <SEOHead 
        title="Všeobecné obchodné podmienky | ILUMINATI SYSTEM"
        description="Všeobecné obchodné podmienky a podmienky používania služby ILUMINATI SYSTEM."
      />
      <div className="min-h-screen bg-slate-50">
      <div className="max-w-4xl mx-auto px-8 py-12">
        <Link to="/" className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 mb-6">
          <ArrowLeft size={18} />
          Späť na hlavnú stránku
        </Link>

        <div className="bg-white rounded-lg shadow-sm p-8">
          <div className="flex flex-col md:flex-row items-center md:items-start gap-4 mb-6">
            <Logo size="small" showText={false} className="md:mr-4" />
            <div className="flex-1 text-center md:text-left">
              <div className="flex items-center gap-3 justify-center md:justify-start mb-2">
                <FileText className="text-blue-600" size={32} />
                <h1 className="text-3xl font-bold text-slate-900">
                  Všeobecné obchodné podmienky (VOP)
                </h1>
              </div>
            </div>
          </div>

          <div className="prose prose-slate max-w-none">
            <p className="text-sm text-slate-500 mb-8">
              <strong>Platné od:</strong> December 2024<br />
              <strong>Verzia:</strong> 1.1
            </p>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">1. Definícia služby</h2>
              <p className="text-slate-700 leading-relaxed">
                ILUMINATE SYSTEM (ďalej len "IS" alebo "Platforma") je informačný nástroj 
                typu Business Intelligence, ktorý agreguje a vizualizuje verejne dostupné dáta 
                z obchodných registrov krajín V4 (Česká republika, Slovensko, Poľsko, Maďarsko). 
                ILUMINATE SYSTEM poskytuje užívateľom nástroje na analýzu vlastníckych štruktúr, identifikáciu 
                rizík a prevenciu podvodov typu "karusel".
              </p>
              <p className="text-slate-700 leading-relaxed mt-4">
                <strong>Dôležité:</strong> ILUMINATE SYSTEM negarantuje správnosť dát v reálnom čase. Dáta sú 
                získavané z oficiálnych štátnych registrov, ale chyby môžu vzniknúť už v zdrojových 
                systémoch. ILUMINATE SYSTEM nenesie zodpovednosť za nepresnosti v pôvodných dátach.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">2. Vylúčenie zodpovednosti (Limitation of Liability)</h2>
              <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-4">
                <p className="text-red-800 font-semibold">
                  Poskytovateľ nenesie zodpovednosť za akékoľvek priame alebo nepriame škody, 
                  ušlý zisk alebo obchodné rozhodnutia vykonané Užívateľom na základe dát z portálu. 
                  Dáta majú len informatívny charakter a nenahrádzajú úradné výpisy ani právne poradenstvo.
                </p>
              </div>
              <ul className="list-disc list-inside text-slate-700 space-y-2 ml-4">
                <li>ILUMINATE SYSTEM poskytuje služby "tak, ako sú" (as-is) bez záruky akéhokoľvek druhu.</li>
                <li>Užívateľ používa Platformu na vlastné riziko.</li>
                <li>ILUMINATE SYSTEM nezodpovedá za obchodné rozhodnutia založené na zobrazených dátach.</li>
                <li>Rizikové skóre a analýzy sú výsledkom štatistických modelov, nie právnych posudkov.</li>
                <li>ILUMINATE SYSTEM nezodpovedá za výpadky externých registrov alebo oneskorenia v aktualizácii dát.</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">3. Model predplatného (SaaS)</h2>
              <h3 className="text-xl font-semibold text-slate-800 mb-3">3.1. Typy predplatného</h3>
              <ul className="list-disc list-inside text-slate-700 space-y-2 ml-4">
                <li><strong>Free:</strong> Obmedzený počet vyhľadávaní mesačne (napr. 5 vyhľadávaní)</li>
                <li><strong>Pro:</strong> Neobmedzené vyhľadávania, pokročilé analýzy, mesačné/ročné predplatné</li>
                <li><strong>Enterprise:</strong> API prístup, vlastné integrácie, individuálna podpora</li>
              </ul>

              <h3 className="text-xl font-semibold text-slate-800 mb-3 mt-6">3.2. Automatická obnova</h3>
              <p className="text-slate-700 leading-relaxed">
                Predplatné sa automaticky obnovuje na konci fakturačného obdobia (mesiac/rok), 
                pokiaľ ho Užívateľ nezruší najmenej 7 dní pred koncom platnosti.
              </p>

              <h3 className="text-xl font-semibold text-slate-800 mb-3 mt-6">3.3. Storno podmienky</h3>
              <p className="text-slate-700 leading-relaxed">
                Užívateľ môže zrušiť predplatné kedykoľvek cez svoj účet. Zrušenie predplatného 
                musí byť vykonané najmenej 7 dní pred koncom fakturačného obdobia, aby sa zabránilo 
                automatickej obnove. Vrátenie peňazí za už zaplatené obdobie sa neposkytuje, 
                okrem prípadov výslovne dohodnutých v individuálnych zmluvách (Enterprise).
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">4. Fair Use Policy & Rizikový Manažment</h2>
              
              <h3 className="text-xl font-semibold text-slate-800 mb-3">4.1. Zákaz scrapovania Platformy</h3>
              <div className="bg-amber-50 border-l-4 border-amber-400 p-4 mb-4">
                <p className="text-amber-800 font-semibold">
                  Je prísne zakázané používať automatizované nástroje (boty, scrapery, API bez 
                  oprávnenia) na ťažbu dát z Platformy. Porušenie vedie k okamžitému zrušeniu 
                  účtu bez náhrady a možnému právnemu postihu.
                </p>
              </div>
              <ul className="list-disc list-inside text-slate-700 space-y-2 ml-4 mb-6">
                <li>Zakázané je používanie web scrapingu, crawlerov alebo podobných nástrojov.</li>
                <li>API prístup je dostupný len pre Enterprise klientov s platnou licenciou.</li>
                <li>ILUMINATI SYSTEM si vyhradzuje právo monitorovať používanie Platformy a detegovať zneužitie.</li>
                <li>Pri porušení sa účet okamžite zablokuje a dáta môžu byť použité ako dôkaz.</li>
              </ul>

              <h3 className="text-xl font-semibold text-slate-800 mb-3">4.2. Fair Use Policy pre Scraping Externých Zdrojov</h3>
              <div className="bg-blue-50 border-l-4 border-blue-400 p-4 mb-4">
                <p className="text-blue-800 font-semibold mb-2">
                  ILUMINATI SYSTEM dodržiava "Fair Use Policy" pri získavaní dát z externých zdrojov:
                </p>
                <ul className="list-disc list-inside text-blue-700 space-y-1 ml-4">
                  <li>Nepreťažujeme štátne servery - používame rozumné rate limiting</li>
                  <li>Používame rotujúce proxy a User-Agent hlavičky pre distribúciu záťaže</li>
                  <li>Respektujeme robots.txt a oficiálne API endpointy, ak sú dostupné</li>
                  <li>Cache mechanizmy znižujú počet požiadaviek na externé servery</li>
                  <li>Vždy uvádzame zdroj dát pri zobrazení informácií</li>
                </ul>
              </div>

              <h3 className="text-xl font-semibold text-slate-800 mb-3">4.3. Zdrojovanie Dát</h3>
              <p className="text-slate-700 leading-relaxed mb-4">
                ILUMINATI SYSTEM vždy uvádza zdroj dát pri zobrazení informácií. Hlavné zdroje:
              </p>
              <ul className="list-disc list-inside text-slate-700 space-y-2 ml-4">
                <li><strong>Slovensko:</strong> Obchodný register SR (ORSR), Živnostenský register (ZRSR), Register účtovných závierok (RUZ), Finančná správa SR</li>
                <li><strong>Česká republika:</strong> ARES (Administrativní registr ekonomických subjektů)</li>
                <li><strong>Poľsko:</strong> KRS (Krajowy Rejestr Sądowy)</li>
                <li><strong>Maďarsko:</strong> Cégközlöny</li>
              </ul>
              <p className="text-slate-700 leading-relaxed mt-4">
                Všetky dáta sú získavané z verejne dostupných, oficiálnych zdrojov. 
                ILUMINATI SYSTEM funguje ako agregátor a vizualizátor týchto dát.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">5. Duševné vlastníctvo</h2>
              <p className="text-slate-700 leading-relaxed">
                Všetky práva k Platforme, vrátane softvéru, dizajnu, loga a obchodnej značky, 
                patria Poskytovateľovi. Užívateľ získava len licenciu na používanie služby podľa 
                týchto VOP.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">6. Zmena podmienok</h2>
              <p className="text-slate-700 leading-relaxed">
                Poskytovateľ si vyhradzuje právo zmeniť tieto VOP. O zmene budú Užívateľovia 
                informovaní e-mailom alebo oznámením v aplikácii najmenej 30 dní vopred. 
                Pokračovaním v používaní Platformy po zmene sa Užívateľ zaväzuje dodržiavať nové podmienky.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">7. Právne predpisy a príslušnosť</h2>
              <p className="text-slate-700 leading-relaxed">
                Tieto VOP sa riadia právnym poriadkom Slovenskej republiky. Prípadné spory sa 
                riešia pred príslušnými súdmi Slovenskej republiky.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">8. Kontakt</h2>
              <p className="text-slate-700 leading-relaxed">
                Pre otázky týkajúce sa týchto VOP kontaktujte nás na: 
                <a href="mailto:legal@crossbordernexus.com" className="text-blue-600 hover:underline ml-1">
                  legal@crossbordernexus.com
                </a>
              </p>
            </section>
          </div>
        </div>
      </div>
    </div>
    </>
  );
};

export default TermsOfService;

