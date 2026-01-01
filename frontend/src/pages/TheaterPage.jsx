import React, { useRef, useCallback, useEffect } from 'react';
import { Volume2, VolumeX, Home, Info } from 'lucide-react';
import { TheaterProvider, useTheater } from '../contexts/TheaterContext';
import TheaterOverlay from '../components/theater/TheaterOverlay';
import TheaterGraph from '../components/theater/TheaterGraph';
import NodeCard from '../components/theater/NodeCard';
import SearchTheater from '../components/theater/SearchTheater';
import ExportPanel from '../components/theater/ExportPanel';
import ImportPanel from '../components/theater/ImportPanel';
import FilterPanel from '../components/theater/FilterPanel';
import { IluminateLogo, NetworkIcon } from '../components/theater/PremiumIcons';
import audioManager from '../utils/AudioManager';
import '../styles/theater.css';
import { Link } from 'react-router-dom';

const TheaterPageContent = () => {
    const graphRef = useRef();
    const {
        introComplete,
        isMuted,
        toggleMute,
        setAudioVolume,
        audioVolume
    } = useTheater();

    // Initialize audio on first interaction
    useEffect(() => {
        const handleFirstInteraction = () => {
            audioManager.init();
            document.removeEventListener('click', handleFirstInteraction);
        };
        document.addEventListener('click', handleFirstInteraction);
        return () => document.removeEventListener('click', handleFirstInteraction);
    }, []);

    // Sync mute state
    useEffect(() => {
        audioManager.setMuted(isMuted);
    }, [isMuted]);

    // Handle search with ORSR lookup - REAL DATA ONLY
    const handleSearch = useCallback(async (query) => {
        try {
            // Import ORSR service
            const { lookupByIco, searchCompanies, isValidIco, companyToGraphData } = await import('../services/orsrLookup');

            // Clean query
            const cleanQuery = query.trim().replace(/\s/g, '');

            // Check if query is IČO
            if (isValidIco(cleanQuery)) {
                // Lookup by IČO
                const company = await lookupByIco(cleanQuery);

                if (company) {
                    // Transform to graph data
                    return companyToGraphData(company);
                }
            }

            // Search by name if not IČO
            const searchResult = await searchCompanies(query, ['SK', 'CZ', 'PL', 'HU']);

            if (searchResult && searchResult.companies && searchResult.companies.length > 0) {
                // Use graph data from API if available
                if (searchResult.graphData) {
                    return searchResult.graphData;
                }
                // Otherwise transform first company
                return companyToGraphData(searchResult.companies[0]);
            }

            // No data found - return empty (NO DEMO DATA)
            console.warn('No data found for query:', query);
            return { nodes: [], edges: [] };
        } catch (error) {
            console.error('Search error:', error);
            // Return empty on error (NO DEMO DATA)
            return { nodes: [], edges: [] };
        }
    }, []);

    const handleToggleMute = () => {
        toggleMute();
        audioManager.toggleMute();
        audioManager.playClick();
    };

    const handleVolumeChange = (e) => {
        const value = parseFloat(e.target.value);
        setAudioVolume(value);
        audioManager.setVolume(value);
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-[#0A0A0A] via-[#1a1a2e] to-[#16213e]">
            {/* Theater Intro Overlay */}
            {!introComplete && <TheaterOverlay />}

            {/* Main Content - only visible after intro */}
            {introComplete && (
                <>
                    {/* Header */}
                    <header className="relative z-20 px-6 py-4">
                        <div className="max-w-7xl mx-auto flex justify-between items-center">
                            {/* Logo */}
                            <Link to="/" className="flex items-center gap-3 group">
                                <IluminateLogo size={36} animated={true} />
                                <div>
                                    <h1 className="text-xl font-bold text-[#D4AF37] group-hover:text-[#FFD700] transition-colors">
                                        ILUMINATE
                                    </h1>
                                    <p className="text-xs text-gray-500 font-mono flex items-center gap-1">
                                        <NetworkIcon size={12} animated={false} />
                                        Theater Mode
                                    </p>
                                </div>
                            </Link>

                            {/* Navigation */}
                            <nav className="flex items-center gap-4">
                                <Link
                                    to="/"
                                    className="flex items-center gap-2 px-4 py-2 text-gray-400 hover:text-[#D4AF37] transition-colors font-mono text-sm"
                                    onClick={() => audioManager.playClick()}
                                >
                                    <Home size={16} />
                                    Domov
                                </Link>
                                <button
                                    className="p-2 text-gray-400 hover:text-[#D4AF37] transition-colors"
                                    title="O aplikácii"
                                    onClick={() => audioManager.playClick()}
                                >
                                    <Info size={18} />
                                </button>
                            </nav>
                        </div>
                    </header>

                    {/* Main Content Area */}
                    <main className="max-w-7xl mx-auto px-6 py-8">
                        {/* Search */}
                        <div className="mb-8">
                            <SearchTheater onSearch={handleSearch} />
                        </div>

                        {/* Content Grid */}
                        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
                            {/* Sidebar - Filters & Import */}
                            <aside className="lg:col-span-1 order-2 lg:order-1 flex flex-col gap-6">
                                <ImportPanel />
                                <FilterPanel />
                            </aside>

                            {/* Main Graph Area */}
                            <div className="lg:col-span-3 order-1 lg:order-2">
                                <TheaterGraph ref={graphRef} />

                                {/* Export Panel */}
                                <div className="mt-4">
                                    <ExportPanel graphRef={graphRef} />
                                </div>
                            </div>
                        </div>
                    </main>

                    {/* Node Detail Card */}
                    <NodeCard />

                    {/* Audio Control */}
                    <div className="audio-control">
                        <button
                            className={`audio-button ${isMuted ? 'muted' : ''}`}
                            onClick={handleToggleMute}
                            title={isMuted ? 'Zapnúť zvuk' : 'Vypnúť zvuk'}
                        >
                            {isMuted ? <VolumeX size={18} /> : <Volume2 size={18} />}
                        </button>
                        {!isMuted && (
                            <input
                                type="range"
                                className="audio-slider"
                                min="0"
                                max="1"
                                step="0.1"
                                value={audioVolume}
                                onChange={handleVolumeChange}
                            />
                        )}
                    </div>

                    {/* Footer */}
                    <footer className="text-center py-8 text-gray-600 font-mono text-xs">
                        <p>ILUMINATE SYSTEM © {new Date().getFullYear()} | Všetky práva vyhradené</p>
                        <p className="mt-1">Dáta z verejných registrov SR, CZ, PL, HU</p>
                    </footer>
                </>
            )}
        </div>
    );
};

import { ToastProvider } from '../contexts/ToastContext';
import ToastContainer from '../components/theater/ToastContainer';

// Wrap with TheaterProvider and ToastProvider
const TheaterPage = () => {
    return (
        <ToastProvider>
            <TheaterProvider>
                <TheaterPageContent />
                <ToastContainer />
            </TheaterProvider>
        </ToastProvider>
    );
};

export default TheaterPage;
