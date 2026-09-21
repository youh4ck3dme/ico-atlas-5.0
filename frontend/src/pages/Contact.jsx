import React, { useState } from 'react';
import { Mail, Phone, MapPin, Send, MessageSquare, ArrowLeft, CheckCircle, AlertCircle } from 'lucide-react';
import { Link } from 'react-router-dom';
import SEOHead from '../components/SEOHead';

const Contact = () => {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        subject: '',
        message: ''
    });
    const [status, setStatus] = useState('idle'); // idle | submitting | success | error

    const handleSubmit = async (e) => {
        e.preventDefault();
        setStatus('submitting');

        // Simulate API call
        setTimeout(() => {
            setStatus('success');
            setFormData({ name: '', email: '', subject: '', message: '' });
        }, 1500);
    };

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    return (
        <>
            <SEOHead
                title="Kontakt | ILUMINATI SYSTEM"
                description="Kontaktujte tím ILUMINATI SYSTEM. Podpora, obchodné oddelenie a technické informácie."
            />
            <div className="min-h-screen bg-slate-50">
                <main className="max-w-6xl mx-auto px-6 py-12">
                    <Link to="/" className="inline-flex items-center gap-2 text-slovak-blue hover:text-blue-700 mb-8 transition-colors font-medium">
                        <ArrowLeft size={18} />
                        Späť na hlavnú stránku
                    </Link>

                    <div className="grid lg:grid-cols-2 gap-12">
                        {/* Contact Info */}
                        <div>
                            <h1 className="text-4xl font-bold text-slate-900 mb-6 font-heading">
                                Ozvite sa nám
                            </h1>
                            <p className="text-slate-600 text-lg mb-12 leading-relaxed">
                                Máte otázky k našim službám, cenám alebo potrebujete technickú pomoc?
                                Náš tím je tu pre vás.
                            </p>

                            <div className="space-y-8">
                                <ContactMethod
                                    icon={<Mail className="text-slovak-blue" size={24} />}
                                    title="Emailová podpora"
                                    value="info@icoatlas.sk"
                                    desc="Odpovedáme do 24 hodín"
                                    isLink={true}
                                    href="mailto:info@icoatlas.sk"
                                />
                                <ContactMethod
                                    icon={<Phone className="text-green-600" size={24} />}
                                    title="Obchodné oddelenie"
                                    value="+421 2 123 45 678"
                                    desc="Po-Pia: 9:00 - 17:00"
                                    isLink={true}
                                    href="tel:+421212345678"
                                />
                                <ContactMethod
                                    icon={<MapPin className="text-slovak-red" size={24} />}
                                    title="Sídlo spoločnosti"
                                    value="Cross-Border Nexus s.r.o."
                                    desc={<span>Mlynské Nivy 16<br />821 09 Bratislava<br />Slovenská republika</span>}
                                    isLink={false}
                                />
                            </div>

                            {/* FAQ Teaser */}
                            <div className="mt-12 bg-white p-6 rounded-xl border border-slate-200">
                                <div className="flex items-start gap-4">
                                    <div className="bg-blue-100 p-3 rounded-lg">
                                        <MessageSquare className="text-slovak-blue" size={24} />
                                    </div>
                                    <div>
                                        <h3 className="font-bold text-slate-900 mb-1">Často kladené otázky</h3>
                                        <p className="text-slate-600 text-sm mb-3">
                                            Rýchle odpovede na najčastejšie otázky o službe.
                                        </p>
                                        <Link to="/faq" className="text-slovak-blue font-medium hover:underline text-sm">
                                            Prejsť na FAQ →
                                        </Link>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Contact Form */}
                        <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-8">
                            <h2 className="text-2xl font-bold text-slate-900 mb-6">Napíšte nám správu</h2>

                            {status === 'success' ? (
                                <div className="flex flex-col items-center justify-center text-center h-[400px]">
                                    <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mb-4 text-green-600">
                                        <CheckCircle size={32} />
                                    </div>
                                    <h3 className="text-xl font-bold text-slate-900 mb-2">Správa odoslaná!</h3>
                                    <p className="text-slate-600 mb-6">Ďakujeme za vašu správu. Budeme vás kontaktovať čoskoro.</p>
                                    <button
                                        onClick={() => setStatus('idle')}
                                        className="text-slovak-blue font-medium hover:underline"
                                    >
                                        Poslať ďalšiu správu
                                    </button>
                                </div>
                            ) : (
                                <form onSubmit={handleSubmit} className="space-y-6">
                                    <div className="grid md:grid-cols-2 gap-6">
                                        <div>
                                            <label htmlFor="name" className="block text-sm font-medium text-slate-700 mb-2">Meno a priezvisko</label>
                                            <input
                                                type="text"
                                                id="name"
                                                name="name"
                                                required
                                                value={formData.name}
                                                onChange={handleChange}
                                                className="w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                                                placeholder="Jozef Novák"
                                            />
                                        </div>
                                        <div>
                                            <label htmlFor="email" className="block text-sm font-medium text-slate-700 mb-2">E-mail</label>
                                            <input
                                                type="email"
                                                id="email"
                                                name="email"
                                                required
                                                value={formData.email}
                                                onChange={handleChange}
                                                className="w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                                                placeholder="jozef@firma.sk"
                                            />
                                        </div>
                                    </div>

                                    <div>
                                        <label htmlFor="subject" className="block text-sm font-medium text-slate-700 mb-2">Predmet</label>
                                        <select
                                            id="subject"
                                            name="subject"
                                            required
                                            value={formData.subject}
                                            onChange={handleChange}
                                            className="w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                                        >
                                            <option value="">Vyberte predmet...</option>
                                            <option value="sales">Obchod a Cenník</option>
                                            <option value="support">Technická podpora</option>
                                            <option value="api">API a Integrácie</option>
                                            <option value="other">Iné</option>
                                        </select>
                                    </div>

                                    <div>
                                        <label htmlFor="message" className="block text-sm font-medium text-slate-700 mb-2">Správa</label>
                                        <textarea
                                            id="message"
                                            name="message"
                                            rows="5"
                                            required
                                            value={formData.message}
                                            onChange={handleChange}
                                            className="w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                                            placeholder="Napíšte nám, s čím vám môžeme pomôcť..."
                                        ></textarea>
                                    </div>

                                    <button
                                        type="submit"
                                        disabled={status === 'submitting'}
                                        className="w-full bg-slovak-blue hover:bg-blue-700 text-white font-bold py-4 rounded-lg shadow-lg hover:shadow-xl transition-all flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed"
                                    >
                                        {status === 'submitting' ? (
                                            'Odosielam...'
                                        ) : (
                                            <>
                                                Odoslať správu
                                                <Send size={18} />
                                            </>
                                        )}
                                    </button>
                                </form>
                            )}
                        </div>
                    </div>
                </main>
            </div>
        </>
    );
};

const ContactMethod = ({ icon, title, value, desc, isLink, href }) => (
    <div className="flex items-start gap-4">
        <div className="bg-white p-3 rounded-xl shadow-sm border border-slate-100 mt-1">
            {icon}
        </div>
        <div>
            <h3 className="font-bold text-slate-900 text-lg mb-1">{title}</h3>
            {isLink ? (
                <a href={href} className="text-xl text-blue-600 font-semibold hover:underline block mb-1">
                    {value}
                </a>
            ) : (
                <div className="text-xl text-slate-800 font-semibold mb-1">
                    {value}
                </div>
            )}
            <div className="text-slate-500 text-sm">{desc}</div>
        </div>
    </div>
);

export default Contact;
