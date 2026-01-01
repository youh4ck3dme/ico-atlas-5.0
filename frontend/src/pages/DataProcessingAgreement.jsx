import React from 'react';
import { FileCheck, ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';

const DataProcessingAgreement = () => {
  return (
    <div className="min-h-screen bg-slate-50">
      <div className="max-w-4xl mx-auto px-8 py-12">
        <Link to="/" className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 mb-6">
          <ArrowLeft size={18} />
          Späť na hlavnú stránku
        </Link>

        <div className="bg-white rounded-lg shadow-sm p-8">
          <div className="flex items-center gap-3 mb-6">
            <FileCheck className="text-blue-600" size={32} />
            <h1 className="text-3xl font-bold text-slate-900">
              Data Processing Agreement (DPA)
            </h1>
          </div>

          <div className="bg-blue-50 border-l-4 border-blue-400 p-4 mb-8">
            <p className="text-blue-800 font-semibold">
              Tento dokument je určený pre B2B klientov (Enterprise), ktorí nahrajú do ILUMINATE SYSTEM vlastné 
              zoznamy partnerov na preverenie. DPA upravuje vzťah medzi Vami (Kontrolor) a nami 
              (Spracovateľ) v súlade s GDPR čl. 28.
            </p>
          </div>

          <div className="prose prose-slate max-w-none">
            <p className="text-sm text-slate-500 mb-8">
              <strong>Platné od:</strong> December 2024<br />
              <strong>Verzia:</strong> 1.1<br />
              <strong>Prevádzkovateľ (Kontrolor):</strong> [Názov klienta]<br />
              <strong>Spracovateľ:</strong> [Názov s.r.o.], IČO: [IČO]
            </p>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">1. Predmet zmluvy</h2>
              <p className="text-slate-700 leading-relaxed">
                Táto zmluva upravuje podmienky spracovania osobných údajov, ktoré Kontrolor poskytne 
                Spracovateľovi v rámci používania služby ILUMINATE SYSTEM Enterprise API. 
                Spracovateľ sa zaväzuje spracovávať údaje výlučne v súlade s touto zmluvou a GDPR.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">2. Rozsah spracovaných údajov</h2>
              <p className="text-slate-700 leading-relaxed mb-4">
                Spracovateľ spracúva nasledovné kategórie osobných údajov poskytnuté Kontrolorom:
              </p>
              <ul className="list-disc list-inside text-slate-700 space-y-2 ml-4">
                <li>Meno a priezvisko osôb (konatelia, spoločníci)</li>
                <li>IČO/DIČ spoločností</li>
                <li>Adresy sídiel</li>
                <li>Iné údaje potrebné pre analýzu rizík (len ak poskytnuté Kontrolorom)</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">3. Účel a spôsob spracovania</h2>
              <p className="text-slate-700 leading-relaxed mb-4">
                <strong>Účel:</strong> Poskytovanie služby Business Intelligence - analýza rizík, 
                identifikácia vzťahov, prevencia podvodov.
              </p>
              <p className="text-slate-700 leading-relaxed mb-4">
                <strong>Spôsob:</strong> Automatizované spracovanie cez API, agregácia s verejne 
                dostupnými dátami z obchodných registrov, generovanie reportov.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">4. Povinnosti Spracovateľa</h2>
              <p className="text-slate-700 leading-relaxed mb-4">
                Spracovateľ sa zaväzuje:
              </p>
              <ul className="list-disc list-inside text-slate-700 space-y-2 ml-4">
                <li>Spracovávať údaje len v súlade s inštrukciami Kontrolora a touto zmluvou</li>
                <li>Zabezpečiť technické a organizačné opatrenia na ochranu údajov</li>
                <li>Nezdieľať údaje s tretími stranami bez súhlasu Kontrolora (okrem právnych povinností)</li>
                <li>Informovať Kontrolora o každom porušení bezpečnosti do 72 hodín</li>
                <li>Umožniť Kontrolorovi audit spracovania</li>
                <li>Po ukončení zmluvy vymazať alebo vrátiť všetky údaje</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">5. Zabezpečenie údajov</h2>
              <p className="text-slate-700 leading-relaxed mb-4">
                Spracovateľ používa nasledovné bezpečnostné opatrenia:
              </p>
              <ul className="list-disc list-inside text-slate-700 space-y-2 ml-4">
                <li>Šifrovanie dát v prenose (HTTPS/TLS 1.3)</li>
                <li>Šifrovanie dát v pokoji (AES-256)</li>
                <li>Prístup len pre autorizovaný personál (princíp najmenšieho oprávnenia)</li>
                <li>Pravidelné bezpečnostné audity a penetračné testy</li>
                <li>Zálohovanie dát s možnosťou obnovy</li>
                <li>Monitorovanie a logovanie prístupov</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">6. Zdieľanie s tretími stranami</h2>
              <p className="text-slate-700 leading-relaxed mb-4">
                Spracovateľ môže použiť nasledovných podspracovateľov (sub-processors):
              </p>
              <ul className="list-disc list-inside text-slate-700 space-y-2 ml-4">
                <li><strong>Cloud hosting:</strong> AWS / Azure (len v EÚ regiónoch)</li>
                <li><strong>Databázy:</strong> PostgreSQL / Neo4j (hostované v EÚ)</li>
                <li><strong>Monitoring:</strong> Sentry, Datadog (anonymizované údaje)</li>
              </ul>
              <p className="text-slate-700 leading-relaxed mt-4">
                Spracovateľ informuje Kontrolora o zmene podspracovateľov. Kontrolor má právo 
                namietať proti novému podspracovateľovi do 14 dní.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">7. Práva dotknutých osôb</h2>
              <p className="text-slate-700 leading-relaxed mb-4">
                Spracovateľ pomáha Kontrolorovi plniť povinnosti týkajúce sa práv dotknutých osôb 
                (právo na prístup, výmaz, opravu, prenosnosť). Všetky žiadosti dotknutých osôb 
                sa presmerujú na Kontrolora do 5 pracovných dní.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">8. Doba uchovávania</h2>
              <p className="text-slate-700 leading-relaxed">
                Údaje sa uchovávajú počas trvania zmluvy a 30 dní po jej ukončení (pre možnosť 
                obnovy). Po uplynutí tejto doby sa údaje trvalo vymažú, okrem prípadov, keď zákon 
                vyžaduje dlhšie uchovávanie.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">9. Audit</h2>
              <p className="text-slate-700 leading-relaxed">
                Kontrolor má právo vykonať audit spracovania údajov po predchádzajúcej dohode 
                (min. 14 dní vopred). Audit sa môže vykonať najviac raz ročne, okrem prípadov 
                podozrenia na porušenie. Náklady na audit hradí Kontrolor.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">10. Ukončenie zmluvy</h2>
              <p className="text-slate-700 leading-relaxed">
                Po ukončení zmluvy Spracovateľ vymaže alebo vráti všetky údaje Kontrolorovi do 
                30 dní. Vymazanie sa potvrdí písomne. Spracovateľ si môže ponechať anonymizované 
                štatistiky, ktoré neumožňujú identifikáciu osôb.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">11. Zodpovednosť</h2>
              <p className="text-slate-700 leading-relaxed">
                Spracovateľ zodpovedá za škody vzniknuté porušením tejto zmluvy alebo GDPR. 
                Zodpovednosť je obmedzená na priame škody do výšky ročného predplatného.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">12. Kontakt</h2>
              <p className="text-slate-700 leading-relaxed">
                Pre otázky týkajúce sa DPA kontaktujte:{" "}
                <a href="mailto:dpa@crossbordernexus.com" className="text-blue-600 hover:underline">
                  dpa@crossbordernexus.com
                </a>
              </p>
            </section>

            <div className="bg-slate-100 p-6 rounded-lg mt-8">
              <p className="text-slate-700 font-semibold mb-2">
                Pre Enterprise klientov:
              </p>
              <p className="text-slate-600 text-sm">
                Tento DPA je súčasťou Enterprise zmluvy. Pre individuálne upravenie podmienok 
                kontaktujte náš obchodný tím na{" "}
                <a href="mailto:sales@crossbordernexus.com" className="text-blue-600 hover:underline">
                  sales@crossbordernexus.com
                </a>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DataProcessingAgreement;

