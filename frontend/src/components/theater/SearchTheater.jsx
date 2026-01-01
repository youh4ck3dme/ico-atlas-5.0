import React, { useState, useCallback, useRef, useEffect } from 'react';
import { Search, Loader2, Database, Wifi } from 'lucide-react';
import { useTheater } from '../../contexts/TheaterContext';
import audioManager from '../../utils/AudioManager';
import '../../styles/theater.css';

import { useToast } from '../../contexts/ToastContext';

const SearchTheater = ({ onSearch }) => {
    const { setSearchQuery, setIsSearching, isSearching, setCentralNode, setGraphData } = useTheater();
    const { addToast } = useToast();
    const [inputValue, setInputValue] = useState('');
    const [showLoadingOverlay, setShowLoadingOverlay] = useState(false);
    const [loadingText, setLoadingText] = useState('Pripájam sa k databáze...');
    const inputRef = useRef(null);

    // Loading text animation
    useEffect(() => {
        if (!isSearching) return;

        const texts = [
            'Pripájam sa k databáze...',
            'Skenujem registre SR, CZ, PL, HU...',
            'Analyzujem vlastnícke štruktúry...',
            'Mapujem firemné vzťahy...',
            'Generujem pavučinu vzťahov...'
        ];

        let index = 0;
        const interval = setInterval(() => {
            index = (index + 1) % texts.length;
            setLoadingText(texts[index]);
            audioManager.playBeep();
        }, 1200);

        return () => clearInterval(interval);
    }, [isSearching]);

    const handleInputChange = (e) => {
        const value = e.target.value;
        setInputValue(value);

        // Subtle beep on typing (throttled)
        if (value.length % 3 === 0 && value.length > 0) {
            audioManager.playClick();
        }
    };

    const handleSubmit = useCallback(async (e) => {
        e.preventDefault();

        if (!inputValue.trim() || isSearching) return;

        // Set searching state
        setIsSearching(true);
        setSearchQuery(inputValue.trim());
        setShowLoadingOverlay(true);

        // Play search initiation sound
        audioManager.playServerHum();

        try {
            // Call the search callback
            if (onSearch) {
                const result = await onSearch(inputValue.trim());

                if (result && result.nodes && result.nodes.length > 0) {
                    // Set central node (first company node or first node)
                    const centralNode = result.nodes.find(n => n.type === 'company') || result.nodes[0];
                    setCentralNode(centralNode);
                    setGraphData(result);


                    // Success sound
                    audioManager.playPulse();
                } else {
                    // No results found
                    // No results found
                    audioManager.playError();
                    setLoadingText('Nenašli sa žiadne výsledky');
                    addToast('Zadané IČO alebo firma sa nenašla v registroch.', 'error');
                    await new Promise(r => setTimeout(r, 1500));
                }
            }
        } catch (error) {
            console.error('Search error:', error);
            audioManager.playError();
            setLoadingText('Chyba pripojenia');
            addToast('Nepodarilo sa pripojiť k serveru.', 'error');
            await new Promise(r => setTimeout(r, 1500));
        } finally {
            setIsSearching(false);
            setShowLoadingOverlay(false);
        }
    }, [inputValue, isSearching, onSearch, setSearchQuery, setIsSearching, setCentralNode, setGraphData]);

    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            handleSubmit(e);
        }
    };

    return (
        <div className="search-theater">
            <form onSubmit={handleSubmit}>
                <div className="search-input-wrapper">
                    {/* Search Icon */}
                    <div className="search-icon">
                        <Search size={20} />
                    </div>

                    {/* Input */}
                    <input
                        ref={inputRef}
                        type="text"
                        className="search-input"
                        placeholder="Zadajte IČO alebo názov firmy..."
                        value={inputValue}
                        onChange={handleInputChange}
                        onKeyDown={handleKeyDown}
                        disabled={isSearching}
                        autoFocus
                    />

                    {/* Submit Button */}
                    <button
                        type="submit"
                        className="search-button"
                        disabled={isSearching || !inputValue.trim()}
                    >
                        {isSearching ? (
                            <Loader2 size={18} className="animate-spin" />
                        ) : (
                            'HĽADAŤ'
                        )}
                    </button>

                    {/* Loading Overlay */}
                    {showLoadingOverlay && (
                        <div className="search-loading">
                            <div className="flex flex-col items-center gap-4">
                                {/* Animated Database Icon */}
                                <div className="relative">
                                    <Database size={48} className="text-[#D4AF37] animate-pulse" />
                                    <Wifi
                                        size={24}
                                        className="absolute -top-2 -right-2 text-[#60a5fa] animate-ping"
                                    />
                                </div>

                                {/* Loading Text */}
                                <div className="loading-text">
                                    {loadingText}
                                </div>

                                {/* Progress Bar */}
                                <div className="w-48 h-1 bg-gray-700 rounded-full overflow-hidden">
                                    <div
                                        className="h-full bg-gradient-to-r from-[#D4AF37] to-[#FFD700] rounded-full"
                                        style={{
                                            animation: 'progressPulse 2s ease-in-out infinite'
                                        }}
                                    />
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </form>

            {/* Search Tips */}
            <div className="mt-4 flex justify-center gap-6 text-xs text-gray-500 font-mono">
                <span className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-[#D4AF37]" />
                    IČO (8 číslic)
                </span>
                <span className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-[#60a5fa]" />
                    Názov firmy
                </span>
                <span className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-[#34d399]" />
                    Meno osoby
                </span>
            </div>

            <style>{`
        @keyframes progressPulse {
          0% { width: 0%; }
          50% { width: 70%; }
          100% { width: 100%; }
        }
      `}</style>
        </div>
    );
};

export default SearchTheater;
