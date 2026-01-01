import React from 'react';
import { Filter, Link, Users, MapPin, AlertTriangle, RefreshCw } from 'lucide-react';
import { useTheater } from '../../contexts/TheaterContext';
import audioManager from '../../utils/AudioManager';
import '../../styles/theater.css';

// Country flags
const countries = [
    { code: 'SK', name: 'Slovensko', flag: '🇸🇰' },
    { code: 'CZ', name: 'Česko', flag: '🇨🇿' },
    { code: 'PL', name: 'Poľsko', flag: '🇵🇱' },
    { code: 'HU', name: 'Maďarsko', flag: '🇭🇺' }
];

const FilterPanel = () => {
    const { filters, updateFilter, resetFilters } = useTheater();

    const handleToggle = (key) => {
        updateFilter(key, !filters[key]);
        audioManager.playClick();
    };

    const handleCountryToggle = (countryCode) => {
        const currentCountries = filters.countries || [];
        const newCountries = currentCountries.includes(countryCode)
            ? currentCountries.filter(c => c !== countryCode)
            : [...currentCountries, countryCode];

        updateFilter('countries', newCountries);
        audioManager.playClick();
    };

    const handleRiskChange = (e) => {
        const value = parseInt(e.target.value, 10);
        updateFilter('riskScoreMin', value);
    };

    const handleReset = () => {
        resetFilters();
        audioManager.playBeep();
    };

    return (
        <div className="filter-panel">
            <div className="flex justify-between items-center mb-4">
                <h3 className="filter-title flex items-center gap-2">
                    <Filter size={16} />
                    Filtre
                </h3>
                <button
                    onClick={handleReset}
                    className="p-2 text-[#D4AF37] hover:bg-[#D4AF37]/20 rounded-lg transition-all"
                    title="Resetovať filtre"
                >
                    <RefreshCw size={16} />
                </button>
            </div>

            {/* Relationship Types */}
            <div className="filter-group">
                <label className="filter-label">Typy vzťahov</label>
                <div className="filter-toggles">
                    <button
                        className={`filter-toggle ${filters.showOwnership ? 'active' : ''}`}
                        onClick={() => handleToggle('showOwnership')}
                    >
                        <Link size={14} />
                        <span>Vlastníctvo</span>
                    </button>
                    <button
                        className={`filter-toggle ${filters.showManagement ? 'active' : ''}`}
                        onClick={() => handleToggle('showManagement')}
                    >
                        <Users size={14} />
                        <span>Vedenie</span>
                    </button>
                    <button
                        className={`filter-toggle ${filters.showLocation ? 'active' : ''}`}
                        onClick={() => handleToggle('showLocation')}
                    >
                        <MapPin size={14} />
                        <span>Sídlo</span>
                    </button>
                    <button
                        className={`filter-toggle ${filters.showDebts ? 'active' : ''}`}
                        onClick={() => handleToggle('showDebts')}
                        style={{
                            borderColor: filters.showDebts ? '#ef4444' : undefined,
                            color: filters.showDebts ? '#ef4444' : undefined,
                            background: filters.showDebts ? 'rgba(239, 68, 68, 0.2)' : undefined
                        }}
                    >
                        <AlertTriangle size={14} />
                        <span>Dlhy</span>
                    </button>
                </div>
            </div>

            {/* Countries */}
            <div className="filter-group">
                <label className="filter-label">Krajiny</label>
                <div className="filter-toggles">
                    {countries.map(country => (
                        <button
                            key={country.code}
                            className={`filter-toggle ${(filters.countries || []).includes(country.code) ? 'active' : ''}`}
                            onClick={() => handleCountryToggle(country.code)}
                        >
                            <span>{country.flag}</span>
                            <span>{country.code}</span>
                        </button>
                    ))}
                </div>
            </div>

            {/* Risk Score */}
            <div className="filter-group">
                <label className="filter-label">
                    Minimálne rizikové skóre: {filters.riskScoreMin || 0}
                </label>
                <input
                    type="range"
                    className="filter-slider"
                    min="0"
                    max="10"
                    value={filters.riskScoreMin || 0}
                    onChange={handleRiskChange}
                />
                <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>0 (nízke)</span>
                    <span>5</span>
                    <span>10 (vysoké)</span>
                </div>
            </div>

            {/* Active Filters Summary */}
            <div className="mt-4 pt-4 border-t border-[#D4AF37]/20">
                <div className="text-xs text-gray-500 font-mono">
                    <span className="text-[#D4AF37]">Aktívne filtre: </span>
                    {[
                        filters.showOwnership && 'Vlastníctvo',
                        filters.showManagement && 'Vedenie',
                        filters.showLocation && 'Sídlo',
                        filters.showDebts && 'Dlhy',
                        ...(filters.countries || [])
                    ].filter(Boolean).join(' · ') || 'Žiadne'}
                </div>
            </div>
        </div>
    );
};

export default FilterPanel;
