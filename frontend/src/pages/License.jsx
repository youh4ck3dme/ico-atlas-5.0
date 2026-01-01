import React from 'react';
import IluminatiLogo from '../components/IluminatiLogo';

const License = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-indigo-900 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8">
          <IluminatiLogo className="mx-auto mb-6" />
          <h1 className="text-4xl font-bold text-white mb-4">Licencia</h1>
          <p className="text-blue-200 text-lg">Open-source licencia pre ILUMINATI SYSTEM</p>
        </div>

        <div className="bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-8 border border-white/20">
          <div className="prose prose-invert max-w-none">
            <h2 className="text-2xl font-bold text-white mb-6">MIT License</h2>

            <p className="text-blue-100 mb-6">
              Copyright (c) 2024 Cross-Border Nexus
            </p>

            <p className="text-blue-100 mb-6">
              S oprávnením sa udeľuje bezplatne akejkoľvek osobe, ktorá získa kópiu tohto softvéru a súvisiacich dokumentačných súborov (ďalej len "softvér"), aby s ním nakladala bez obmedzení vrátane, nie však výlučne, práv na používanie, kopírovanie, úpravu, zlúčenie, publikovanie, distribúciu, sublicencovanie a/alebo predaj kópií softvéru, a aby umožnila osobám, ktorým sa softvér poskytuje, aby tak konali za týchto podmienok:
            </p>

            <p className="text-blue-100 mb-6">
              Vyššie uvedené autorské práva a toto oprávnenie sa poskytujú za predpokladu, že vyššie uvedené upozornenie na autorské práva a toto oprávnenie sa zobrazia vo všetkých kópiách alebo podstatných častiach softvéru.
            </p>

            <p className="text-blue-100 mb-8">
              SOFTVÉR SA POSKYTUJE "TAK, AKO JE", BEZ AKEJKOĽVEK ZÁRUKY, VÝSLOVNÝCH ALEBO IMPLICITNÝCH, VRÁTANE, ALE NIE VÝLUČNE, ZÁRUK TÝKAJÚCICH SA OBCHODOVATEĽNOSTI, VHODNOSTI NA URČITÝ ÚČEL A NEPORUŠENIA PRÁV. V ŽIADNOM PRÍPADE NEBUDÚ AUTORI ALEBO DRŽITELIA AUTORSKÝCH PRÁV ZODPOVEDNÍ ZA AKÉKOĽVEK NÁROKY, ŠKODY ALEBO INÉ ZODPOVEDNOSTI, ČI UŽ V SÚVISLOSTI SO ZMLUVOU, DELIKTOM ALEBO INÝM SPÔSOBOM, VYPLÝVAJÚCE Z ALEBO V SÚVISLOSTI S SOFTVÉROM ALEBO POUŽÍVANÍM ALEBO INÝMI KONANÍMI V SOFTVÉRI.
            </p>

            <div className="bg-blue-900/30 rounded-lg p-6 border border-blue-500/30">
              <h3 className="text-xl font-semibold text-blue-200 mb-4">Preklad do angličtiny (originál):</h3>
              <p className="text-blue-100 text-sm italic">
                Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
              </p>
              <p className="text-blue-100 text-sm italic mt-3">
                The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
              </p>
              <p className="text-blue-100 text-sm italic mt-3">
                THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
              </p>
            </div>

            <div className="mt-8 p-6 bg-yellow-900/20 rounded-lg border border-yellow-500/30">
              <h3 className="text-lg font-semibold text-yellow-200 mb-3">Dôležité upozornenie</h3>
              <p className="text-yellow-100 text-sm">
                Táto licencia sa vzťahuje len na open-source komponenty systému ILUMINATI. Niektoré funkcionality môžu využívať externé API služby, ktoré majú vlastné licenčné podmienky. Používateľ je zodpovedný za dodržiavanie všetkých príslušných právnych predpisov pri používaní tohto softvéru.
              </p>
            </div>
          </div>
        </div>

        <div className="text-center mt-8">
          <a
            href="https://github.com/crossbordernexus/iluminati-system"
            className="inline-flex items-center px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-colors"
            target="_blank"
            rel="noopener noreferrer"
          >
            <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 0C4.477 0 0 4.484 0 10.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0110 4.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.203 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.942.359.31.678.921.678 1.856 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0020 10.017C20 4.484 15.522 0 10 0z" clipRule="evenodd" />
            </svg>
            Zobraziť na GitHub
          </a>
        </div>
      </div>
    </div>
  );
};

export default License;