import React, { useState } from 'react';
import { Layers, Building2, User, AlertTriangle, ChevronDown, ChevronUp, Filter, Eye, EyeOff, Calendar } from 'lucide-react';

const GraphControls = ({ filters, onFilterChange }) => {
    const [isOpen, setIsOpen] = useState(false);

    const toggleType = (type) => {
        onFilterChange({ ...filters, [type]: !filters[type] });
    };

    return (
        <div className={`absolute left-4 transition-all duration-300 z-20
            bottom-20 md:bottom-8
            flex flex-col gap-4
        `}>
            {/* Mobile Toggle FAB */}
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="md:hidden absolute bottom-0 left-0 w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center text-white shadow-lg shadow-blue-600/50 z-30 transition-transform active:scale-95"
            >
                <Filter size={20} />
            </button>

            {/* Panel Content Wrapper */}
            <div className={`
                flex flex-col gap-4 origin-bottom-left transition-all duration-300
                ${isOpen ? 'opacity-100 scale-100 mb-16' : 'opacity-0 scale-95 pointer-events-none mb-0'}
                md:opacity-100 md:scale-100 md:pointer-events-auto md:mb-0
            `}>

                {/* Timeline Slider */}
                <div className="bg-slate-900/80 backdrop-blur-md border border-white/10 rounded-xl p-3 w-64 md:w-80 shadow-2xl">
                    <div className="flex justify-between items-center mb-2 px-1">
                        <div className="flex items-center gap-2 text-xs font-mono text-amber-500">
                            <Calendar size={12} />
                            <span>TIMELINE: LIVE</span>
                        </div>
                        <span className="text-[10px] text-slate-500">2020 - 2026</span>
                    </div>
                    <div className="relative h-2 bg-slate-800 rounded-full cursor-pointer group">
                        <div className="absolute top-0 left-0 bottom-0 w-[40%] bg-amber-500/50 rounded-full"></div>
                        <div className="absolute top-1/2 left-[40%] w-3 h-3 bg-white rounded-full -translate-y-1/2 shadow-lg group-hover:scale-125 transition-transform"></div>
                    </div>
                </div>

                {/* Filter Pills */}
                <div className="bg-slate-900/80 backdrop-blur-md border border-white/10 rounded-lg p-2 shadow-xl flex flex-col md:flex-row gap-2">
                    <button
                        onClick={() => toggleType('showCompanies')}
                        className={`px-3 py-1.5 rounded-md text-xs font-bold transition-all flex items-center gap-2 justify-between md:justify-start ${filters.showCompanies ? 'bg-amber-500/20 text-amber-500 border border-amber-500/30' : 'text-slate-500 hover:text-slate-300'}`}
                    >
                        <div className="flex items-center gap-2">
                            {filters.showCompanies ? <Eye size={12} /> : <EyeOff size={12} />}
                            <span>COMPANIES</span>
                        </div>
                    </button>

                    <button
                        onClick={() => toggleType('showPeople')}
                        className={`px-3 py-1.5 rounded-md text-xs font-bold transition-all flex items-center gap-2 justify-between md:justify-start ${filters.showPeople ? 'bg-blue-500/20 text-blue-500 border border-blue-500/30' : 'text-slate-500 hover:text-slate-300'}`}
                    >
                        <div className="flex items-center gap-2">
                            {filters.showPeople ? <Eye size={12} /> : <EyeOff size={12} />}
                            <span>PEOPLE</span>
                        </div>
                    </button>

                    <button
                        onClick={() => toggleType('showRisks')}
                        className={`px-3 py-1.5 rounded-md text-xs font-bold transition-all flex items-center gap-2 justify-between md:justify-start ${filters.showRisks ? 'bg-red-500/20 text-red-500 border border-red-500/30' : 'text-slate-500 hover:text-slate-300'}`}
                    >
                        <div className="flex items-center gap-2">
                            {filters.showRisks ? <Eye size={12} /> : <EyeOff size={12} />}
                            <span>RISKS</span>
                        </div>
                    </button>
                </div>

            </div>
        </div>
    );
};

export default GraphControls;
