import React from 'react';
import { Check, X, HelpCircle, AlertCircle } from 'lucide-react';

const ComparisonSection = () => {
    return (
        <section className="py-24 bg-white relative overflow-hidden">
            {/* Decorative background elements */}
            <div className="absolute top-0 right-0 w-1/3 h-full bg-slate-50 skew-x-12 transform origin-top-right -z-10" />
            <div className="absolute bottom-0 left-0 w-64 h-64 bg-blue-50 rounded-full blur-3xl opacity-60 -z-10" />

            <div className="max-w-7xl mx-auto px-6">
                <div className="text-center mb-16">
                    <h2 className="text-4xl font-bold text-slate-900 mb-4 font-heading">
                        Prečo platiť viac za menej dát?
                    </h2>
                    <p className="text-xl text-slate-600 max-w-2xl mx-auto">
                        ILUMINATI SYSTEM prináša revolúciu v pomere cena/výkon.
                        Pozrite sa, ako stojíme proti konkurencii.
                    </p>
                </div>

                <div className="overflow-x-auto">
                    <table className="w-full min-w-[800px] border-collapse">
                        <thead>
                            <tr>
                                <th className="p-6 text-left w-1/4">
                                    <span className="text-sm font-semibold text-slate-400 uppercase tracking-wider">Funkcionalita</span>
                                </th>
                                <th className="p-6 w-1/5 text-center bg-slate-50 rounded-t-xl border border-slate-200 opacity-70 grayscale">
                                    <div className="font-bold text-slate-600 mb-1">FinStat</div>
                                    <div className="text-xs text-slate-400">Premium</div>
                                </th>
                                <th className="p-6 w-1/5 text-center bg-slate-50 rounded-t-xl border border-slate-200 opacity-70 grayscale">
                                    <div className="font-bold text-slate-600 mb-1">Index Podnikateľa</div>
                                    <div className="text-xs text-slate-400">Standard</div>
                                </th>
                                <th className="p-6 w-1/4 text-center bg-[#0A0A0A] rounded-t-xl relative transform scale-105 shadow-2xl border-t-4 border-[#D4AF37]">
                                    <div className="absolute -top-4 left-1/2 transform -translate-x-1/2 bg-[#D4AF37] text-[#0A0A0A] px-3 py-1 rounded-full text-xs font-bold shadow-md whitespace-nowrap">
                                        VÍŤAZ TESTU
                                    </div>
                                    <div className="font-bold text-[#D4AF37] text-xl mb-1 mt-2">ILUMINATI</div>
                                    <div className="text-xs text-gray-400">Business</div>
                                </th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100">
                            {/* Row 1: Price */}
                            <tr className="group hover:bg-slate-50 transition-colors">
                                <td className="p-6 text-slate-700 font-medium">Cena ročne</td>
                                <td className="p-6 text-center text-slate-500">~ 300 € +</td>
                                <td className="p-6 text-center text-slate-500">349 €</td>
                                <td className="p-6 text-center bg-[#0A0A0A]/5 border-x-2 border-[#D4AF37]/10 font-bold text-2xl text-green-600">
                                    229 €
                                </td>
                            </tr>

                            {/* Row 2: Region */}
                            <tr className="group hover:bg-slate-50 transition-colors">
                                <td className="p-6 text-slate-700 font-medium flex items-center gap-2">
                                    Pokrytie krajín
                                    <HelpCircle size={14} className="text-slate-400 cursor-help" title="Počet krajín zahrnutých v základnej cene" />
                                </td>
                                <td className="p-6 text-center text-slate-500">Slovensko</td>
                                <td className="p-6 text-center text-slate-500">Slovensko</td>
                                <td className="p-6 text-center bg-[#0A0A0A]/5 border-x-2 border-[#D4AF37]/10 font-bold text-slate-900">
                                    4 krajiny (V4)
                                    <div className="text-xs text-slate-500 font-normal mt-1">SK, CZ, PL, HU</div>
                                </td>
                            </tr>

                            {/* Row 3: Visualization */}
                            <tr className="group hover:bg-slate-50 transition-colors">
                                <td className="p-6 text-slate-700 font-medium">Vizualizácia väzieb</td>
                                <td className="p-6 text-center text-slate-500"><X className="mx-auto text-slate-300" /></td>
                                <td className="p-6 text-center text-slate-500"><X className="mx-auto text-slate-300" /></td>
                                <td className="p-6 text-center bg-[#0A0A0A]/5 border-x-2 border-[#D4AF37]/10">
                                    <div className="flex flex-col items-center justify-center">
                                        <Check className="text-green-600 mb-1" strokeWidth={3} />
                                        <span className="text-xs font-bold text-green-700 bg-green-100 px-2 py-0.5 rounded-full">Graph AI</span>
                                    </div>
                                </td>
                            </tr>

                            {/* Row 4: Updates */}
                            <tr className="group hover:bg-slate-50 transition-colors">
                                <td className="p-6 text-slate-700 font-medium">Aktualizácia dát</td>
                                <td className="p-6 text-center text-slate-500">24h</td>
                                <td className="p-6 text-center text-slate-500">24h</td>
                                <td className="p-6 text-center bg-[#0A0A0A]/5 border-x-2 border-[#D4AF37]/10 text-slate-900 font-semibold">
                                    Real-time / Live
                                </td>
                            </tr>

                            {/* Row 5: Export */}
                            <tr className="group hover:bg-slate-50 transition-colors">
                                <td className="p-6 text-slate-700 font-medium">Hromadný export</td>
                                <td className="p-6 text-center text-slate-500">Limitovaný</td>
                                <td className="p-6 text-center text-slate-500">Excel</td>
                                <td className="p-6 text-center bg-[#0A0A0A]/5 border-x-2 border-[#D4AF37]/10 border-b-2 border-b-[#0A0A0A]/10 text-slate-900 font-semibold rounded-b-xl">
                                    Excel, CSV, JSON, PDF
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div className="mt-8 text-center text-sm text-slate-400 italic">
                    * Ceny a funkcie konkurencie sú založené na verejne dostupných informáciách k 1.1.2025 a môžu sa líšiť podľa individuálnych ponúk.
                </div>
            </div>
        </section>
    );
};

export default ComparisonSection;
