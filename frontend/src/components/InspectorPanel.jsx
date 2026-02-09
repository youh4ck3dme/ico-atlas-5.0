import React from 'react';
import { X, Building2, User, MapPin, AlertTriangle, ExternalLink, Calendar, FileText } from 'lucide-react';

const InspectorPanel = ({ selectedNode, onClose }) => {
    if (!selectedNode) return null;

    const { type, label, risk_score, ico, address, details, country } = selectedNode;

    // Helper to get color based on type
    const getTypeColor = (t) => {
        switch (t) {
            case 'company': return 'text-amber-500 border-amber-500/30 bg-amber-500/10';
            case 'person': return 'text-blue-500 border-blue-500/30 bg-blue-500/10';
            case 'address': return 'text-emerald-500 border-emerald-500/30 bg-emerald-500/10';
            case 'debt': return 'text-red-500 border-red-500/30 bg-red-500/10';
            default: return 'text-slate-500 border-slate-500/30 bg-slate-500/10';
        }
    };

    const typeClass = getTypeColor(type);

    return (
        <div className="absolute 
            top-auto right-0 bottom-0 left-0 w-full h-[60vh] rounded-t-2xl border-t
            md:top-20 md:right-4 md:bottom-20 md:left-auto md:w-96 md:h-auto md:max-h-[calc(100vh-140px)] md:rounded-xl md:border
            overflow-y-auto bg-slate-900/80 backdrop-blur-xl border-white/10 shadow-2xl z-30
            animate-in slide-in-from-bottom md:slide-in-from-right duration-300"
        >
            {/* Header */}
            <div className="p-4 border-b border-white/10 flex justify-between items-start sticky top-0 bg-slate-900/90 backdrop-blur-sm z-10">
                <div>
                    <div className={`inline-flex items-center gap-2 px-2 py-1 rounded-md text-xs font-mono uppercase font-bold border ${typeClass.split(' ')[1]} ${typeClass.split(' ')[0]} ${typeClass.split(' ')[2]} mb-2`}>
                        {type === 'company' && <Building2 size={12} />}
                        {type === 'person' && <User size={12} />}
                        {type === 'address' && <MapPin size={12} />}
                        {type === 'debt' && <AlertTriangle size={12} />}
                        {type}
                    </div>
                    <h2 className="text-xl font-bold text-white leading-tight">{label}</h2>
                    {country && <span className="text-xs text-slate-400 font-mono mt-1 block">REGION: {country}</span>}
                </div>
                <button onClick={onClose} className="p-1 hover:bg-white/10 rounded-lg text-slate-400 hover:text-white transition-colors">
                    <X size={20} />
                </button>
            </div>

            {/* Content */}
            <div className="p-4 space-y-6">

                {/* Risk Score Meter */}
                {risk_score > 0 && (
                    <div className="bg-slate-800/50 rounded-lg p-3 border border-white/5">
                        <div className="flex justify-between items-end mb-2">
                            <span className="text-xs text-slate-400 font-mono">RISK SCORE</span>
                            <span className={`text-xl font-bold font-mono ${risk_score > 7 ? 'text-red-500' : risk_score > 4 ? 'text-amber-500' : 'text-emerald-500'}`}>
                                {risk_score}/10
                            </span>
                        </div>
                        <div className="w-full bg-slate-700 h-2 rounded-full overflow-hidden">
                            <div
                                className={`h-full ${risk_score > 7 ? 'bg-red-500' : risk_score > 4 ? 'bg-amber-500' : 'bg-emerald-500'}`}
                                style={{ width: `${(risk_score / 10) * 100}%` }}
                            ></div>
                        </div>
                        <div className="mt-2 text-xs text-slate-400">
                            Subject has elevated risk factors present in public registries.
                        </div>
                    </div>
                )}

                {/* Details Grid */}
                <div className="grid grid-cols-1 gap-4">
                    {ico && (
                        <div className="p-3 bg-white/5 rounded-lg border border-white/5 hover:border-white/10 transition-colors">
                            <label className="text-[10px] uppercase tracking-wider text-slate-500 font-bold block mb-1">Registration ID (IČO)</label>
                            <div className="font-mono text-slate-200 select-all">{ico}</div>
                        </div>
                    )}

                    {address && (
                        <div className="p-3 bg-white/5 rounded-lg border border-white/5 hover:border-white/10 transition-colors">
                            <label className="text-[10px] uppercase tracking-wider text-slate-500 font-bold block mb-1">Registered Address</label>
                            <div className="text-sm text-slate-200 flex items-start gap-2">
                                <MapPin size={14} className="mt-0.5 text-slate-500 shrink-0" />
                                {address}
                            </div>
                        </div>
                    )}

                    {details && (
                        <div className="p-3 bg-white/5 rounded-lg border border-white/5 hover:border-white/10 transition-colors">
                            <label className="text-[10px] uppercase tracking-wider text-slate-500 font-bold block mb-1">Additional Info</label>
                            <div className="text-sm text-slate-300 leading-relaxed">{details}</div>
                        </div>
                    )}
                </div>

                {/* Integration Actions */}
                <div className="flex gap-2 pt-2">
                    <button className="flex-1 bg-blue-600 hover:bg-blue-500 text-white py-2 px-4 rounded-lg text-sm font-bold transition-colors flex items-center justify-center gap-2">
                        <FileText size={16} />
                        Full Report
                    </button>
                    <button className="flex-1 bg-slate-700 hover:bg-slate-600 text-white py-2 px-4 rounded-lg text-sm font-bold transition-colors flex items-center justify-center gap-2">
                        <ExternalLink size={16} />
                        Open Registry
                    </button>
                </div>

                {/* Footer Graph Stats (Fake data for visual) */}
                <div className="pt-4 border-t border-white/5">
                    <div className="text-[10px] uppercase tracking-wider text-slate-500 font-bold mb-2">Network Activity</div>
                    <div className="flex items-end justify-between h-16 gap-1">
                        {[40, 65, 30, 80, 50, 90, 45].map((h, i) => (
                            <div key={i} className="w-full bg-slate-700/50 hover:bg-blue-500/50 transition-colors rounded-sm" style={{ height: `${h}%` }}></div>
                        ))}
                    </div>
                </div>

            </div>
        </div>
    );
};

export default InspectorPanel;
