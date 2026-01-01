import React, { useState } from 'react';
import { Search, Loader2, Building2, User, MapPin, AlertTriangle, Sparkles, Globe, Shield } from 'lucide-react';
import Disclaimer from '../components/Disclaimer';
import Logo from '../components/Logo';
import ForceGraph from '../components/ForceGraph';

// --- JEDNODUCHÝ SVG GRAPH RENDERER (MVP) ---
const SimpleGraph = ({ data }) => {
  if (!data || data.nodes.length === 0) return null;

  // Jednoduchý layout algoritmus: rozmiestni uzly do kruhu
  const centerX = 400;
  const centerY = 300;
  const radius = 200;
  
  const nodesWithPos = data.nodes.map((node, index) => {
    const angle = (index / data.nodes.length) * 2 * Math.PI;
    return {
      ...node,
      x: centerX + radius * Math.cos(angle),
      y: centerY + radius * Math.sin(angle),
    };
  });

  const getNodePos = (id) => nodesWithPos.find(n => n.id === id);

  return (
    <div className="border-2 border-[#D4AF37]/30 rounded-xl bg-gradient-to-br from-[#0A0A0A] via-[#1a1a2e] to-[#16213e] shadow-2xl overflow-hidden mt-6 backdrop-blur-sm">
      <svg width="100%" height="600" viewBox="0 0 800 600" className="w-full">
        {/* Kozmické pozadie */}
        <defs>
          <radialGradient id="cosmicBg" cx="50%" cy="50%">
            <stop offset="0%" stopColor="#1a1a2e" stopOpacity="0.8" />
            <stop offset="100%" stopColor="#0A0A0A" stopOpacity="1" />
          </radialGradient>
          <filter id="glow">
            <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
            <feMerge>
              <feMergeNode in="coloredBlur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
          <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="28" refY="3.5" orient="auto">
            <polygon points="0 0, 10 3.5, 0 7" fill="#D4AF37" opacity="0.6" />
          </marker>
        </defs>

        {/* Kozmické pozadie */}
        <rect width="100%" height="100%" fill="url(#cosmicBg)" />
        
        {/* Hviezdy */}
        {Array.from({ length: 50 }).map((_, i) => (
          <circle
            key={i}
            cx={Math.random() * 800}
            cy={Math.random() * 600}
            r={Math.random() * 1.5}
            fill="#D4AF37"
            opacity={Math.random() * 0.8 + 0.2}
            className="animate-pulse"
            style={{ animationDelay: `${Math.random() * 2}s`, animationDuration: `${Math.random() * 3 + 2}s` }}
          />
        ))}

        {/* HRANY (Edges) */}
        {data.edges.map((edge, i) => {
          const source = getNodePos(edge.source);
          const target = getNodePos(edge.target);
          if (!source || !target) return null;
          return (
            <g key={i}>
              <line 
                x1={source.x} y1={source.y} 
                x2={target.x} y2={target.y} 
                stroke="#D4AF37" 
                strokeWidth="2"
                opacity="0.4"
                markerEnd="url(#arrowhead)"
                className="transition-opacity hover:opacity-80"
              />
              <text 
                x={(source.x + target.x)/2} 
                y={(source.y + target.y)/2} 
                className="text-[9px] fill-[#D4AF37] font-semibold"
                style={{ textShadow: '0 0 4px #D4AF37' }}
              >
                {edge.type}
              </text>
            </g>
          );
        })}

        {/* UZLY (Nodes) */}
        {nodesWithPos.map((node) => (
          <g key={node.id} className="cursor-pointer transition-all hover:scale-110">
            <circle 
              cx={node.x} cy={node.y} r="28" 
              fill={
                node.type === 'company' ? '#D4AF37' : 
                node.type === 'person' ? '#10b981' : 
                node.type === 'address' ? '#f59e0b' :
                node.type === 'debt' ? '#ef4444' : '#6b7280'
              } 
              stroke="#0A0A0A" 
              strokeWidth="3"
              filter="url(#glow)"
              className="drop-shadow-2xl"
              style={{ 
                filter: `drop-shadow(0 0 8px ${node.type === 'company' ? '#D4AF37' : node.type === 'person' ? '#10b981' : node.type === 'address' ? '#f59e0b' : '#ef4444'})`
              }}
            />
            
            {/* Ikona v strede uzla */}
            <foreignObject x={node.x - 14} y={node.y - 14} width="28" height="28">
               <div className="flex items-center justify-center h-full text-[#0A0A0A]">
                 {node.type === 'company' && <Building2 size={18} />}
                 {node.type === 'person' && <User size={18} />}
                 {node.type === 'address' && <MapPin size={18} />}
                 {node.type === 'debt' && <AlertTriangle size={18} />}
               </div>
            </foreignObject>

            {/* Label a Risk Score */}
            <text 
              x={node.x} 
              y={node.y + 45} 
              textAnchor="middle" 
              className="text-xs font-bold fill-[#D4AF37]"
              style={{ textShadow: '0 0 6px #D4AF37' }}
            >
              {node.label.length > 15 ? node.label.substring(0, 15) + '...' : node.label}
            </text>
            
            {node.risk_score > 0 && (
              <text 
                x={node.x + 25} 
                y={node.y - 25} 
                className="text-xs font-bold fill-red-400"
                style={{ textShadow: '0 0 4px #ef4444' }}
              >
                ⚠ {node.risk_score}
              </text>
            )}
          </g>
        ))}
      </svg>
    </div>
  );
};

// --- HLAVNÁ STRÁNKA ---
function HomePage() {
  const [query, setQuery] = useState('');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query) return;

    setLoading(true);
    setError(null);
    setData(null);

    try {
      const response = await fetch(`http://localhost:8000/api/search?q=${encodeURIComponent(query)}`);
      if (!response.ok) throw new Error('Chyba pri komunikácii so serverom');
      
      const result = await response.json();
      if (result.nodes.length === 0) {
        setError('Nenašli sa žiadne výsledky pre zadaný dopyt.');
      } else {
        setData(result);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0A0A0A] via-[#1a1a2e] to-[#16213e] relative overflow-hidden">
      {/* Animated Stars Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        {Array.from({ length: 100 }).map((_, i) => (
          <div
            key={i}
            className="absolute rounded-full bg-[#D4AF37] animate-pulse"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              width: `${Math.random() * 3 + 1}px`,
              height: `${Math.random() * 3 + 1}px`,
              opacity: Math.random() * 0.8 + 0.2,
              animationDelay: `${Math.random() * 3}s`,
              animationDuration: `${Math.random() * 4 + 2}s`,
            }}
          />
        ))}
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Logo Header */}
        <div className="text-center mb-16 animate-fade-in">
          <Logo size="xl" showText={true} className="mb-6" />
          <p className="text-lg text-gray-300 mt-4 max-w-2xl mx-auto">
            Business Intelligence & Visualization pre V4 región
          </p>
          <p className="text-sm text-gray-400 mt-2 max-w-xl mx-auto">
            Demokratizácia prístupu k dátam • Agregácia zo 4 krajín • Real-time vizualizácia vzťahov
          </p>
        </div>

        {/* Search Bar - Premium Design */}
        <div className="max-w-3xl mx-auto mb-16 animate-fade-in-up">
          <form onSubmit={handleSearch} className="relative">
            <div className="relative group">
              <div className="absolute inset-0 bg-gradient-to-r from-[#D4AF37]/20 via-[#FFD700]/20 to-[#D4AF37]/20 rounded-2xl blur-xl group-hover:blur-2xl transition-all duration-300"></div>
              <div className="relative bg-[#0A0A0A]/80 backdrop-blur-md border-2 border-[#D4AF37]/30 rounded-2xl p-2 shadow-2xl">
                <div className="flex items-center">
                  <Search className="absolute left-6 text-[#D4AF37] z-10" size={24} style={{ filter: 'drop-shadow(0 0 8px #D4AF37)' }} />
                  <input
                    type="text"
                    className="w-full pl-16 pr-32 py-5 bg-transparent text-white placeholder:text-[#D4AF37]/50 text-lg focus:outline-none focus:ring-0"
                    placeholder="Zadajte IČO alebo názov firmy (napr. 88888888, Agrofert)..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                  />
                  <button 
                    type="submit"
                    disabled={loading}
                    className="absolute right-2 bg-gradient-to-r from-[#D4AF37] to-[#FFD700] hover:from-[#FFD700] hover:to-[#D4AF37] text-[#0A0A0A] px-8 py-3 rounded-xl font-bold text-lg transition-all duration-300 transform hover:scale-105 hover:shadow-[0_0_30px_rgba(212,175,55,0.6)] disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
                    style={{ boxShadow: '0 0 20px rgba(212, 175, 55, 0.4)' }}
                  >
                    {loading ? (
                      <Loader2 className="animate-spin" size={20} />
                    ) : (
                      <span className="flex items-center gap-2">
                        <Sparkles size={18} />
                        Analyzovať
                      </span>
                    )}
                  </button>
                </div>
              </div>
            </div>
          </form>
          
          {/* Quick Test Hint */}
          <p className="text-center mt-4 text-sm text-[#D4AF37]/70">
            💡 Tip: Vyskúšajte testovacie IČO <span className="font-mono font-bold text-[#FFD700]">88888888</span>
          </p>
        </div>

        {/* Features Section */}
        {!data && (
          <div className="grid md:grid-cols-3 gap-6 mb-16 animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
            {[
              { icon: Globe, title: 'Cross-Border', desc: 'Agregácia dát zo 4 krajín V4' },
              { icon: Shield, title: 'Risk Intelligence', desc: 'Detekcia podvodov a rizík' },
              { icon: Sparkles, title: 'Real-time', desc: 'Aktuálne dáta z registrov' },
            ].map((feature, i) => (
              <div 
                key={i}
                className="bg-[#0A0A0A]/60 backdrop-blur-md border-2 border-[#D4AF37]/20 rounded-xl p-6 hover:border-[#D4AF37]/50 transition-all duration-300 hover:transform hover:scale-105 hover:shadow-[0_0_30px_rgba(212,175,55,0.3)] group"
              >
                <feature.icon className="w-12 h-12 text-[#D4AF37] mb-4 group-hover:scale-110 transition-transform" style={{ filter: 'drop-shadow(0 0 10px #D4AF37)' }} />
                <h3 className="text-xl font-bold text-[#D4AF37] mb-2">{feature.title}</h3>
                <p className="text-gray-300 text-sm">{feature.desc}</p>
              </div>
            ))}
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="max-w-3xl mx-auto mb-8 animate-fade-in">
            <div className="bg-red-900/30 border-2 border-red-500/50 text-red-200 p-6 rounded-xl flex items-center gap-3 backdrop-blur-md shadow-2xl">
              <AlertTriangle size={24} className="text-red-400" style={{ filter: 'drop-shadow(0 0 8px #ef4444)' }} />
              <span className="font-semibold">{error}</span>
            </div>
          </div>
        )}

        {/* Results / Graph */}
        {data && (
          <div className="animate-fade-in">
            <div className="flex justify-between items-center mb-6">
              <div>
                <h2 className="text-3xl font-bold text-[#D4AF37] mb-2" style={{ textShadow: '0 0 10px rgba(212, 175, 55, 0.5)' }}>
                  Nájdené subjekty: {data.nodes.filter(n => n.type === 'company').length}
                </h2>
                <p className="text-gray-400 text-sm">
                  Celkom uzlov: {data.nodes.length} • Vzťahy: {data.edges.length}
                </p>
              </div>
              <div className="flex gap-2">
                {['SK', 'CZ', 'PL', 'HU'].map(country => {
                  const count = data.nodes.filter(n => n.country === country).length;
                  if (count === 0) return null;
                  return (
                    <span 
                      key={country}
                      className="px-3 py-1 rounded-lg bg-[#D4AF37]/20 border border-[#D4AF37]/30 text-[#D4AF37] text-xs font-bold"
                    >
                      {country}: {count}
                    </span>
                  );
                })}
              </div>
            </div>
            
            <ForceGraph data={data} />
            
            {/* Disclaimer pod grafom */}
            <div className="mt-6">
              <Disclaimer />
            </div>
            
            {/* Detailný výpis (Tabuľka) */}
            <div className="mt-12 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {data.nodes.filter(n => n.type === 'company').map(node => (
                <div 
                  key={node.id} 
                  className="bg-[#0A0A0A]/60 backdrop-blur-md border-2 border-[#D4AF37]/20 rounded-xl p-6 hover:border-[#D4AF37]/50 transition-all duration-300 hover:transform hover:scale-105 hover:shadow-[0_0_30px_rgba(212,175,55,0.3)] group"
                >
                  <div className="flex justify-between items-start mb-3">
                    <h3 className="font-bold text-[#D4AF37] text-lg group-hover:text-[#FFD700] transition-colors">{node.label}</h3>
                    <span className="px-2 py-1 rounded bg-[#D4AF37]/20 border border-[#D4AF37]/30 text-[#D4AF37] text-xs font-mono font-bold">
                      {node.country}
                    </span>
                  </div>
                  <p className="text-gray-300 text-sm mb-3">{node.details}</p>
                  {node.risk_score > 0 && (
                    <div className="mt-3 inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-red-900/30 border border-red-500/50">
                      <AlertTriangle size={14} className="text-red-400" />
                      <span className="text-xs font-bold text-red-300">
                        Riziko: {node.risk_score}/10
                      </span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Custom Animations */}
      <style>{`
        @keyframes fade-in {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes fade-in-up {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes gradient {
          0%, 100% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
        }
        .animate-fade-in {
          animation: fade-in 0.8s ease-out;
        }
        .animate-fade-in-up {
          animation: fade-in-up 0.8s ease-out;
        }
        .animate-gradient {
          background-size: 200% auto;
          animation: gradient 3s ease infinite;
        }
      `}</style>
    </div>
  );
}

export default HomePage;
