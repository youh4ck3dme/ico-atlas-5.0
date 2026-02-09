import React, { useState } from 'react';
import { Search, Loader2, Sparkles, Globe, Shield, AlertTriangle } from 'lucide-react';
import Disclaimer from '../components/Disclaimer';
import Logo from '../components/Logo';
import NexusGraph from '../components/NexusGraph';

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
    <div className="min-h-screen bg-[#020617] relative overflow-hidden font-sans text-slate-200">

      {/* Background Gradients */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-blue-900/10 blur-[120px]"></div>
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-amber-900/10 blur-[120px]"></div>
      </div>

      <div className="relative z-10 max-w-[1600px] mx-auto px-4 py-8 flex flex-col h-screen">

        {/* Header Compact */}
        <div className="flex flex-col items-center justify-center mb-8 shrink-0">
          <Logo size="lg" showText={true} className="mb-4" />

          {/* Compact Search */}
          <div className="w-full max-w-2xl relative z-20">
            <form onSubmit={handleSearch} className="relative group">
              <div className="absolute inset-0 bg-gradient-to-r from-amber-500/20 to-blue-600/20 blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              <div className="relative flex items-center bg-slate-900/80 backdrop-blur-xl border border-slate-700/50 rounded-full shadow-2xl p-1">
                <Search className="ml-4 text-slate-400" size={20} />
                <input
                  type="text"
                  className="w-full bg-transparent border-none text-white px-4 py-2 focus:ring-0 placeholder-slate-500 font-mono"
                  placeholder="SEARCH INTELLIGENCE DATABASE..."
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                />
                <button
                  type="submit"
                  disabled={loading}
                  className="bg-slate-800 hover:bg-slate-700 text-amber-500 px-6 py-2 rounded-full font-bold text-sm border border-slate-700 transition-all disabled:opacity-50"
                >
                  {loading ? <Loader2 className="animate-spin" size={16} /> : 'ANALYZE'}
                </button>
              </div>
            </form>

            {!data && (
              <div className="flex justify-center gap-6 mt-4 text-xs text-slate-500 font-mono">
                <span>TRY: <b className="text-amber-500 cursor-pointer hover:underline" onClick={() => setQuery('88888888')}>88888888</b></span>
                <span>OR: <b className="text-amber-500 cursor-pointer hover:underline" onClick={() => setQuery('Agrofert')}>Agrofert</b></span>
              </div>
            )}
          </div>
        </div>

        {/* Main Content Area */}
        <div className="flex-1 min-h-0 flex flex-col relative">
          {error && (
            <div className="absolute top-0 left-0 right-0 z-50 flex justify-center p-4">
              <div className="bg-red-900/80 backdrop-blur border border-red-500/50 text-red-200 px-6 py-3 rounded-lg flex items-center gap-3 shadow-2xl">
                <AlertTriangle size={20} />
                <span>{error}</span>
              </div>
            </div>
          )}

          {!data && !loading && (
            <div className="flex-1 flex flex-col items-center justify-center text-center opacity-50">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl w-full">
                {[
                  { icon: Globe, title: 'V4 INTELLIGENCE', desc: 'SK • CZ • PL • HU Registry Aggregation' },
                  { icon: Shield, title: 'RISK ANALYSIS', desc: 'Real-time Debt & Fraud Detection' },
                  { icon: Sparkles, title: 'DEEP CONNECTIONS', desc: 'Cross-border Relationship Mapping' },
                ].map((item, i) => (
                  <div key={i} className="p-6 border border-slate-800 rounded-2xl bg-slate-900/30">
                    <item.icon className="w-10 h-10 text-slate-600 mb-4 mx-auto" strokeWidth={1.5} />
                    <h3 className="text-slate-300 font-bold mb-2 font-mono">{item.title}</h3>
                    <p className="text-slate-500 text-sm">{item.desc}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {data && (
            <div className="flex-1 relative h-full w-full animate-fade-in border border-slate-800/50 rounded-xl overflow-hidden shadow-2xl bg-black">
              <NexusGraph data={data} width={1200} height={800} />
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="shrink-0 py-4 text-center">
          <Disclaimer />
        </div>

      </div>

      <style>{`
        @keyframes fade-in {
          from { opacity: 0; transform: scale(0.98); }
          to { opacity: 1; transform: scale(1); }
        }
        .animate-fade-in {
          animation: fade-in 0.5s cubic-bezier(0.16, 1, 0.3, 1);
        }
      `}</style>
    </div>
  );
}

export default HomePage;
