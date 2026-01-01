import React, { useState, useEffect, useCallback, useMemo } from 'react';
import {
    Search, BarChart3, Users, Building2,
    TrendingUp, AlertTriangle, Globe,
    Download, Share2, Settings, Filter,
    Plus, RefreshCw, Eye, EyeOff
} from 'lucide-react';
import EnhancedForceGraph from '../components/EnhancedForceGraph';
import { useAuth } from '../contexts/AuthContext';

const EnhancedDashboard = () => {
    const { user, isAuthenticated } = useAuth();
    const [searchQuery, setSearchQuery] = useState('');
    const [searchResults, setSearchResults] = useState([]);
    const [selectedCompany, setSelectedCompany] = useState(null);
    const [graphData, setGraphData] = useState({ nodes: [], edges: [] });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [activeTab, setActiveTab] = useState('search');
    const [dashboardMetrics, setDashboardMetrics] = useState({});
    const [filters, setFilters] = useState({
        countries: ['SK', 'CZ', 'PL', 'HU'],
        riskMin: 0,
        riskMax: 10,
        legalForms: [],
        dateRange: 'all'
    });

    // Dashboard metrics calculation
    const calculateMetrics = useCallback((companies) => {
        if (!companies || companies.length === 0) {
            return {
                totalCompanies: 0,
                avgRiskScore: 0,
                highRiskCount: 0,
                countriesCount: 0,
                totalRelationships: 0
            };
        }

        const totalCompanies = companies.length;
        const riskScores = companies.map(c => c.risk_score || 0);
        const avgRiskScore = (riskScores.reduce((a, b) => a + b, 0) / totalCompanies).toFixed(1);
        const highRiskCount = companies.filter(c => (c.risk_score || 0) > 7).length;
        const countriesCount = new Set(companies.map(c => c.country)).size;
        const totalRelationships = companies.reduce((sum, c) => sum + (c.related_companies?.length || 0), 0);

        return {
            totalCompanies,
            avgRiskScore,
            highRiskCount,
            countriesCount,
            totalRelationships
        };
    }, []);

    // Generate sample graph data for demonstration
    const generateSampleGraphData = useCallback((companies) => {
        if (!companies || companies.length === 0) {
            return { nodes: [], edges: [] };
        }

        const nodes = companies.map((company, index) => ({
            id: company.identifier || `company_${index}`,
            label: company.name || company.label || `Company ${index + 1}`,
            type: 'company',
            country: company.country || 'SK',
            risk_score: company.risk_score || Math.random() * 10,
            size: 8 + (company.risk_score || 0) * 0.5,
            connections: Math.floor(Math.random() * 10),
            details: company
        }));

        // Generate sample edges
        const edges = [];
        for (let i = 0; i < nodes.length; i++) {
            for (let j = i + 1; j < Math.min(nodes.length, i + 3); j++) {
                if (Math.random() > 0.5) {
                    edges.push({
                        source: nodes[i].id,
                        target: nodes[j].id,
                        type: 'RELATED_TO',
                        weight: Math.random() * 5 + 1
                    });
                }
            }
        }

        return { nodes, edges };
    }, []);

    // Search function
    const handleSearch = useCallback(async () => {
        if (!searchQuery.trim()) return;

        setLoading(true);
        setError(null);

        try {
            // Simulate API call - in real implementation, this would call the backend
            const mockResults = [
                {
                    identifier: '35906215',
                    name: 'Agrofert Holding a.s.',
                    country: 'CZ',
                    address: 'U Trati 123/12, 100 00 Praha 10',
                    risk_score: 3.2,
                    legal_form: 'Akciová společnost',
                    executives: ['Petr Kellner', 'Daniel Křetínský'],
                    shareholders: ['Petr Kellner', 'Jana Křetínská'],
                    founded: '1993-01-01',
                    status: 'Aktivní',
                    related_companies: ['Komerční banka', 'ČEZ Group']
                },
                {
                    identifier: '45406215',
                    name: 'Slovenské elektrárne, a.s.',
                    country: 'SK',
                    address: 'Drieňová 4, 820 07 Bratislava',
                    risk_score: 6.8,
                    legal_form: 'Akciová spoločnosť',
                    executives: ['Miroslav Kollár', 'Peter Žiga'],
                    shareholders: ['Enel', 'EPH'],
                    founded: '1996-01-01',
                    status: 'Aktivní',
                    related_companies: ['Enel', 'EPH', 'ČEZ Group']
                },
                {
                    identifier: '12345678',
                    name: 'Virtual Office Services s.r.o.',
                    country: 'SK',
                    address: 'Nábrežie arm. gen. L. Svobodu 1, 811 02 Bratislava',
                    risk_score: 8.5,
                    legal_form: 'Spoločnosť s ručením obmedzeným',
                    executives: ['Ján Novák'],
                    shareholders: ['Ján Novák'],
                    founded: '2020-01-01',
                    status: 'Aktivní',
                    virtual_seat: true,
                    related_companies: []
                }
            ];

            setSearchResults(mockResults);
            setDashboardMetrics(calculateMetrics(mockResults));
            setGraphData(generateSampleGraphData(mockResults));

        } catch (err) {
            setError('Search failed. Please try again.');
            console.error('Search error:', err);
        } finally {
            setLoading(false);
        }
    }, [searchQuery, calculateMetrics, generateSampleGraphData]);

    // Export functionality
    const handleExport = useCallback(async (format) => {
        try {
            // This would call the backend export service
            console.log(`Exporting to ${format}...`);

            // Mock export - in real implementation, this would download a file
            const exportData = {
                format,
                companies: searchResults,
                graphData,
                generatedAt: new Date().toISOString()
            };

            console.log('Export data:', exportData);

            // Simulate download
            const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `iluminati_export_${format}_${Date.now()}.json`;
            link.click();
            URL.revokeObjectURL(url);

        } catch (err) {
            console.error('Export failed:', err);
        }
    }, [searchResults, graphData]);

    // Share functionality
    const handleShare = useCallback(async () => {
        try {
            const shareData = {
                title: 'ILUMINATI System - Business Intelligence',
                text: `Search results for "${searchQuery}"`,
                url: window.location.href
            };

            if (navigator.share) {
                await navigator.share(shareData);
            } else {
                // Fallback: copy to clipboard
                await navigator.clipboard.writeText(shareData.url);
                alert('Link copied to clipboard!');
            }
        } catch (err) {
            console.error('Share failed:', err);
        }
    }, [searchQuery]);

    // Refresh data
    const handleRefresh = useCallback(() => {
        if (searchQuery) {
            handleSearch();
        }
    }, [searchQuery, handleSearch]);

    // Filter companies
    const filteredCompanies = useMemo(() => {
        if (!searchResults || searchResults.length === 0) return [];

        return searchResults.filter(company => {
            // Country filter
            if (filters.countries.length > 0 && !filters.countries.includes(company.country)) {
                return false;
            }

            // Risk score filter
            const riskScore = company.risk_score || 0;
            if (riskScore < filters.riskMin || riskScore > filters.riskMax) {
                return false;
            }

            // Legal form filter
            if (filters.legalForms.length > 0 && !filters.legalForms.includes(company.legal_form)) {
                return false;
            }

            return true;
        });
    }, [searchResults, filters]);

    return (
        <div className="min-h-screen bg-gradient-to-br from-black via-charcoal to-navy">
            {/* Header */}
            <header className="border-b border-gold/30 bg-black/80 backdrop-blur-md sticky top-0 z-50">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex items-center justify-between h-16">
                        {/* Logo and Title */}
                        <div className="flex items-center gap-4">
                            <div className="w-10 h-10 bg-gradient-to-br from-gold to-platinum rounded-lg flex items-center justify-center shadow-gold">
                                <Building2 size={24} className="text-black font-bold" />
                            </div>
                            <div>
                                <h1 className="text-xl font-bold text-gold">ILUMINATI SYSTEM</h1>
                                <p className="text-xs text-gray-400">Enhanced Business Intelligence</p>
                            </div>
                        </div>

                        {/* User Info */}
                        {isAuthenticated && (
                            <div className="flex items-center gap-4 text-sm">
                                <span className="text-gray-300">Welcome, {user?.name || user?.email}</span>
                                <div className="w-8 h-8 bg-gold rounded-full flex items-center justify-center text-black font-bold">
                                    {user?.name?.charAt(0) || user?.email?.charAt(0) || 'U'}
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Search Section */}
                <section className="mb-8">
                    <div className="bg-gradient-to-r from-gold/10 to-platinum/10 border border-gold/30 rounded-xl p-6 backdrop-blur-sm">
                        <div className="flex flex-col lg:flex-row gap-4 items-center">
                            <div className="flex-1 flex gap-2">
                                <div className="relative flex-1">
                                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gold" />
                                    <input
                                        type="text"
                                        placeholder="Search companies by name, IČO, or identifier..."
                                        value={searchQuery}
                                        onChange={(e) => setSearchQuery(e.target.value)}
                                        className="w-full pl-10 pr-4 py-3 bg-black/50 border border-gold/30 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-gold focus:ring-1 focus:ring-gold/50"
                                        onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                                    />
                                </div>
                                <button
                                    onClick={handleSearch}
                                    disabled={loading || !searchQuery.trim()}
                                    className="btn-premium disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    {loading ? (
                                        <>
                                            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-black mr-2"></div>
                                            Searching...
                                        </>
                                    ) : (
                                        'Search'
                                    )}
                                </button>
                            </div>

                            <div className="flex gap-2">
                                <button
                                    onClick={handleRefresh}
                                    className="p-3 border border-gold/30 rounded-lg text-gold hover:bg-gold/20 transition-all"
                                    title="Refresh Data"
                                >
                                    <RefreshCw size={20} />
                                </button>
                                <button
                                    onClick={handleShare}
                                    className="p-3 border border-gold/30 rounded-lg text-gold hover:bg-gold/20 transition-all"
                                    title="Share Results"
                                >
                                    <Share2 size={20} />
                                </button>
                                <button
                                    onClick={() => setActiveTab(activeTab === 'search' ? 'graph' : 'search')}
                                    className="p-3 border border-gold/30 rounded-lg text-gold hover:bg-gold/20 transition-all"
                                    title="Toggle View"
                                >
                                    <Globe size={20} />
                                </button>
                            </div>
                        </div>

                        {error && (
                            <div className="mt-4 p-3 bg-ruby/20 border border-ruby/30 rounded-lg text-ruby">
                                {error}
                            </div>
                        )}
                    </div>
                </section>

                {/* Dashboard Metrics */}
                {searchResults.length > 0 && (
                    <section className="mb-8">
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
                            <div className="card-premium">
                                <div className="flex items-center justify-between">
                                    <div>
                                        <p className="text-gray-400 text-sm">Total Companies</p>
                                        <p className="text-2xl font-bold text-gold">{dashboardMetrics.totalCompanies}</p>
                                    </div>
                                    <div className="w-12 h-12 bg-gold/20 rounded-lg flex items-center justify-center">
                                        <Building2 size={24} className="text-gold" />
                                    </div>
                                </div>
                            </div>

                            <div className="card-premium">
                                <div className="flex items-center justify-between">
                                    <div>
                                        <p className="text-gray-400 text-sm">Avg Risk Score</p>
                                        <p className="text-2xl font-bold text-{dashboardMetrics.avgRiskScore > 6 ? 'ruby' : 'emerald'}">
                                            {dashboardMetrics.avgRiskScore}
                                        </p>
                                    </div>
                                    <div className="w-12 h-12 bg-emerald/20 rounded-lg flex items-center justify-center">
                                        <TrendingUp size={24} className="text-emerald" />
                                    </div>
                                </div>
                            </div>

                            <div className="card-premium">
                                <div className="flex items-center justify-between">
                                    <div>
                                        <p className="text-gray-400 text-sm">High Risk</p>
                                        <p className="text-2xl font-bold text-ruby">{dashboardMetrics.highRiskCount}</p>
                                    </div>
                                    <div className="w-12 h-12 bg-ruby/20 rounded-lg flex items-center justify-center">
                                        <AlertTriangle size={24} className="text-ruby" />
                                    </div>
                                </div>
                            </div>

                            <div className="card-premium">
                                <div className="flex items-center justify-between">
                                    <div>
                                        <p className="text-gray-400 text-sm">Countries</p>
                                        <p className="text-2xl font-bold text-sapphire">{dashboardMetrics.countriesCount}</p>
                                    </div>
                                    <div className="w-12 h-12 bg-sapphire/20 rounded-lg flex items-center justify-center">
                                        <Globe size={24} className="text-sapphire" />
                                    </div>
                                </div>
                            </div>

                            <div className="card-premium">
                                <div className="flex items-center justify-between">
                                    <div>
                                        <p className="text-gray-400 text-sm">Relationships</p>
                                        <p className="text-2xl font-bold text-platinum">{dashboardMetrics.totalRelationships}</p>
                                    </div>
                                    <div className="w-12 h-12 bg-platinum/20 rounded-lg flex items-center justify-center">
                                        <Users size={24} className="text-platinum" />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </section>
                )}

                {/* Main Content Area */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Left Column - Search Results */}
                    <div className="lg:col-span-1">
                        <div className="card-premium">
                            <div className="flex items-center justify-between mb-4">
                                <h2 className="text-xl font-bold text-gold">Search Results</h2>
                                <div className="flex gap-2">
                                    <button
                                        onClick={() => setFilters(prev => ({ ...prev, riskMin: 0, riskMax: 10 }))}
                                        className="text-xs px-2 py-1 bg-gold/20 border border-gold/30 rounded text-gold hover:bg-gold/40"
                                    >
                                        Reset Filters
                                    </button>
                                </div>
                            </div>

                            {/* Filters */}
                            <div className="mb-4 p-3 bg-black/30 rounded-lg border border-gold/20">
                                <div className="flex items-center gap-2 mb-2">
                                    <Filter size={16} className="text-gold" />
                                    <span className="text-sm font-medium text-gold">Filters</span>
                                </div>
                                <div className="grid grid-cols-2 gap-2 text-xs">
                                    <label className="flex items-center gap-2">
                                        <input type="checkbox" defaultChecked className="form-checkbox text-gold" />
                                        <span>SK</span>
                                    </label>
                                    <label className="flex items-center gap-2">
                                        <input type="checkbox" defaultChecked className="form-checkbox text-gold" />
                                        <span>CZ</span>
                                    </label>
                                    <label className="flex items-center gap-2">
                                        <input type="checkbox" defaultChecked className="form-checkbox text-gold" />
                                        <span>PL</span>
                                    </label>
                                    <label className="flex items-center gap-2">
                                        <input type="checkbox" defaultChecked className="form-checkbox text-gold" />
                                        <span>HU</span>
                                    </label>
                                </div>
                            </div>

                            {/* Results List */}
                            <div className="space-y-3 max-h-96 overflow-y-auto">
                                {filteredCompanies.map((company, index) => (
                                    <div
                                        key={index}
                                        className={`p-3 border rounded-lg cursor-pointer transition-all hover:border-gold/50 ${selectedCompany?.identifier === company.identifier ? 'border-gold/70 bg-gold/5' : 'border-gold/20'
                                            }`}
                                        onClick={() => setSelectedCompany(company)}
                                    >
                                        <div className="flex items-center justify-between">
                                            <div>
                                                <h3 className="font-semibold text-white">{company.name}</h3>
                                                <p className="text-sm text-gray-400">{company.identifier} • {company.country}</p>
                                                <p className="text-xs text-gray-500">{company.legal_form}</p>
                                            </div>
                                            <div className="text-right">
                                                <div className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-bold ${(company.risk_score || 0) > 7 ? 'bg-ruby/20 text-ruby' :
                                                        (company.risk_score || 0) > 4 ? 'bg-amber/20 text-amber' : 'bg-emerald/20 text-emerald'
                                                    }`}>
                                                    Risk: {company.risk_score || 0}/10
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                ))}

                                {filteredCompanies.length === 0 && searchResults.length > 0 && (
                                    <div className="text-center text-gray-500 py-4">
                                        No results match your filters.
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>

                    {/* Right Column - Graph or Details */}
                    <div className="lg:col-span-2">
                        {activeTab === 'search' ? (
                            // Company Details
                            selectedCompany ? (
                                <div className="card-premium">
                                    <div className="flex items-center justify-between mb-4">
                                        <h2 className="text-xl font-bold text-gold">Company Details</h2>
                                        <div className="flex gap-2">
                                            <button
                                                onClick={() => handleExport('pdf')}
                                                className="btn-premium-secondary text-xs px-3 py-1"
                                            >
                                                <Download size={14} className="mr-1" /> PDF
                                            </button>
                                            <button
                                                onClick={() => handleExport('excel')}
                                                className="btn-premium-secondary text-xs px-3 py-1"
                                            >
                                                <Download size={14} className="mr-1" /> Excel
                                            </button>
                                        </div>
                                    </div>

                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        <div className="space-y-4">
                                            <div>
                                                <h3 className="text-sm font-medium text-gold mb-2">Basic Information</h3>
                                                <div className="space-y-2 text-sm">
                                                    <div className="flex justify-between">
                                                        <span className="text-gray-400">Name:</span>
                                                        <span className="text-white">{selectedCompany.name}</span>
                                                    </div>
                                                    <div className="flex justify-between">
                                                        <span className="text-gray-400">IČO:</span>
                                                        <span className="text-white">{selectedCompany.identifier}</span>
                                                    </div>
                                                    <div className="flex justify-between">
                                                        <span className="text-gray-400">Country:</span>
                                                        <span className="text-white">{selectedCompany.country}</span>
                                                    </div>
                                                    <div className="flex justify-between">
                                                        <span className="text-gray-400">Legal Form:</span>
                                                        <span className="text-white">{selectedCompany.legal_form}</span>
                                                    </div>
                                                    <div className="flex justify-between">
                                                        <span className="text-gray-400">Status:</span>
                                                        <span className="text-white">{selectedCompany.status}</span>
                                                    </div>
                                                </div>
                                            </div>

                                            <div>
                                                <h3 className="text-sm font-medium text-gold mb-2">Address</h3>
                                                <p className="text-sm text-white">{selectedCompany.address}</p>
                                            </div>
                                        </div>

                                        <div className="space-y-4">
                                            <div>
                                                <h3 className="text-sm font-medium text-gold mb-2">Key People</h3>
                                                <div className="space-y-2">
                                                    {selectedCompany.executives?.map((exec, index) => (
                                                        <div key={index} className="flex justify-between text-sm">
                                                            <span className="text-gray-400">Executive:</span>
                                                            <span className="text-white">{exec}</span>
                                                        </div>
                                                    ))}
                                                    {selectedCompany.shareholders?.map((shareholder, index) => (
                                                        <div key={index} className="flex justify-between text-sm">
                                                            <span className="text-gray-400">Shareholder:</span>
                                                            <span className="text-white">{shareholder}</span>
                                                        </div>
                                                    ))}
                                                </div>
                                            </div>

                                            <div>
                                                <h3 className="text-sm font-medium text-gold mb-2">Risk Assessment</h3>
                                                <div className="flex items-center gap-4">
                                                    <div className="text-3xl font-bold text-{selectedCompany.risk_score > 7 ? 'ruby' : selectedCompany.risk_score > 4 ? 'amber' : 'emerald'}">
                                                        {selectedCompany.risk_score}/10
                                                    </div>
                                                    <div className="flex-1 bg-gray-700 rounded-full h-2">
                                                        <div
                                                            className={`h-2 rounded-full ${selectedCompany.risk_score > 7 ? 'bg-ruby' :
                                                                    selectedCompany.risk_score > 4 ? 'bg-amber' : 'bg-emerald'
                                                                }`}
                                                            style={{ width: `${(selectedCompany.risk_score / 10) * 100}%` }}
                                                        ></div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ) : (
                                <div className="card-premium h-96 flex items-center justify-center text-gray-500">
                                    Select a company to view details
                                </div>
                            )
                        ) : (
                            // Network Graph
                            <div className="card-premium">
                                <div className="flex items-center justify-between mb-4">
                                    <h2 className="text-xl font-bold text-gold">Network Visualization</h2>
                                    <div className="flex gap-2">
                                        <button
                                            onClick={() => setActiveTab('search')}
                                            className="btn-premium-secondary text-xs px-3 py-1"
                                        >
                                            <Eye size={14} className="mr-1" /> View Details
                                        </button>
                                    </div>
                                </div>
                                <EnhancedForceGraph
                                    data={graphData}
                                    height={500}
                                    width={800}
                                    enableRealTime={true}
                                    showToolbar={true}
                                    enableExport={true}
                                    enableFilters={true}
                                    onNodeClick={(node) => {
                                        const company = searchResults.find(c => c.identifier === node.id);
                                        if (company) setSelectedCompany(company);
                                    }}
                                />
                            </div>
                        )}
                    </div>
                </div>
            </main>
        </div>
    );
};

export default EnhancedDashboard;