import React from 'react';
import { AlertTriangle, ExternalLink } from 'lucide-react';

/**
 * Disclaimer komponent - zobrazuje sa pod grafmi, reportmi a analýzami
 * Obsahuje informácie o zdrojoch dát a vylúčení zodpovednosti
 */
const Disclaimer = ({ 
  sources = [], 
  compact = false,
  showFullText = false 
}) => {
  const defaultSources = [
    { name: 'Obchodný register SR (ORSR)', url: 'https://www.orsr.sk' },
    { name: 'Živnostenský register SR (ZRSR)', url: 'https://www.zrsr.sk' },
    { name: 'Register účtovných závierok (RUZ)', url: 'https://www.registeruz.sk' },
    { name: 'ARES (ČR)', url: 'https://wwwinfo.mfcr.cz' },
    { name: 'Finančná správa SR', url: 'https://www.financnasprava.sk' },
  ];

  const displaySources = sources.length > 0 ? sources : defaultSources;

  if (compact) {
    return (
      <div className="p-4 bg-amber-50 dark:bg-amber-900/20 border-l-4 border-amber-400 rounded text-xs">
        <div className="space-y-2">
          <div className="flex items-start gap-2">
            <AlertTriangle className="text-amber-600 dark:text-amber-400 flex-shrink-0 mt-0.5" size={14} />
            <div className="flex-1">
              <p className="text-amber-900 dark:text-amber-200 font-semibold mb-1">
                Dôležité upozornenie
              </p>
              <p className="text-amber-800 dark:text-amber-300 leading-relaxed">
                Dáta majú len informatívny charakter. Poskytovateľ negarantuje správnosť dát. 
                Pre oficiálne informácie použite pôvodné zdroje.
              </p>
            </div>
          </div>
          {displaySources.length > 0 && (
            <div className="mt-2 pl-6">
              <p className="text-amber-900 dark:text-amber-200 font-semibold text-xs mb-1.5">Zdroj dát:</p>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-4 gap-y-1 text-amber-800 dark:text-amber-300">
                {displaySources.map((source, idx) => (
                  <div key={idx} className="text-xs flex items-center gap-1">
                    {source.url ? (
                      <a 
                        href={source.url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="hover:underline inline-flex items-center gap-1"
                      >
                        {source.name}
                        <ExternalLink size={10} />
                      </a>
                    ) : (
                      <span>{source.name}</span>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="mt-6 p-4 bg-amber-50 border-l-4 border-amber-400 rounded-lg">
      <div className="flex items-start gap-3">
        <AlertTriangle className="text-amber-600 flex-shrink-0 mt-0.5" size={20} />
        <div className="flex-1">
          <h4 className="text-amber-900 font-semibold mb-2">
            Vyhlásenie o odmietnutí zodpovednosti
          </h4>
          
          {showFullText ? (
            <div className="text-amber-800 text-sm leading-relaxed space-y-2">
              <p>
                Dáta zobrazené na portáli ILUMINATI SYSTEM sú agregované z verejných zdrojov 
                (Obchodné registre, Finančné správy V4) automatizovaným spôsobom. 
                ILUMINATI SYSTEM nevytvára tieto dáta a nenesie zodpovednosť za ich aktuálnosť, 
                správnosť či úplnosť.
              </p>
              <p>
                Informácie slúžia výhradne na podporu rozhodovania (business intelligence) 
                a nenahrádzajú oficiálne právne úkony alebo úradné výpisy. Rizikové skóre je 
                výsledkom štatistického modelu, nie obvinením z trestnej činnosti.
              </p>
              <p className="font-semibold">
                Poskytovateľ negarantuje správnosť dát. Dáta majú len informatívny charakter.
              </p>
            </div>
          ) : (
            <p className="text-amber-800 text-sm leading-relaxed">
              Dáta majú len informatívny charakter. Poskytovateľ negarantuje správnosť dát. 
              Pre oficiálne informácie použite pôvodné zdroje. Rizikové skóre je výsledkom 
              štatistického modelu, nie právnym obvinením.
            </p>
          )}

          {displaySources.length > 0 && (
            <div className="mt-3 pt-3 border-t border-amber-200">
              <p className="text-amber-900 font-semibold text-sm mb-2 flex items-center gap-2">
                <span>Zdroj dát:</span>
              </p>
              <ul className="space-y-1">
                {displaySources.map((source, idx) => (
                  <li key={idx} className="text-amber-800 text-sm">
                    {source.url ? (
                      <a 
                        href={source.url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="hover:underline inline-flex items-center gap-1"
                      >
                        {source.name}
                        <ExternalLink size={12} />
                      </a>
                    ) : (
                      source.name
                    )}
                  </li>
                ))}
              </ul>
            </div>
          )}

          <div className="mt-3 pt-3 border-t border-amber-200">
            <a 
              href="/disclaimer" 
              className="text-amber-900 hover:text-amber-700 text-sm font-semibold underline"
            >
              Viac informácií o vylúčení zodpovednosti
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Disclaimer;
