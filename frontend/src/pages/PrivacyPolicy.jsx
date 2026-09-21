import React from 'react';
import { Shield, ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';
import SEOHead from '../components/SEOHead';

const PrivacyPolicy = () => {
  return (
    <>
      <SEOHead 
        title="Ochrana súkromia | ILUMINATI SYSTEM"
        description="Zásady ochrany súkromia a spracovania osobných údajov v súlade s GDPR."
      />
      <div className="min-h-screen bg-slate-50">
      <div className="max-w-4xl mx-auto px-8 py-12">
        <Link to="/" className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 mb-6">
          <ArrowLeft size={18} />
          Späť na hlavnú stránku
        </Link>

        <div className="bg-white rounded-lg shadow-sm p-8">
          <div className="flex items-center gap-3 mb-6">
            <Shield className="text-blue-600" size={32} />
            <h1 className="text-3xl font-bold text-slate-900">
              Zásady ochrany osobných údajov (GDPR)
            </h1>
          </div>

          <div className="prose prose-slate max-w-none">
            <p className="text-sm text-slate-500 mb-8">
              <strong>Platné od:</strong> December 2024<br />
              <strong>Verzia:</strong> 1.1<br />
              <strong>Prevádzkovateľ:</strong> [Názov s.r.o.], IČO: [IČO], Sídlo: [Adresa]
            </p>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">1. Úvod</h2>
              <p className="text-slate-700 leading-relaxed">
                Tento dokument popisuje, ako ILUMINATE SYSTEM spracúva osobné údaje v súlade 
                s Nariadením GDPR (General Data Protection Regulation) a zákonmi o ochrane osobných údajov 
                platnými v krajinách V4.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">2. Dve skupiny dotknutých osôb</h2>
              
              <h3 className="text-xl font-semibold text-slate-800 mb-3">2.1. Registrovaní užívatelia (Klienti)</h3>
              <p className="text-slate-700 leading-relaxed mb-4">
                Osobné údaje registrovaných užívateľov (e-mail, meno, fakturačné údaje) spracúvame 
                na základe <strong>súhlasu</strong> a <strong>výkonu zmluvy</strong> (poskytovanie služby).
              </p>
              <p className="text-slate-700 leading-relaxed">
                <strong>Účel spracovania:</strong> Poskytovanie služby, fakturácia, komunikácia, 
                technická podpora.
              </p>

              <h3 className="text-xl font-semibold text-slate-800 mb-3 mt-6">2.2. Subjekty v dátach (Osoby v grafoch)</h3>
              <p className="text-slate-700 leading-relaxed mb-4">
                ILUMINATE SYSTEM zobrazuje osobné údaje osôb (mená, adresy, funkcie v spoločnostiach), ktoré sú 
                <strong> verejne dostupné</strong> v obchodných registroch krajín V4. Tieto osoby 
                sa <strong>neregistrujú</strong> na Platforme, ale ich údaje sa zobrazujú v grafoch.
              </p>
              <p className="text-slate-700 leading-relaxed">
                <strong>Právny základ:</strong> <strong>Oprávnený záujem (Legitimate Interest)</strong> 
                podľa čl. 6(1)(f) GDPR.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">3. Právny základ pre "scrapované osoby"</h2>
              <div className="bg-blue-50 border-l-4 border-blue-400 p-4 mb-4">
                <p className="text-blue-800 font-semibold mb-2">
                  Argumentácia pre Oprávnený záujem:
                </p>
                <ul className="list-disc list-inside text-blue-700 space-y-1 ml-4">
                  <li>Spracúvanie verejne dostupných údajov z obchodných registrov</li>
                  <li>Účel: Prevencia podvodov (karusel, DPH podvody)</li>
                  <li>Zvýšenie transparentnosti podnikateľského prostredia</li>
                  <li>Podpora Due Diligence procesov</li>
                  <li>Rizikové riadenie pre malé a stredné podniky</li>
                </ul>
              </div>
              <p className="text-slate-700 leading-relaxed">
                ILUMINATE SYSTEM spracúva tieto údaje, pretože sú <strong>verejne dostupné</strong> a ich 
                zobrazenie slúži <strong>legitímnemu záujmu</strong> na prevencii podvodov a 
                zvýšení transparentnosti. Tieto údaje nie sú získavané tajne, ale z oficiálnych 
                zdrojov, ktoré sú prístupné každému.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">4. Práva dotknutých osôb</h2>
              <p className="text-slate-700 leading-relaxed mb-4">
                Každá osoba, ktorej údaje spracúvame, má nasledovné práva:
              </p>
              <ul className="list-disc list-inside text-slate-700 space-y-2 ml-4">
                <li><strong>Právo na prístup:</strong> Môžete požiadať o informácie, aké údaje o vás spracúvame.</li>
                <li><strong>Právo na opravu:</strong> Môžete požiadať o opravu nepresných údajov.</li>
                <li><strong>Právo na výmaz:</strong> Môžete požiadať o výmaz údajov (pozri nižšie).</li>
                <li><strong>Právo na námietku:</strong> Môžete namietať proti spracovaniu na základe oprávneného záujmu.</li>
                <li><strong>Právo na obmedzenie spracovania:</strong> Môžete požiadať o dočasné pozastavenie spracovania.</li>
                <li><strong>Právo na prenosnosť:</strong> Môžete požiadať o export vašich údajov.</li>
              </ul>

              <div className="bg-amber-50 border-l-4 border-amber-400 p-4 mt-4">
                <p className="text-amber-800 text-sm mb-3">
                  <strong>Dôležité pre osoby v grafoch:</strong> Ak sa vaše meno zobrazuje v grafe 
                  a chcete byť vymazaný, kontaktujte nás na{" "}
                  <a href="mailto:privacy@crossbordernexus.com" className="underline font-semibold">
                    privacy@crossbordernexus.com
                  </a>
                  . Každú žiadosť posúdime individuálne.
                </p>
                <div className="bg-white p-3 rounded mt-3">
                  <p className="text-amber-900 font-semibold text-xs mb-2">Postup pri žiadosti o výmaz:</p>
                  <ol className="list-decimal list-inside text-amber-800 text-xs space-y-1 ml-2">
                    <li>Pošlite e-mail na privacy@crossbordernexus.com s predmetom "Žiadosť o výmaz údajov"</li>
                    <li>Uveďte vaše meno, dátum narodenia a IČO spoločnosti, kde sa zobrazujete</li>
                    <li>Uveďte dôvod žiadosti (voliteľné, ale pomôže pri posúdení)</li>
                    <li>Odozveme sa do 30 dní a posúdime vašu žiadosť</li>
                    <li>Ak žiadosť schválime, údaje vymažeme do 7 dní</li>
                  </ol>
                  <p className="text-amber-800 text-xs mt-2 italic">
                    Poznámka: Vzhľadom na to, že údaje sú verejne dostupné v obchodných registroch, 
                    výmaz z ILUMINATI SYSTEM nezabráni ich zobrazeniu v pôvodných registroch. 
                    Pre úplné odstránenie kontaktujte príslušný obchodný register.
                  </p>
                </div>
              </div>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">5. Doba uchovávania</h2>
              <ul className="list-disc list-inside text-slate-700 space-y-2 ml-4">
                <li><strong>Registrovaní užívatelia:</strong> Údaje sa uchovávajú počas trvania účtu a 3 roky po jeho zrušení (kvôli daňovým povinnostiam).</li>
                <li><strong>Osoby v dátach:</strong> Údaje sa uchovávajú počas trvania zverejnenia v zdrojovom registri. Ak sa údaj odstráni z oficiálneho registra, odstránime ho aj z ILUMINATE SYSTEM do 30 dní.</li>
                <li><strong>Cache dát:</strong> Dáta z externých API sa cachujú s TTL 24 hodín pre optimalizáciu výkonu.</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">6. Zdieľanie údajov s tretími stranami</h2>
              <p className="text-slate-700 leading-relaxed mb-4">
                ILUMINATE SYSTEM nezdieľa osobné údaje s tretími stranami, okrem:
              </p>
              <ul className="list-disc list-inside text-slate-700 space-y-2 ml-4">
                <li><strong>Poskytovatelia cloudových služieb:</strong> Hosting, databázy (napr. AWS, Azure) - na základe zmlúv o spracovaní údajov.</li>
                <li><strong>Platobné brány:</strong> Stripe, PayPal (len pre fakturačné údaje registrovaných užívateľov).</li>
                <li><strong>Analytické nástroje:</strong> Google Analytics (anonymizované údaje).</li>
                <li><strong>Právne povinnosti:</strong> Ak to vyžaduje zákon alebo súdny príkaz.</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">7. Bezpečnosť</h2>
              <p className="text-slate-700 leading-relaxed">
                ILUMINATE SYSTEM používa moderné bezpečnostné opatrenia: šifrovanie dát v prenose (HTTPS), 
                šifrovanie v pokoji, pravidelné bezpečnostné audity, prístup len pre autorizovaný personál.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">8. Kontakt pre ochranu údajov</h2>
              <p className="text-slate-700 leading-relaxed">
                Pre otázky týkajúce sa ochrany osobných údajov, výmazu údajov alebo námietok kontaktujte:
              </p>
              <div className="bg-slate-50 p-4 rounded-lg mt-4">
                <p className="font-semibold text-slate-900">E-mail:</p>
                <a href="mailto:privacy@crossbordernexus.com" className="text-blue-600 hover:underline">
                  privacy@crossbordernexus.com
                </a>
                <p className="font-semibold text-slate-900 mt-4">Adresa:</p>
                <p className="text-slate-700">[Názov s.r.o.]<br />[Adresa]<br />[PSČ, Mesto]</p>
              </div>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">9. Zmeny v týchto zásadách</h2>
              <p className="text-slate-700 leading-relaxed">
                Tieto zásady môžeme meniť. O zmene budeme informovať registrovaných užívateľov 
                e-mailom a zverejníme novú verziu na tejto stránke.
              </p>
            </section>
          </div>
        </div>
      </div>
    </div>
    </>
  );
};

export default PrivacyPolicy;

