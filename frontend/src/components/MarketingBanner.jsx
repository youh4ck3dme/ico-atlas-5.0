import React, { useState, useEffect } from 'react';
import { X, ArrowRight, Zap } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const MarketingBanner = () => {
    const [isVisible, setIsVisible] = useState(false);
    const [timeLeft, setTimeLeft] = useState(13 * 60 * 60 + 42 * 60 + 15); // Start with some fixed time for demo urgency
    const navigate = useNavigate();

    useEffect(() => {
        // Show banner after 2 seconds
        const timer = setTimeout(() => {
            const hasSeenBanner = sessionStorage.getItem('hasSeenMarketingBanner');
            if (!hasSeenBanner) {
                setIsVisible(true);
            }
        }, 2000);

        // Countdown interval
        const interval = setInterval(() => {
            setTimeLeft((prev) => (prev > 0 ? prev - 1 : 0));
        }, 1000);

        return () => {
            clearTimeout(timer);
            clearInterval(interval);
        };
    }, []);

    const closeBanner = () => {
        setIsVisible(false);
        sessionStorage.setItem('hasSeenMarketingBanner', 'true');
    };

    const formatTime = (seconds) => {
        const h = Math.floor(seconds / 3600);
        const m = Math.floor((seconds % 3600) / 60);
        const s = seconds % 60;
        return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
    };

    if (!isVisible) return null;

    return (
        <div className="fixed bottom-0 left-0 right-0 z-50 animate-in slide-in-from-bottom duration-500">
            {/* Main Gradient Bar */}
            <div className="bg-gradient-to-r from-[#0A0A0A] via-[#1a1a2e] to-[#0A0A0A] border-t-2 border-[#D4AF37] shadow-[0_-10px_40px_rgba(212,175,55,0.2)] p-4 md:p-5">
                <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">

                    {/* Left content with icon */}
                    <div className="flex items-center gap-4 flex-1">
                        <div className="hidden md:flex bg-[#EE1C25] p-3 rounded-full shadow-[0_0_15px_rgba(238,28,37,0.6)] animate-pulse">
                            <Zap className="text-white" size={24} strokeWidth={3} />
                        </div>
                        <div>
                            <div className="flex items-center gap-3 mb-1">
                                <h3 className="text-white text-lg md:text-xl font-bold font-heading">
                                    POZOR: Limitovaná ponuka
                                </h3>
                                <div className="bg-[#EE1C25] text-white text-xs font-bold px-2 py-0.5 rounded animate-bounce">
                                    Končí o {formatTime(timeLeft)}
                                </div>
                            </div>
                            <p className="text-blue-100 text-sm md:text-base leading-tight">
                                Nenechajte si ujsť <span className="text-[#D4AF37] font-bold">4 krajiny za cenu 1</span>.
                                Pridajte sa k <span className="font-bold text-white">500+ lídrom</span> na trhu.
                            </p>
                        </div>
                    </div>

                    {/* Right Action Buttons */}
                    <div className="flex items-center gap-4 w-full md:w-auto">
                        <button
                            onClick={() => navigate('/pricing')}
                            className="flex-1 md:flex-none bg-gradient-to-r from-[#D4AF37] to-[#FFD700] hover:from-[#FFD700] hover:to-[#D4AF37] text-[#0A0A0A] px-6 py-3 rounded-xl font-bold text-sm md:text-base shadow-[0_0_20px_rgba(212,175,55,0.4)] hover:shadow-[0_0_30px_rgba(212,175,55,0.6)] transition-all transform hover:-translate-y-1 flex items-center justify-center gap-2"
                        >
                            Chcem ušetriť
                            <ArrowRight size={18} />
                        </button>
                        <button
                            onClick={closeBanner}
                            className="bg-white/10 hover:bg-white/20 text-white p-3 rounded-xl transition-colors"
                            aria-label="Zavrieť"
                        >
                            <X size={20} />
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default MarketingBanner;
