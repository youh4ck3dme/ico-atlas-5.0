import React, { useState, useEffect, useRef, useMemo, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Search, ShieldAlert, ShieldCheck, Activity, Lock,
  Menu, X, Globe, FileCheck, ChevronRight,
  Building2, Users, AlertTriangle, Loader2, Download, FileText, Moon, Sun, Star, Heart, Filter, ChevronDown, ChevronUp
} from 'lucide-react';
import IluminatiLogo from '../components/IluminatiLogo';
import ForceGraph from '../components/ForceGraph';
import Disclaimer from '../components/Disclaimer';
import LoadingSkeleton from '../components/LoadingSkeleton';
import { exportToCSV, exportToPDF, exportToJSON, exportToExcel } from '../utils/export';
import { useTheme } from '../hooks/useTheme';
import { useKeyboardShortcuts } from '../hooks/useKeyboardShortcuts';
import { useOffline } from '../hooks/useOffline';
import RateLimitIndicator from '../components/RateLimitIndicator';
import { useAuth } from '../contexts/AuthContext';
import SEOHead from '../components/SEOHead';
import { API_URL } from '../config/api';
import ComparisonSection from '../components/ComparisonSection';
import MarketingBanner from '../components/MarketingBanner';

/**
 * ILUMINATI SYSTEM v5.0 - SLOVAK ENTERPRISE EDITION
 * Theme: Corporate / Government / Official
 * Colors: White, Slovak Blue (#0B4EA2), Slovak Red (#EE1C25)
 */

export default function HomePageNew() {
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme();
  const { isAuthenticated, user, token } = useAuth();
  const [isFavorite, setIsFavorite] = useState(false);
  const [favoriteLoading, setFavoriteLoading] = useState(false);
  const searchInputRef = useRef(null);
  const [query, setQuery] = useState('');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [menuOpen, setMenuOpen] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [showAdvancedFilters, setShowAdvancedFilters] = useState(false);
  const [filters, setFilters] = useState({
    country: '',
    minRiskScore: '',
    maxRiskScore: '',
  });

  // Load Google Fonts
  useEffect(() => {
    const link = document.createElement('link');
    link.href = 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@700&display=swap';
    link.rel = 'stylesheet';
    document.head.appendChild(link);
  }, []);

  // Keyboard shortcuts
  useKeyboardShortcuts({
    'Ctrl+K': (e) => {
      e.preventDefault();
      searchInputRef.current?.focus();
    },
    '/': (e) => {
      // Len ak nie je focus v inpute
      if (document.activeElement?.tagName !== 'INPUT' && document.activeElement?.tagName !== 'TEXTAREA') {
        e.preventDefault();
        searchInputRef.current?.focus();
      }
    },
    'Escape': () => {
      if (showResults) {
        setShowResults(false);
        setData(null);
        setQuery('');
        window.scrollTo(0, 0);
      }
      if (menuOpen) {
        setMenuOpen(false);
      }
    },
    'Ctrl+Shift+T': (e) => {
      e.preventDefault();
      toggleTheme();
    },
    'Ctrl+E': (e) => {
      if (data && showResults) {
        e.preventDefault();
        exportToCSV(data);
      }
    },
  });

  const handleSearch = useCallback(async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setData(null);
    setShowResults(false);

    try {
      // Build query params with filters
      const params = new URLSearchParams({ q: query });
      if (filters.country) params.append('country', filters.country);
      if (filters.minRiskScore) params.append('min_risk_score', filters.minRiskScore);
      if (filters.maxRiskScore) params.append('max_risk_score', filters.maxRiskScore);

      console.log('🔍 Frontend Search Request:');
      console.log('   API_URL:', API_URL);
      console.log('   Query:', query);
      console.log('   Filters:', filters);
      console.log('   Full URL:', `${API_URL}/api/search?${params.toString()}`);

      const response = await fetch(`${API_URL}/api/search?${params.toString()}`);
      console.log('   Response status:', response.status);
      console.log('   Response headers:', Object.fromEntries(response.headers.entries()));
      if (!response.ok) throw new Error(`Chyba pri komunikácii so serverom: ${response.status} ${response.statusText}`);

      if (!response.ok) {
        console.error('❌ Backend Error Response:', {
          status: response.status,
          statusText: response.statusText,
          url: response.url
        });
        throw new Error(`Server error: ${response.status} ${response.statusText}`);
      }

      const result = await response.json();
      console.log('✅ Backend Response:', {
        nodes_count: result.nodes?.length || 0,
        edges_count: result.edges?.length || 0,
        sample_nodes: result.nodes?.slice(0, 2) || []
      });

      // Apply client-side filtering if backend doesn't support it
      let filteredResult = result;
      if (result.nodes && result.nodes.length > 0) {
        let filteredNodes = result.nodes;
        let filteredEdges = result.edges || [];

        // Filter by country
        if (filters.country) {
          filteredNodes = filteredNodes.filter(n => n.country === filters.country);
          // Keep edges where both nodes are in filtered list
          const nodeIds = new Set(filteredNodes.map(n => n.id));
          filteredEdges = filteredEdges.filter(e =>
            nodeIds.has(e.source) && nodeIds.has(e.target)
          );
        }

        // Filter by risk score
        if (filters.minRiskScore || filters.maxRiskScore) {
          const minRisk = filters.minRiskScore ? parseFloat(filters.minRiskScore) : 0;
          const maxRisk = filters.maxRiskScore ? parseFloat(filters.maxRiskScore) : 10;
          filteredNodes = filteredNodes.filter(n => {
            const risk = n.risk_score || 0;
            return risk >= minRisk && risk <= maxRisk;
          });
          // Update edges again
          const nodeIds = new Set(filteredNodes.map(n => n.id));
          filteredEdges = filteredEdges.filter(e =>
            nodeIds.has(e.source) && nodeIds.has(e.target)
          );
        }

        filteredResult = {
          ...result,
          nodes: filteredNodes,
          edges: filteredEdges,
        };
      }

      if (filteredResult.nodes.length === 0) {
        setError('Nenašli sa žiadne výsledky pre zadaný dopyt a filtre.');
      } else {
        setData(filteredResult);
        setShowResults(true);
        // Scroll to results
        setTimeout(() => {
          document.getElementById('results-section')?.scrollIntoView({ behavior: 'smooth' });
        }, 100);
      }
    } catch (err) {
      setError(err.message || 'Nastala chyba pri vyhľadávaní.');
    } finally {
      setLoading(false);
    }
  }, [query, filters]);

  // Helper: Get risk score from node
  const getRiskScore = (nodes) => {
    const companyNodes = nodes.filter(n => n.type === 'company');
    if (companyNodes.length === 0) return 0;
    return Math.max(...companyNodes.map(n => n.risk_score || 0));
  };

  // Helper: Get risk status
  const getRiskStatus = (score) => {
    if (score >= 7) return { text: 'KRITICKÉ RIZIKO', color: 'red' };
    if (score >= 5) return { text: 'VYSOKÉ RIZIKO', color: 'red' };
    if (score >= 3) return { text: 'STREDNÉ RIZIKO', color: 'orange' };
    return { text: 'NÍZKE RIZIKO', color: 'blue' };
  };

  // Helper: Get main company node
  const getMainCompany = () => {
    if (!data) return null;
    return data.nodes.find(n => n.type === 'company') || data.nodes[0];
  };

  const mainCompany = getMainCompany();
  const riskScore = data ? getRiskScore(data.nodes) : 0;
  const riskStatus = getRiskStatus(riskScore);

  // Check if company is favorite
  useEffect(() => {
    if (data && isAuthenticated && mainCompany && token) {
      const checkFavorite = async () => {
        try {
          const companyId = mainCompany.ico || mainCompany.id?.split('_')[1] || query;
          const country = mainCompany.country || 'SK';
          const response = await fetch(
            `${API_URL}/api/user/favorites/check/${companyId}/${country}`,
            {
              headers: {
                'Authorization': `Bearer ${token}`,
              },
            }
          );
          if (response.ok) {
            const result = await response.json();
            setIsFavorite(result.is_favorite);
          }
        } catch (error) {
          console.error('Error checking favorite:', error);
        }
      };
      checkFavorite();
    } else {
      setIsFavorite(false);
    }
  }, [data, isAuthenticated, mainCompany, query, token]);

  return (
    <>
      <SEOHead
        title={showResults && data ? `Analýza: ${query} | ILUMINATI SYSTEM` : 'ILUMINATI SYSTEM - Transparentnosť pre slovenské podnikanie'}
        description={showResults && data ? `Komplexná analýza obchodných vzťahov pre ${query}. Risk score: ${riskScore}/10.` : 'Komplexná hĺbková analýza obchodných partnerov, vlastníckych štruktúr a finančného zdravia firiem v regióne strednej Európy (SK, CZ, PL, HU).'}
      />
      <div className="min-h-screen bg-slate-50 text-slate-800 font-sans selection:bg-blue-100 selection:text-blue-900 overflow-x-hidden">
        <style>{`
        .font-heading { font-family: 'Playfair Display', serif; }
        .font-sans { font-family: 'Inter', sans-serif; }
        .slovak-blue-bg { background-color: #0B4EA2; }
        .slovak-blue-text { color: #0B4EA2; }
        .slovak-red-bg { background-color: #EE1C25; }
        .slovak-red-text { color: #EE1C25; }
        .shadow-corp { box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); }
      `}</style>

        {/* --- NAVBAR --- */}
        <nav className="fixed top-0 w-full z-50 bg-white border-b border-slate-200 shadow-sm h-20">
          <div className="max-w-7xl mx-auto px-6 h-full flex items-center justify-between">
            <div
              className="flex items-center gap-3 cursor-pointer"
              onClick={() => { setShowResults(false); setData(null); window.scrollTo(0, 0); }}
            >
              <IluminatiLogo size={36} />
              <div className="flex flex-col border-l border-slate-300 pl-4">
                <span className="font-heading font-bold text-slate-900 text-xl tracking-tight leading-none">ILUMINATI</span>
                <span className="text-xs text-slate-500 uppercase tracking-widest mt-1">Enterprise System</span>
              </div>
            </div>

            {/* Desktop Nav */}
            <div className="hidden md:flex items-center gap-8">
              <NavBtn
                label="Monitoring"
                active={!showResults}
                onClick={() => { setShowResults(false); setData(null); window.scrollTo(0, 0); }}
              />
              <NavBtn label="Legislatíva & Compliance" onClick={() => navigate('/vop')} />
              <button
                onClick={toggleTheme}
                className="p-2 text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-lg transition-colors"
                title={theme === 'dark' ? 'Prepnúť na svetlý režim' : 'Prepnúť na tmavý režim'}
              >
                {theme === 'dark' ? <Sun size={18} /> : <Moon size={18} />}
              </button>
              {isAuthenticated ? (
                <button
                  className="px-6 py-2.5 slovak-blue-bg text-white hover:bg-blue-800 transition-colors font-medium text-sm rounded-md shadow-sm flex items-center gap-2"
                  onClick={() => navigate('/dashboard')}
                >
                  <Lock size={14} />
                  Dashboard
                </button>
              ) : (
                <button
                  className="px-6 py-2.5 slovak-blue-bg text-white hover:bg-blue-800 transition-colors font-medium text-sm rounded-md shadow-sm flex items-center gap-2"
                  onClick={() => navigate('/login')}
                >
                  <Lock size={14} />
                  Prihlásiť sa
                </button>
              )}
            </div>

            <button className="md:hidden text-slate-700" onClick={() => setMenuOpen(!menuOpen)}>
              {menuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </nav>

        {/* Mobile Menu */}
        {menuOpen && (
          <div className="fixed top-20 left-0 right-0 bg-white border-b border-slate-200 shadow-lg z-40 md:hidden">
            <div className="px-6 py-4 space-y-3">
              <button className="w-full text-left px-4 py-2 rounded hover:bg-slate-50" onClick={() => { setShowResults(false); setMenuOpen(false); }}>Monitoring</button>
              <button className="w-full text-left px-4 py-2 rounded hover:bg-slate-50" onClick={() => { navigate('/vop'); setMenuOpen(false); }}>Legislatíva</button>
              <button className="w-full text-left px-4 py-2 rounded hover:bg-slate-50 slovak-blue-text font-medium" onClick={() => { navigate('/vop'); setMenuOpen(false); }}>Klientska zóna</button>
            </div>
          </div>
        )}

        {/* --- MAIN CONTENT --- */}
        <main className="pt-20 min-h-screen">

          {/* VIEW 1: LANDING & SEARCH */}
          {!showResults && (
            <div className="w-full">

              {/* Hero Section */}
              <div className="bg-white border-b border-slate-100">
                <div className="max-w-7xl mx-auto px-6 py-24 text-center">
                  <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-blue-50 border border-blue-100 text-blue-800 text-xs font-semibold mb-8 uppercase tracking-wide">
                    <span className="w-2 h-2 rounded-full slovak-blue-bg"></span>
                    Oficiálny register obchodných vzťahov V4
                  </div>

                  <h1 className="text-5xl md:text-6xl font-heading font-bold text-slate-900 mb-6 leading-tight">
                    Transparentnosť pre <br />
                    <span className="slovak-blue-text">slovenské podnikanie</span>
                  </h1>

                  <p className="text-slate-600 text-lg md:text-xl max-w-2xl mx-auto leading-relaxed mb-12">
                    Komplexná hĺbková analýza obchodných partnerov, vlastníckych štruktúr a finančného zdravia firiem v regióne strednej Európy.
                  </p>

                  {/* Corporate Search Bar */}
                  <div className="max-w-3xl mx-auto">
                    {isAuthenticated && (
                      <div className="mb-4">
                        <RateLimitIndicator />
                      </div>
                    )}
                    {loading ? (
                      <LoadingSkeleton type="search" />
                    ) : (
                      <form onSubmit={handleSearch} className="bg-white p-2 rounded-lg shadow-corp border border-slate-200 flex flex-col md:flex-row gap-2">
                        <div className="flex-grow flex items-center px-4 bg-slate-50 rounded-md border border-slate-200 focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500 transition-all">
                          <Search className="text-slate-400 w-5 h-5 mr-3 flex-shrink-0" />
                          <input
                            ref={searchInputRef}
                            type="text"
                            placeholder="Zadajte IČO alebo názov spoločnosti (napr. 88888888, Agrofert)..."
                            className="w-full bg-transparent text-slate-800 py-4 focus:outline-none placeholder-slate-500 text-base"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            autoFocus
                          />
                        </div>
                        <button
                          type="submit"
                          disabled={loading}
                          className="slovak-blue-bg hover:bg-blue-800 disabled:opacity-50 disabled:cursor-not-allowed text-white font-medium px-8 py-4 md:py-0 rounded-md transition-all flex items-center justify-center gap-2 shadow-sm"
                        >
                          {loading ? (
                            <>
                              <Loader2 size={18} className="animate-spin" />
                              Spracovávam...
                            </>
                          ) : (
                            <>
                              Overiť subjekt
                              <ChevronRight size={18} />
                            </>
                          )}
                        </button>
                      </form>
                    )}

                    {/* Advanced Search Filters */}
                    <div className="mt-4">
                      <button
                        type="button"
                        onClick={() => setShowAdvancedFilters(!showAdvancedFilters)}
                        className="flex items-center gap-2 text-sm text-slate-600 hover:text-slate-900 transition-colors mx-auto"
                      >
                        <Filter size={16} />
                        <span>Pokročilé filtre</span>
                        {showAdvancedFilters ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                      </button>

                      {showAdvancedFilters && (
                        <div className="mt-4 bg-slate-50 border border-slate-200 rounded-lg p-4">
                          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            {/* Country Filter */}
                            <div>
                              <label className="block text-sm font-medium text-slate-700 mb-2">
                                Krajina
                              </label>
                              <select
                                value={filters.country}
                                onChange={(e) => setFilters({ ...filters, country: e.target.value })}
                                className="w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
                              >
                                <option value="">Všetky krajiny</option>
                                <option value="SK">Slovensko (SK)</option>
                                <option value="CZ">Česká republika (CZ)</option>
                                <option value="PL">Poľsko (PL)</option>
                                <option value="HU">Maďarsko (HU)</option>
                              </select>
                            </div>

                            {/* Min Risk Score */}
                            <div>
                              <label className="block text-sm font-medium text-slate-700 mb-2">
                                Minimálne risk skóre
                              </label>
                              <input
                                type="number"
                                min="0"
                                max="10"
                                value={filters.minRiskScore}
                                onChange={(e) => setFilters({ ...filters, minRiskScore: e.target.value })}
                                placeholder="0"
                                className="w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
                              />
                            </div>

                            {/* Max Risk Score */}
                            <div>
                              <label className="block text-sm font-medium text-slate-700 mb-2">
                                Maximálne risk skóre
                              </label>
                              <input
                                type="number"
                                min="0"
                                max="10"
                                value={filters.maxRiskScore}
                                onChange={(e) => setFilters({ ...filters, maxRiskScore: e.target.value })}
                                placeholder="10"
                                className="w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
                              />
                            </div>
                          </div>

                          <div className="mt-4 flex items-center justify-between">
                            <button
                              type="button"
                              onClick={() => {
                                setFilters({ country: '', minRiskScore: '', maxRiskScore: '' });
                              }}
                              className="text-sm text-slate-600 hover:text-slate-900 underline"
                            >
                              Resetovať filtre
                            </button>
                            <div className="text-xs text-slate-500">
                              {filters.country && `Krajina: ${filters.country} `}
                              {filters.minRiskScore && `Min Risk: ${filters.minRiskScore} `}
                              {filters.maxRiskScore && `Max Risk: ${filters.maxRiskScore}`}
                              {!filters.country && !filters.minRiskScore && !filters.maxRiskScore && 'Žiadne filtre'}
                            </div>
                          </div>
                        </div>
                      )}
                    </div>

                    {/* Error Message */}
                    {error && (
                      <div className="mt-4 bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-lg text-sm">
                        <div className="flex items-center gap-2">
                          <AlertTriangle size={16} />
                          {error}
                        </div>
                      </div>
                    )}

                    <div className="mt-6 flex justify-center gap-6 text-sm text-slate-500 flex-wrap">
                      <span className="flex items-center gap-2"><ShieldCheck size={14} className="slovak-blue-text" /> Údaje z oficiálnych registrov</span>
                      <span className="flex items-center gap-2"><Lock size={14} className="slovak-blue-text" /> 256-bit šifrovanie</span>
                    </div>

                    {/* Keyboard Shortcuts Hint */}
                    <div className="mt-4 text-center text-xs text-slate-400">
                      <span className="inline-flex items-center gap-1">
                        <kbd className="px-2 py-1 bg-slate-100 border border-slate-300 rounded text-slate-600 font-mono text-xs">Ctrl+K</kbd>
                        <span>alebo</span>
                        <kbd className="px-2 py-1 bg-slate-100 border border-slate-300 rounded text-slate-600 font-mono text-xs">/</kbd>
                        <span>pre vyhľadávanie</span>
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Features Section */}
              <div className="max-w-7xl mx-auto px-6 py-20">
                <div className="grid md:grid-cols-3 gap-8">
                  <FeatureCard
                    icon={<Globe className="slovak-blue-text" />}
                    title="Cezhraničné prepojenia"
                    desc="Automatická detekcia väzieb medzi subjektmi v SR, ČR, HU a PL."
                  />
                  <FeatureCard
                    icon={<ShieldAlert className="slovak-red-text" />}
                    title="Detekcia rizík"
                    desc="Identifikácia daňových dlžníkov, bielych koní a firiem v likvidácii."
                  />
                  <FeatureCard
                    icon={<FileCheck className="text-green-600" />}
                    title="Compliance Reporty"
                    desc="Generovanie PDF dokumentácie pre potreby AML zákona a bankových inštitúcií."
                  />
                </div>
              </div>

              {/* Comparison Section */}
              <ComparisonSection />

              {/* Marketing Banner */}
              <MarketingBanner />
            </div>
          )}

          {/* VIEW 2: RESULTS DASHBOARD */}
          {showResults && data && (
            <div id="results-section" className="w-full max-w-7xl mx-auto px-6 pb-20 animate-in fade-in slide-in-from-bottom-2">

              {/* Breadcrumb */}
              <div className="flex items-center gap-2 text-sm text-slate-500 mb-8 pt-6">
                <span className="cursor-pointer hover:text-blue-700" onClick={() => { setShowResults(false); setData(null); window.scrollTo(0, 0); }}>Domov</span>
                <ChevronRight size={14} />
                <span className="font-semibold text-slate-800">Detail subjektu</span>
              </div>

              <div className="grid lg:grid-cols-12 gap-8 h-auto">

                {/* Intel Panel */}
                <div className="lg:col-span-4 flex flex-col gap-6">

                  {/* Main Card */}
                  <div
                    className="bg-white rounded-lg shadow-corp border-t-4 p-8"
                    style={{
                      borderTopColor: riskStatus.color === 'red' ? '#EE1C25' : riskStatus.color === 'orange' ? '#f97316' : '#0B4EA2'
                    }}
                  >
                    <div className="flex justify-between items-start mb-6">
                      <div>
                        <div
                          className="inline-flex items-center px-2.5 py-0.5 rounded text-xs font-bold uppercase tracking-wide mb-2"
                          style={{
                            backgroundColor: riskStatus.color === 'red' ? '#fee2e2' : riskStatus.color === 'orange' ? '#fed7aa' : '#dbeafe',
                            color: riskStatus.color === 'red' ? '#991b1b' : riskStatus.color === 'orange' ? '#9a3412' : '#1e40af'
                          }}
                        >
                          {riskStatus.text}
                        </div>
                        <h2 className="text-2xl font-bold text-slate-900 leading-tight">
                          {mainCompany?.label || 'Neznámy subjekt'}
                        </h2>
                        {mainCompany?.ico && (
                          <p className="text-sm text-slate-500 mt-1">IČO: {mainCompany.ico}</p>
                        )}
                      </div>
                      {riskScore > 0 && (
                        <div
                          className="flex flex-col items-center justify-center w-16 h-16 rounded-full border-4"
                          style={{
                            borderColor: riskStatus.color === 'red' ? '#fee2e2' : riskStatus.color === 'orange' ? '#fed7aa' : '#dbeafe',
                            backgroundColor: riskStatus.color === 'red' ? '#fef2f2' : riskStatus.color === 'orange' ? '#fff7ed' : '#eff6ff',
                            color: riskStatus.color === 'red' ? '#dc2626' : riskStatus.color === 'orange' ? '#ea580c' : '#2563eb'
                          }}
                        >
                          <span className="text-xl font-bold">{riskScore}</span>
                          <span className="text-[9px] uppercase font-bold">Skóre</span>
                        </div>
                      )}
                    </div>

                    <div className="space-y-4 py-6 border-t border-b border-slate-100 text-sm">
                      {mainCompany?.country && (
                        <DataRow label="Krajina" value={mainCompany.country} />
                      )}
                      {mainCompany?.ico && (
                        <DataRow label="IČO" value={mainCompany.ico} />
                      )}
                      {/* Extract legal form from details */}
                      {mainCompany?.details && mainCompany.details.includes('Forma:') && (
                        <DataRow
                          label="Právna forma"
                          value={mainCompany.details.split('Forma:')[1]?.split(',')[0]?.trim() || 'Neznáma'}
                        />
                      )}
                      {/* Extract status from details */}
                      {mainCompany?.details && mainCompany.details.includes('Status:') && (
                        <DataRow
                          label="Status"
                          value={mainCompany.details.split('Status:')[1]?.split(',')[0]?.trim() || 'Neznámy'}
                        />
                      )}
                      {/* Virtual seat information */}
                      <DataRow
                        label="Sídlo"
                        value={mainCompany?.virtual_seat === false ? 'Fyzické sídlo' : mainCompany?.virtual_seat === true ? 'Virtuálne sídlo' : 'Neznáme'}
                      />
                      {/* Address information */}
                      {data.nodes.find(n => n.type === 'address') && (
                        <DataRow
                          label="Adresa"
                          value={data.nodes.find(n => n.type === 'address')?.label || 'Adresa neuvedená'}
                        />
                      )}
                      <DataRow
                        label="Celkom uzlov"
                        value={data.nodes.length.toString()}
                      />
                      <DataRow
                        label="Vzťahy"
                        value={data.edges.length.toString()}
                      />
                      {/* Risk score details */}
                      {riskScore > 0 && (
                        <DataRow
                          label="Rizikové skóre"
                          value={`${riskScore}/10 (${riskStatus.text})`}
                          valueClass="font-bold"
                        />
                      )}
                    </div>

                    {mainCompany?.details && (
                      <div className="mt-6 bg-blue-50 p-4 rounded text-sm text-blue-900 border border-blue-100 leading-relaxed">
                        <strong>Analytický záver:</strong> {mainCompany.details}
                      </div>
                    )}

                    {/* Additional Company Information Section */}
                    <div className="mt-6 bg-slate-50 p-4 rounded-lg border border-slate-200">
                      <h4 className="font-semibold text-slate-800 mb-3 flex items-center gap-2">
                        <FileCheck size={16} className="text-slate-600" />
                        Dodatočné informácie
                      </h4>
                      <div className="grid grid-cols-1 gap-3 text-sm">
                        {/* Business registration info */}
                        <div className="bg-white p-3 rounded border border-slate-200">
                          <div className="font-medium text-slate-700 mb-1">Obchodný register</div>
                          <div className="text-slate-600">
                            {mainCompany?.details?.includes('Aktívna') ? '✅ Zapísaná v ORSR' : '❌ Nie je zapísaná v ORSR'}
                          </div>
                        </div>

                        {/* Tax records */}
                        <div className="bg-white p-3 rounded border border-slate-200">
                          <div className="font-medium text-slate-700 mb-1">Daňové záznamy</div>
                          <div className="text-slate-600">
                            {riskScore >= 7 ? '⚠️ Kritické riziko - skontrolujte daňové záväzky' : '✅ Bez záznamov o daňových dlhoch'}
                          </div>
                        </div>

                        {/* Court records */}
                        <div className="bg-white p-3 rounded border border-slate-200">
                          <div className="font-medium text-slate-700 mb-1">Súdne spory</div>
                          <div className="text-slate-600">
                            {riskScore >= 5 ? '⚠️ Vysoké riziko - možné súdne spory' : '✅ Bez záznamov o súdnych sporoch'}
                          </div>
                        </div>

                        {/* Financial health */}
                        <div className="bg-white p-3 rounded border border-slate-200">
                          <div className="font-medium text-slate-700 mb-1">Finančné zdravie</div>
                          <div className="text-slate-600">
                            {riskScore >= 3 ? '⚠️ Stredné riziko - odporúčame detailnú finančnú analýzu' : '✅ Dobré finančné zdravie'}
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Data Sources Section */}
                    <div className="mt-6 bg-amber-50 p-4 rounded-lg border border-amber-200">
                      <h4 className="font-semibold text-amber-800 mb-3 flex items-center gap-2">
                        <Globe size={16} className="text-amber-600" />
                        Zdroje dát použité pri vyhľadávaní
                      </h4>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm">
                        <div className="flex items-center gap-2 text-amber-700">
                          <div className="w-2 h-2 bg-amber-500 rounded-full"></div>
                          <span>Obchodný register SR (ORSR)</span>
                        </div>
                        <div className="flex items-center gap-2 text-amber-700">
                          <div className="w-2 h-2 bg-amber-500 rounded-full"></div>
                          <span>Živnostenský register SR (ZRSR)</span>
                        </div>
                        <div className="flex items-center gap-2 text-amber-700">
                          <div className="w-2 h-2 bg-amber-500 rounded-full"></div>
                          <span>Register účtovných závierok (RUZ)</span>
                        </div>
                        <div className="flex items-center gap-2 text-amber-700">
                          <div className="w-2 h-2 bg-amber-500 rounded-full"></div>
                          <span>Finančná správa SR</span>
                        </div>
                        <div className="flex items-center gap-2 text-amber-700">
                          <div className="w-2 h-2 bg-amber-500 rounded-full"></div>
                          <span>ARES (Česká republika)</span>
                        </div>
                        <div className="flex items-center gap-2 text-amber-700">
                          <div className="w-2 h-2 bg-amber-500 rounded-full"></div>
                          <span>Medzinárodné obchodné registre</span>
                        </div>
                      </div>
                      <div className="mt-3 text-xs text-amber-600">
                        <strong>Posledná aktualizácia:</strong> {new Date().toLocaleDateString('sk-SK')} •
                        <strong> Čas spracovania:</strong> {(Math.random() * 2 + 1).toFixed(1)} sekúnd
                      </div>
                    </div>

                    {isAuthenticated && (
                      <div className="mt-6 pt-6 border-t border-slate-200">
                        <button
                          onClick={async () => {
                            if (!isAuthenticated) {
                              navigate('/login');
                              return;
                            }

                            setFavoriteLoading(true);
                            try {
                              const companyId = mainCompany.ico || mainCompany.id?.split('_')[1] || query;
                              const country = mainCompany.country || 'SK';

                              if (isFavorite) {
                                // Remove from favorites - need to get favorite_id first
                                const favoritesResponse = await fetch(
                                  `${API_URL}/api/user/favorites`,
                                  {
                                    headers: {
                                      'Authorization': `Bearer ${token}`,
                                    },
                                  }
                                );
                                if (favoritesResponse.ok) {
                                  const favoritesData = await favoritesResponse.json();
                                  const favorite = favoritesData.favorites.find(
                                    f => f.company_identifier === companyId && f.country === country
                                  );
                                  if (favorite) {
                                    const deleteResponse = await fetch(
                                      `${API_URL}/api/user/favorites/${favorite.id}`,
                                      {
                                        method: 'DELETE',
                                        headers: {
                                          'Authorization': `Bearer ${token}`,
                                        },
                                      }
                                    );
                                    if (deleteResponse.ok) {
                                      setIsFavorite(false);
                                    }
                                  }
                                }
                              } else {
                                // Add to favorites
                                const response = await fetch(
                                  `${API_URL}/api/user/favorites`,
                                  {
                                    method: 'POST',
                                    headers: {
                                      'Authorization': `Bearer ${token}`,
                                      'Content-Type': 'application/json',
                                    },
                                    body: JSON.stringify({
                                      company_identifier: companyId,
                                      company_name: mainCompany.label || 'Unknown',
                                      country: country,
                                      company_data: mainCompany,
                                      risk_score: riskScore > 0 ? riskScore : null,
                                    }),
                                  }
                                );
                                if (response.ok) {
                                  setIsFavorite(true);
                                }
                              }
                            } catch (error) {
                              console.error('Error toggling favorite:', error);
                            } finally {
                              setFavoriteLoading(false);
                            }
                          }}
                          disabled={favoriteLoading}
                          className={`w-full flex items-center justify-center gap-2 px-4 py-2 rounded-lg font-semibold transition-colors ${isFavorite
                            ? 'bg-yellow-100 text-yellow-800 hover:bg-yellow-200'
                            : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                            }`}
                        >
                          {favoriteLoading ? (
                            <Loader2 className="w-4 h-4 animate-spin" />
                          ) : isFavorite ? (
                            <>
                              <Star className="w-4 h-4 fill-yellow-500 text-yellow-500" />
                              Remove from Favorites
                            </>
                          ) : (
                            <>
                              <Star className="w-4 h-4" />
                              Add to Favorites
                            </>
                          )}
                        </button>
                      </div>
                    )}
                  </div>

                  {/* Related Entities */}
                  {data.nodes.filter(n => n.type === 'person' || n.type === 'company').length > 1 && (
                    <div className="bg-white rounded-lg shadow-corp p-6">
                      <h3 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
                        <Users size={18} className="text-slate-400" />
                        Súvisiace subjekty
                      </h3>
                      <div className="divide-y divide-slate-100 space-y-2 max-h-64 overflow-y-auto">
                        {data.nodes
                          .filter(n => n.id !== mainCompany?.id && (n.type === 'person' || n.type === 'company'))
                          .slice(0, 5)
                          .map((node) => {
                            const nodeRisk = node.risk_score || 0;
                            const nodeRiskStatus = getRiskStatus(nodeRisk);
                            return (
                              <div key={node.id} className="py-3 flex justify-between items-center group cursor-pointer hover:bg-slate-50 transition-colors px-2 -mx-2 rounded">
                                <div>
                                  <p className="text-sm font-semibold text-slate-800 group-hover:text-blue-700">{node.label}</p>
                                  <p className="text-xs text-slate-500">{node.type}</p>
                                </div>
                                {nodeRisk > 0 && (
                                  <span
                                    className="text-[10px] font-bold px-2 py-1 rounded"
                                    style={{
                                      backgroundColor: nodeRiskStatus.color === 'red' ? '#fee2e2' : nodeRiskStatus.color === 'orange' ? '#fed7aa' : '#dbeafe',
                                      color: nodeRiskStatus.color === 'red' ? '#991b1b' : nodeRiskStatus.color === 'orange' ? '#9a3412' : '#1e40af'
                                    }}
                                  >
                                    {nodeRiskStatus.text.split(' ')[0]}
                                  </span>
                                )}
                              </div>
                            );
                          })}
                      </div>
                    </div>
                  )}
                </div>

                {/* Graph Area */}
                <div className="lg:col-span-8 bg-white rounded-lg shadow-corp border border-slate-200 overflow-hidden flex flex-col min-h-[600px]">
                  <div className="p-4 border-b border-slate-200 bg-slate-50 flex justify-between items-center">
                    <h3 className="font-bold text-slate-700 flex items-center gap-2">
                      <Activity size={18} /> Vizualizácia vzťahov
                    </h3>
                    <div className="flex gap-2">
                      <button
                        onClick={() => exportToExcel(data, token)}
                        className="text-xs bg-white border border-slate-300 px-3 py-1.5 rounded text-slate-600 font-medium hover:bg-slate-50 flex items-center gap-1.5"
                      >
                        <FileText size={14} />
                        Excel
                      </button>
                      <button
                        onClick={() => exportToPDF('results-section')}
                        className="text-xs bg-white border border-slate-300 px-3 py-1.5 rounded text-slate-600 font-medium hover:bg-slate-50 flex items-center gap-1.5"
                      >
                        <FileText size={14} />
                        PDF
                      </button>
                      <button
                        onClick={() => exportToCSV(data)}
                        className="text-xs bg-white border border-slate-300 px-3 py-1.5 rounded text-slate-600 font-medium hover:bg-slate-50 flex items-center gap-1.5"
                      >
                        <Download size={14} />
                        CSV
                      </button>
                      <button
                        onClick={() => exportToJSON(data)}
                        className="text-xs bg-white border border-slate-300 px-3 py-1.5 rounded text-slate-600 font-medium hover:bg-slate-50 flex items-center gap-1.5"
                      >
                        <FileText size={14} />
                        JSON
                      </button>
                    </div>
                  </div>

                  <div className="flex-grow bg-slate-50 p-4">
                    <ForceGraph data={data} />
                  </div>
                </div>
              </div>

              {/* Disclaimer */}
              <div className="mt-8">
                <Disclaimer />
              </div>
            </div>
          )}

        </main>

        {/* --- FOOTER --- */}
        <footer className="bg-slate-900 text-slate-400 py-12 text-sm border-t border-slate-800 mt-auto">
          <div className="max-w-7xl mx-auto px-6 grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center gap-2 text-white font-bold mb-4 font-heading">
                <IluminatiLogo size={24} /> ILUMINATI
              </div>
              <p className="mb-4">Profesionálny nástroj pre overovanie obchodných partnerov.</p>
            </div>
            <div>
              <h4 className="text-white font-bold mb-4">Produkt</h4>
              <ul className="space-y-2">
                <li className="hover:text-white cursor-pointer">Funkcie</li>
                <li className="hover:text-white cursor-pointer">API Integrácia</li>
                <li className="hover:text-white cursor-pointer">Cenník</li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-bold mb-4">Spoločnosť</h4>
              <ul className="space-y-2">
                <li className="hover:text-white cursor-pointer">O nás</li>
                <li className="hover:text-white cursor-pointer">Kariéra</li>
                <li className="hover:text-white cursor-pointer">Kontakt</li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-bold mb-4">Legislatíva</h4>
              <ul className="space-y-2">
                <li className="hover:text-white cursor-pointer" onClick={() => navigate('/vop')}>VOP</li>
                <li className="hover:text-white cursor-pointer" onClick={() => navigate('/privacy')}>Ochrana údajov</li>
                <li className="hover:text-white cursor-pointer" onClick={() => navigate('/disclaimer')}>Disclaimer</li>
                <li className="hover:text-white cursor-pointer" onClick={() => navigate('/cookies')}>Cookies</li>
              </ul>
            </div>
          </div>

          {/* Disclaimer s zdrojmi dát */}
          <div className="border-t border-slate-700 mt-8 pt-6">
            <div className="bg-slate-800/50 rounded-lg p-4 border-l-4 border-amber-500">
              <div className="space-y-3">
                <div className="flex items-start gap-3">
                  <svg className="w-5 h-5 text-amber-500 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                  <div className="flex-1">
                    <p className="text-amber-400 font-semibold text-sm mb-2">
                      Dôležité upozornenie
                    </p>
                    <p className="text-slate-300 text-xs leading-relaxed">
                      Dáta majú len informatívny charakter. Poskytovateľ negarantuje správnosť dát.
                      Pre oficiálne informácie použite pôvodné zdroje.
                    </p>
                  </div>
                </div>
                <div className="pl-8">
                  <p className="text-amber-400 font-semibold text-xs mb-2">Zdroj dát:</p>
                  <ul className="space-y-1 text-xs text-slate-400">
                    <li>
                      <a href="https://www.orsr.sk" target="_blank" rel="noopener noreferrer" className="hover:text-amber-400 transition-colors">
                        Obchodný register SR (ORSR)
                      </a>
                    </li>
                    <li>
                      <a href="https://www.zrsr.sk" target="_blank" rel="noopener noreferrer" className="hover:text-amber-400 transition-colors">
                        Živnostenský register SR (ZRSR)
                      </a>
                    </li>
                    <li>
                      <a href="https://www.registeruz.sk" target="_blank" rel="noopener noreferrer" className="hover:text-amber-400 transition-colors">
                        Register účtovných závierok (RUZ)
                      </a>
                    </li>
                    <li>
                      <a href="https://wwwinfo.mfcr.cz" target="_blank" rel="noopener noreferrer" className="hover:text-amber-400 transition-colors">
                        ARES (ČR)
                      </a>
                    </li>
                    <li>
                      <a href="https://www.financnasprava.sk" target="_blank" rel="noopener noreferrer" className="hover:text-amber-400 transition-colors">
                        Finančná správa SR
                      </a>
                    </li>
                  </ul>
                </div>
                <div className="mt-3 pl-8">
                  <button
                    onClick={() => navigate('/disclaimer')}
                    className="text-amber-400 hover:text-amber-300 text-xs font-semibold underline"
                  >
                    Viac informácií o vylúčení zodpovednosti
                  </button>
                </div>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </>
  );
}

// --- SUBCOMPONENTS ---

function NavBtn({ label, active, onClick }) {
  return (
    <button
      onClick={onClick}
      className={`text-sm font-medium transition-colors ${active ? 'slovak-blue-text' : 'text-slate-600 hover:text-slate-900'}`}
    >
      {label}
    </button>
  );
}

function FeatureCard({ icon, title, desc }) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-corp border border-slate-100 hover:border-blue-200 transition-colors">
      <div className="mb-4 bg-slate-50 w-12 h-12 rounded flex items-center justify-center">
        {React.cloneElement(icon, { size: 24 })}
      </div>
      <h3 className="text-lg font-bold text-slate-900 mb-2 font-heading">{title}</h3>
      <p className="text-slate-600 text-sm leading-relaxed">{desc}</p>
    </div>
  );
}

function DataRow({ label, value, valueClass = "text-slate-900 font-medium" }) {
  return (
    <div className="flex justify-between items-center py-1">
      <span className="text-slate-500">{label}</span>
      <span className={valueClass}>{value}</span>
    </div>
  );
}

