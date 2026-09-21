import React, { useEffect, useRef } from 'react';
import { Search, ExternalLink, Copy, Network, ShieldAlert } from 'lucide-react';

const GraphContextMenu = ({ x, y, node, onClose }) => {
    const menuRef = useRef(null);

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (menuRef.current && !menuRef.current.contains(event.target)) {
                onClose();
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, [onClose]);

    if (!node) return null;

    const googleSearch = () => {
        window.open(`https://www.google.com/search?q=${encodeURIComponent(node.label + ' ' + (node.ico || ''))}`, '_blank');
        onClose();
    };

    const finstatSearch = () => {
        // Example distinct search
        window.open(`https://finstat.sk/${encodeURIComponent(node.label)}`, '_blank');
        onClose();
    }

    return (
        <div
            ref={menuRef}
            className="fixed z-50 w-56 bg-slate-900/95 backdrop-blur-xl border border-white/10 rounded-lg shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-100"
            style={{ top: y, left: x }}
        >
            <div className="px-3 py-2 border-b border-white/5 bg-white/5">
                <div className="text-xs font-bold text-slate-300 truncate">{node.label}</div>
                <div className="text-[10px] text-slate-500 font-mono uppercase">{node.type} • {node.id}</div>
            </div>

            <div className="p-1">
                <button
                    onClick={googleSearch}
                    className="w-full text-left px-2 py-1.5 text-sm text-slate-300 hover:bg-blue-600 hover:text-white rounded flex items-center gap-2 transition-colors"
                >
                    <Search size={14} />
                    Google Intelligence
                </button>

                <button
                    onClick={finstatSearch}
                    className="w-full text-left px-2 py-1.5 text-sm text-slate-300 hover:bg-emerald-600 hover:text-white rounded flex items-center gap-2 transition-colors"
                >
                    <ExternalLink size={14} />
                    Open Source Check
                </button>

                <div className="h-px bg-white/10 my-1"></div>

                <button className="w-full text-left px-2 py-1.5 text-sm text-slate-300 hover:bg-amber-600 hover:text-white rounded flex items-center gap-2 transition-colors">
                    <Network size={14} />
                    Expand Connections
                </button>

                <button className="w-full text-left px-2 py-1.5 text-sm text-slate-300 hover:bg-slate-700 hover:text-white rounded flex items-center gap-2 transition-colors">
                    <Copy size={14} />
                    Copy ID
                </button>

                {node.risk_score > 5 && (
                    <>
                        <div className="h-px bg-white/10 my-1"></div>
                        <button className="w-full text-left px-2 py-1.5 text-sm text-red-400 hover:bg-red-900/50 hover:text-red-200 rounded flex items-center gap-2 transition-colors">
                            <ShieldAlert size={14} />
                            Flag as High Risk
                        </button>
                    </>
                )}
            </div>
        </div>
    );
};

export default GraphContextMenu;
