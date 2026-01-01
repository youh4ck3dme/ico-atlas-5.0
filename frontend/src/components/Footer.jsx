import React from 'react';
import { Link } from 'react-router-dom';
import { FileText, Shield, Cookie, AlertCircle } from 'lucide-react';
import Logo from './Logo';
import Disclaimer from './Disclaimer';

const Footer = () => {
  return (
    <footer className="bg-[#0A0A0A] border-t-2 border-[#D4AF37]/20 text-[#D4AF37]/80 mt-20 relative">
      <div className="absolute inset-0 bg-gradient-to-t from-[#1a1a2e] to-transparent opacity-30"></div>
      <div className="relative z-10 max-w-6xl mx-auto px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* O projekte */}
          <div>
            <div className="mb-4">
              <Logo size="small" showText={true} />
            </div>
            <p className="text-sm text-gray-400">
              Business Intelligence & Visualization pre V4 región. 
              Demokratizácia prístupu k dátam pre malé a stredné podniky.
            </p>
          </div>

          {/* Právne dokumenty */}
          <div>
            <h4 className="text-[#D4AF37] font-semibold mb-4 flex items-center gap-2">
              <FileText size={18} />
              Právne dokumenty
            </h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/vop" className="hover:text-[#FFD700] transition-colors text-gray-300">
                  Všeobecné obchodné podmienky
                </Link>
              </li>
              <li>
                <Link to="/privacy" className="hover:text-[#FFD700] transition-colors text-gray-300">
                  Zásady ochrany osobných údajov
                </Link>
              </li>
              <li>
                <Link to="/disclaimer" className="hover:text-[#FFD700] transition-colors text-gray-300">
                  Vyhlásenie o odmietnutí zodpovednosti
                </Link>
              </li>
              <li>
                <Link to="/cookies" className="hover:text-[#FFD700] transition-colors text-gray-300">
                  Cookie Policy
                </Link>
              </li>
              <li>
                <Link to="/dpa" className="hover:text-[#FFD700] transition-colors text-gray-300">
                  Data Processing Agreement (B2B)
                </Link>
              </li>
              <li>
                <Link to="/license" className="hover:text-[#FFD700] transition-colors text-gray-300">
                  Open-source licencia
                </Link>
              </li>
            </ul>
          </div>

          {/* Kontakt */}
          <div>
            <h4 className="text-[#D4AF37] font-semibold mb-4 flex items-center gap-2">
              <Shield size={18} />
              Kontakt
            </h4>
            <ul className="space-y-2 text-sm">
              <li>
                <a href="mailto:support@crossbordernexus.com" className="hover:text-[#FFD700] transition-colors text-gray-300">
                  support@crossbordernexus.com
                </a>
              </li>
              <li>
                <a href="mailto:privacy@crossbordernexus.com" className="hover:text-[#FFD700] transition-colors text-gray-300">
                  privacy@crossbordernexus.com
                </a>
              </li>
              <li className="text-gray-400 text-xs">
                Pre otázky týkajúce sa GDPR a ochrany údajov
              </li>
              <li className="text-gray-400 text-xs mt-3">
                Cross-Border Nexus s.r.o.<br/>
                Bratislava, Slovensko
              </li>
            </ul>
          </div>

          {/* Informácie */}
          <div>
            <h4 className="text-[#D4AF37] font-semibold mb-4 flex items-center gap-2">
              <AlertCircle size={18} />
              Dôležité
            </h4>
            <p className="text-sm text-gray-400 mb-3">
              Dáta zobrazené na portáli sú agregované z verejných zdrojov. 
              Slúžia výhradne na podporu rozhodovania a nenahrádzajú oficiálne právne úkony.
            </p>
            <p className="text-xs text-gray-500 italic">
              Poskytovateľ negarantuje správnosť dát. Dáta majú len informatívny charakter.
            </p>
          </div>
        </div>

        {/* Disclaimer s zdrojmi dát */}
        <div className="border-t border-[#D4AF37]/20 mt-8 pt-6">
          <Disclaimer 
            compact={true}
            sources={[
              { name: 'Obchodný register SR (ORSR)', url: 'https://www.orsr.sk' },
              { name: 'Živnostenský register SR (ZRSR)', url: 'https://www.zrsr.sk' },
              { name: 'Register účtovných závierok (RUZ)', url: 'https://www.registeruz.sk' },
              { name: 'ARES (ČR)', url: 'https://wwwinfo.mfcr.cz' },
              { name: 'Finančná správa SR', url: 'https://www.financnasprava.sk' },
            ]}
          />
        </div>

        <div className="border-t border-[#D4AF37]/20 mt-6 pt-6">
          <p className="text-center text-sm text-gray-400 w-full">
            &copy; 2025 Iluminati Corp s.r.o.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

