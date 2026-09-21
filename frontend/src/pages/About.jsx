import React from 'react';
import { ShieldCheck, Database, Globe, Lock, ArrowLeft, Building2, Users, Search, BarChart3 } from 'lucide-react';
import { Link } from 'react-router-dom';
import SEOHead from '../components/SEOHead';
import Logo from '../components/Logo';
import IluminatiLogo from '../components/IluminatiLogo';

const About = () => {
    return (
        <>
            <SEOHead
                title="O projekte | ILUMINATI SYSTEM"
                description="Vízia, misia a technológie za projektom ILUMINATI SYSTEM - centralizovaného registra firiem V4."
            />
            <div className="min-h-screen bg-slate-50">
                {/* Header */}
                <header className="bg-gradient-to-r from-slate-900 to-slate-800 text-white py-16">
                    <div className="max-w-6xl mx-auto px-6">
                        <Link to="/" className="inline-flex items-center gap-2 text-blue-200 hover:text-white mb-8 transition-colors">
                            <ArrowLeft size={18} />
                            Späť na hlavnú stránku
                        </Link>
                        <div className="flex flex-col md:flex-row items-center gap-8">
                            <div className="flex-1">
                                <h1 className="text-4xl md:text-5xl font-bold mb-4 font-heading">
                                    Demokratizácia dát <br />
                                    <span className="text-blue-400">pre bezpečné podnikanie</span>
                                </h1>
                                <p className="text-xl text-blue-100 leading-relaxed max-w-2xl">
                                    ILUMINATI SYSTEM je Business Intelligence platforma novej generácie,
                                    ktorá prináša transparentnosť do obchodných vzťahov v regióne V4
                                    (Slovensko, Česko, Poľsko, Maďarsko).
                                </p>
                            </div>
                            <div className="hidden md:block">
                                <IluminatiLogo size={120} />
                            </div>
                        </div>
                    </div>
                </header>

                <main className="max-w-6xl mx-auto px-6 py-12">
                    {/* Mission Section */}
                    <div className="grid md:grid-cols-2 gap-12 mb-20 items-center">
                        <div>
                            <h2 className="text-3xl font-bold text-slate-900 mb-6">Naša Misia</h2>
                            <p className="text-slate-600 leading-relaxed mb-6 text-lg">
                                Veríme, že prístup k informáciám by nemal byť privilégiom veľkých korporácií.
                                Naším cieľom je poskytnúť malým a stredným podnikateľom rovnaké analytické nástroje,
                                aké používajú banky a nadnárodné spoločnosti.
                            </p>
                            <p className="text-slate-600 leading-relaxed text-lg">
                                Agregujeme dáta z viac ako 15 verejných registrov a pomocou pokročilých algoritmov
                                odhaľujeme skryté väzby, riziká a príležitosti.
                            </p>
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                            <StatCard number="4+" label="Krajiny V4" />
                            <StatCard number="2M+" label="Firiem v databáze" />
                            <StatCard number="15+" label="Dátových zdrojov" />
                            <StatCard number="24/7" label="Dostupnosť" />
                        </div>
                    </div>

                    {/* Features Grid */}
                    <h2 className="text-3xl font-bold text-slate-900 mb-12 text-center">Čo nás odlišuje</h2>
                    <div className="grid md:grid-cols-3 gap-8 mb-20">
                        <FeatureCard
                            icon={<Globe className="text-slovak-blue" size={32} />}
                            title="Cross-border Analýza"
                            description="Ako jediní na trhu efektívne prepájame dáta zo všetkých krajín V4 do jedného grafu väzieb."
                        />
                        <FeatureCard
                            icon={<ShieldCheck className="text-green-600" size={32} />}
                            title="Risk Intelligence"
                            description="Vlastné algoritmy detegujúce daňové podvody, biele kone a rizikové vlastnícke štruktúry."
                        />
                        <FeatureCard
                            icon={<Database className="text-purple-600" size={32} />}
                            title="Technologická Excellencia"
                            description="Moderný stack (React, Python, Go) zabezpečuje bleskovú odozvu a stabilitu aj pri veľkých dátach."
                        />
                    </div>

                    {/* Team/Company Section */}
                    <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-8 md:p-12 mb-12">
                        <h2 className="text-2xl font-bold text-slate-900 mb-6">O Spoločnosti</h2>
                        <div className="prose prose-slate max-w-none">
                            <p className="text-slate-600 mb-4">
                                ILUMINATI SYSTEM prevádzkuje spoločnosť <strong>Cross-Border Nexus s.r.o.</strong>,
                                technologický startup so sídlom v Bratislave. Náš tím tvoria seniorní vývojári,
                                data analytici a experti na forenzný audit.
                            </p>
                            <p className="text-slate-600">
                                Sme hrdí na to, že pomáhame tvoriť transparentnejšie podnikateľské prostredie
                                v strednej Európe.
                            </p>
                        </div>
                    </div>
                </main>
            </div>
        </>
    );
};

const StatCard = ({ number, label }) => (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 text-center hover:shadow-md transition-shadow">
        <div className="text-3xl font-bold text-slovak-blue mb-2">{number}</div>
        <div className="text-sm text-slate-500 font-medium uppercase tracking-wide">{label}</div>
    </div>
);

const FeatureCard = ({ icon, title, description }) => (
    <div className="bg-white p-8 rounded-xl shadow-sm border border-slate-200 hover:-translate-y-1 transition-transform duration-300">
        <div className="bg-slate-50 w-16 h-16 rounded-full flex items-center justify-center mb-6">
            {icon}
        </div>
        <h3 className="text-xl font-bold text-slate-900 mb-3">{title}</h3>
        <p className="text-slate-600 leading-relaxed">
            {description}
        </p>
    </div>
);

export default About;
