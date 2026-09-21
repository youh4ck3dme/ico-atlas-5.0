import React, { useRef, useState, useCallback, useEffect, memo } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import {
    Building2, User, MapPin, AlertTriangle,
    ZoomIn, ZoomOut, RotateCcw, Download,
    Eye, EyeOff, Filter, Search,
    Plus, Minus, Maximize, Minimize,
    Share2, FileText, Settings
} from 'lucide-react';

const EnhancedForceGraph = ({
    data,
    onNodeClick,
    onNodeHover,
    height = 600,
    width = 800,
    enableRealTime = true,
    showToolbar = true,
    enableExport = true,
    enableFilters = true
}) => {
    const fgRef = useRef();
    const [filters, setFilters] = useState({
        showCompanies: true,
        showPersons: true,
        showAddresses: true,
        showDebts: true,
        minRiskScore: 0,
        maxRiskScore: 10
    });
    const [searchQuery, setSearchQuery] = useState('');
    const [isFullscreen, setIsFullscreen] = useState(false);
    const [graphSettings, setGraphSettings] = useState({
        nodeSize: 8,
        linkDistance: 100,
        charge: -300,
        friction: 0.9,
        gravity: 0.1
    });
    const [isPlaying, setIsPlaying] = useState(true);

    // Node styling with luxury aesthetics
    const getNodeColor = useCallback((node) => {
        if (!node || !node.type) return '#D4AF37';

        // Highlight selected/highlighted nodes
        if (node.selected) return '#FFFFFF';
        if (node.highlighted) return '#FFD700';

        switch (node.type) {
            case 'company':
                return node.risk_score > 7 ? '#EF4444' : '#D4AF37'; // Red for high risk, Gold for normal
            case 'person':
                return '#60A5FA'; // Sapphire Blue
            case 'address':
                return '#34D399'; // Emerald Green
            case 'debt':
                return '#F87171'; // Ruby Red
            default:
                return '#D4AF37';
        }
    }, []);

    const getNodeSize = useCallback((node) => {
        if (!node) return 8;

        let baseSize = 8;
        if (node.type === 'company') baseSize = 12;
        if (node.type === 'debt') baseSize = 10;
        if (node.selected) baseSize += 4;
        if (node.highlighted) baseSize += 2;

        // Size based on connections
        const connectionBonus = (node.connections || 0) * 0.5;
        return baseSize + connectionBonus;
    }, []);

    const getNodeCanvasObject = useCallback((node, ctx, globalScale) => {
        if (!node) return;

        const label = node.label || node.id;
        const fontSize = 12 / globalScale;
        const textWidth = ctx.measureText(label).width;
        const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.2);

        // Draw node with gradient
        const radius = getNodeSize(node);
        const gradient = ctx.createRadialGradient(node.x, node.y - radius / 2, 0, node.x, node.y, radius);

        if (node.type === 'company') {
            gradient.addColorStop(0, '#FFF7E6');
            gradient.addColorStop(1, getNodeColor(node));
        } else {
            gradient.addColorStop(0, '#FFFFFF');
            gradient.addColorStop(1, getNodeColor(node));
        }

        ctx.beginPath();
        ctx.arc(node.x, node.y, radius, 0, 2 * Math.PI, false);
        ctx.fillStyle = gradient;
        ctx.fill();

        // Add glow effect for high-risk nodes
        if (node.risk_score > 7) {
            ctx.shadowColor = '#EF4444';
            ctx.shadowBlur = 15;
        } else if (node.type === 'company') {
            ctx.shadowColor = '#D4AF37';
            ctx.shadowBlur = 8;
        } else {
            ctx.shadowBlur = 0;
        }

        // Draw risk score indicator
        if (node.risk_score !== undefined && node.risk_score > 0) {
            ctx.beginPath();
            ctx.arc(node.x + radius - 2, node.y + radius - 2, 4, 0, 2 * Math.PI);
            ctx.fillStyle = node.risk_score > 7 ? '#EF4444' : '#FBBF24';
            ctx.fill();
        }

        // Draw label
        ctx.shadowBlur = 0;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillStyle = '#FFFFFF';
        ctx.font = `${fontSize}px Inter`;
        ctx.fillText(label, node.x, node.y + radius + 15);

        // Draw connection count
        if (node.connections > 0) {
            ctx.font = `${fontSize * 0.8}px Inter`;
            ctx.fillStyle = '#9CA3AF';
            ctx.fillText(`${node.connections} connections`, node.x, node.y + radius + 30);
        }
    }, [getNodeSize, getNodeColor]);

    // Edge styling
    const getEdgeColor = useCallback((edge) => {
        if (!edge) return '#D4AF37';

        switch (edge.type) {
            case 'OWNED_BY': return '#D4AF37';
            case 'MANAGED_BY': return '#60A5FA';
            case 'LOCATED_AT': return '#34D399';
            case 'HAS_DEBT': return '#EF4444';
            default: return '#D4AF37';
        }
    }, []);

    const getEdgeWidth = useCallback((edge) => {
        if (!edge) return 2;
        return Math.max(1, edge.weight || 2);
    }, []);

    // Filter data
    const filteredData = React.useMemo(() => {
        if (!data || !data.nodes) return { nodes: [], edges: [] };

        const filteredNodes = data.nodes.filter(node => {
            if (!node) return false;

            // Type filter
            if (node.type === 'company' && !filters.showCompanies) return false;
            if (node.type === 'person' && !filters.showPersons) return false;
            if (node.type === 'address' && !filters.showAddresses) return false;
            if (node.type === 'debt' && !filters.showDebts) return false;

            // Risk score filter
            if (node.risk_score < filters.minRiskScore || node.risk_score > filters.maxRiskScore) return false;

            // Search filter
            if (searchQuery && !node.label.toLowerCase().includes(searchQuery.toLowerCase())) return false;

            return true;
        });

        const filteredEdges = data.edges.filter(edge => {
            if (!edge) return false;
            const sourceNode = filteredNodes.find(n => n.id === edge.source);
            const targetNode = filteredNodes.find(n => n.id === edge.target);
            return sourceNode && targetNode;
        });

        return { nodes: filteredNodes, edges: filteredEdges };
    }, [data, filters, searchQuery]);

    // Toolbar component
    const Toolbar = () => (
        <div className="absolute top-4 right-4 z-10 flex flex-col gap-3 bg-black/60 backdrop-blur-md p-4 rounded-xl border border-gold/30 shadow-xl">
            {/* Zoom controls */}
            <div className="flex gap-2">
                <button
                    onClick={() => fgRef.current?.zoom(1.5, 200)}
                    className="p-2 bg-gold/20 border border-gold/30 rounded-lg text-gold hover:bg-gold/40 transition-all hover:scale-110"
                    title="Zoom In"
                >
                    <Plus size={18} />
                </button>
                <button
                    onClick={() => fgRef.current?.zoom(0.75, 200)}
                    className="p-2 bg-gold/20 border border-gold/30 rounded-lg text-gold hover:bg-gold/40 transition-all hover:scale-110"
                    title="Zoom Out"
                >
                    <Minus size={18} />
                </button>
                <button
                    onClick={() => fgRef.current?.zoomToFit(400)}
                    className="p-2 bg-gold/20 border border-gold/30 rounded-lg text-gold hover:bg-gold/40 transition-all hover:scale-110"
                    title="Fit to Screen"
                >
                    <RotateCcw size={18} />
                </button>
            </div>

            {/* Play/Pause controls */}
            <div className="flex gap-2">
                <button
                    onClick={() => setIsPlaying(!isPlaying)}
                    className={`p-2 border rounded-lg transition-all hover:scale-110 ${isPlaying
                            ? 'bg-emerald/20 border-emerald/30 text-emerald'
                            : 'bg-gray/20 border-gray/30 text-gray'
                        }`}
                    title={isPlaying ? "Pause Physics" : "Resume Physics"}
                >
                    {isPlaying ? '⏸️' : '▶️'}
                </button>
            </div>

            {/* Export controls */}
            {enableExport && (
                <div className="flex gap-2">
                    <button
                        onClick={() => {
                            const canvas = fgRef.current?.getGraphCanvas();
                            if (canvas) {
                                const link = document.createElement('a');
                                link.download = 'network-graph.png';
                                link.href = canvas.toDataURL('image/png');
                                link.click();
                            }
                        }}
                        className="p-2 bg-emerald/20 border border-emerald/30 rounded-lg text-emerald hover:bg-emerald/40 transition-all hover:scale-110"
                        title="Export PNG"
                    >
                        <Download size={18} />
                    </button>
                    <button
                        onClick={() => {
                            // Export to SVG for high quality
                            const svg = fgRef.current?.getGraphSVG();
                            if (svg) {
                                const blob = new Blob([svg], { type: 'image/svg+xml' });
                                const url = URL.createObjectURL(blob);
                                const link = document.createElement('a');
                                link.download = 'network-graph.svg';
                                link.href = url;
                                link.click();
                                URL.revokeObjectURL(url);
                            }
                        }}
                        className="p-2 bg-sapphire/20 border border-sapphire/30 rounded-lg text-sapphire hover:bg-sapphire/40 transition-all hover:scale-110"
                        title="Export SVG"
                    >
                        <FileText size={18} />
                    </button>
                </div>
            )}

            {/* Fullscreen toggle */}
            <div className="flex gap-2">
                <button
                    onClick={() => setIsFullscreen(!isFullscreen)}
                    className="p-2 bg-platinum/20 border border-platinum/30 rounded-lg text-platinum hover:bg-platinum/40 transition-all hover:scale-110"
                    title={isFullscreen ? "Exit Fullscreen" : "Enter Fullscreen"}
                >
                    {isFullscreen ? <Minimize size={18} /> : <Maximize size={18} />}
                </button>
            </div>

            {/* Settings */}
            <div className="flex gap-2">
                <button
                    onClick={() => {
                        // Open settings modal or panel
                        console.log('Settings clicked');
                    }}
                    className="p-2 bg-navy/20 border border-navy/30 rounded-lg text-navy hover:bg-navy/40 transition-all hover:scale-110"
                    title="Graph Settings"
                >
                    <Settings size={18} />
                </button>
            </div>
        </div>
    );

    // Filter panel component
    const FilterPanel = () => (
        <div className="absolute top-4 left-4 z-10 bg-black/60 backdrop-blur-md p-4 rounded-xl border border-gold/30 shadow-xl">
            {/* Search */}
            <div className="mb-4">
                <div className="flex items-center gap-2 bg-gold/10 border border-gold/30 rounded-lg p-2">
                    <Search size={18} className="text-gold" />
                    <input
                        type="text"
                        placeholder="Search nodes..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="bg-transparent text-white placeholder-gray-400 border-none outline-none flex-1"
                    />
                </div>
            </div>

            {/* Type filters */}
            <div className="space-y-2">
                <label className="text-sm font-medium text-gold">Node Types</label>
                <div className="grid grid-cols-2 gap-2">
                    <label className="flex items-center gap-2 cursor-pointer">
                        <input
                            type="checkbox"
                            checked={filters.showCompanies}
                            onChange={(e) => setFilters(prev => ({ ...prev, showCompanies: e.target.checked }))}
                            className="form-checkbox text-gold"
                        />
                        <Building2 size={16} className="text-gold" />
                        <span className="text-sm">Companies</span>
                    </label>
                    <label className="flex items-center gap-2 cursor-pointer">
                        <input
                            type="checkbox"
                            checked={filters.showPersons}
                            onChange={(e) => setFilters(prev => ({ ...prev, showPersons: e.target.checked }))}
                            className="form-checkbox text-sapphire"
                        />
                        <User size={16} className="text-sapphire" />
                        <span className="text-sm">Persons</span>
                    </label>
                    <label className="flex items-center gap-2 cursor-pointer">
                        <input
                            type="checkbox"
                            checked={filters.showAddresses}
                            onChange={(e) => setFilters(prev => ({ ...prev, showAddresses: e.target.checked }))}
                            className="form-checkbox text-emerald"
                        />
                        <MapPin size={16} className="text-emerald" />
                        <span className="text-sm">Addresses</span>
                    </label>
                    <label className="flex items-center gap-2 cursor-pointer">
                        <input
                            type="checkbox"
                            checked={filters.showDebts}
                            onChange={(e) => setFilters(prev => ({ ...prev, showDebts: e.target.checked }))}
                            className="form-checkbox text-ruby"
                        />
                        <AlertTriangle size={16} className="text-ruby" />
                        <span className="text-sm">Debts</span>
                    </label>
                </div>
            </div>

            {/* Risk score filter */}
            <div className="mt-4">
                <label className="text-sm font-medium text-gold mb-2 block">Risk Score Range</label>
                <div className="flex gap-2 text-sm">
                    <span>{filters.minRiskScore}</span>
                    <input
                        type="range"
                        min="0"
                        max="10"
                        step="1"
                        value={filters.minRiskScore}
                        onChange={(e) => setFilters(prev => ({ ...prev, minRiskScore: parseInt(e.target.value) }))}
                        className="flex-1"
                    />
                    <span>{filters.maxRiskScore}</span>
                </div>
            </div>
        </div>
    );

    // Graph interaction handlers
    const handleNodeClick = useCallback((node) => {
        if (onNodeClick) {
            onNodeClick(node);
        }

        // Highlight clicked node and its connections
        if (fgRef.current) {
            const graph = fgRef.current;
            const nodes = graph.graphData().nodes;

            nodes.forEach(n => {
                n.highlighted = (n.id === node.id);
            });

            graph.refresh();
        }
    }, [onNodeClick]);

    const handleNodeHover = useCallback((node) => {
        if (onNodeHover) {
            onNodeHover(node);
        }

        // Change cursor style
        document.body.style.cursor = node ? 'pointer' : 'default';
    }, [onNodeHover]);

    // Initialize graph settings
    useEffect(() => {
        if (fgRef.current) {
            const graph = fgRef.current;

            // Apply physics settings
            graph.d3Force('link').distance(graphSettings.linkDistance);
            graph.d3Force('charge').strength(graphSettings.charge);
            graph.d3Force('friction').constant(graphSettings.friction);
            graph.d3Force('gravity').constant(graphSettings.gravity);

            // Pause/resume physics
            if (isPlaying) {
                graph.d3ReheatSimulation();
            } else {
                graph.d3AlphaTarget(0);
            }
        }
    }, [graphSettings, isPlaying]);

    // Cleanup
    useEffect(() => {
        return () => {
            document.body.style.cursor = 'default';
        };
    }, []);

    return (
        <div className="relative border-2 border-gold/30 rounded-xl bg-gradient-to-br from-black via-charcoal to-navy shadow-2xl overflow-hidden">
            {/* Filter Panel */}
            {enableFilters && <FilterPanel />}

            {/* Toolbar */}
            {showToolbar && <Toolbar />}

            {/* Graph */}
            <ForceGraph2D
                ref={fgRef}
                graphData={filteredData}
                nodeLabel={(node) => `${node.label || node.id}\n${node.type || 'unknown'} • Risk: ${node.risk_score || 0}/10`}
                nodeColor={getNodeColor}
                nodeVal={getNodeSize}
                nodeCanvasObject={getNodeCanvasObject}
                nodeRelSize={6}
                linkColor={(link) => getEdgeColor(link)}
                linkWidth={getEdgeWidth}
                linkDirectionalArrowLength={6}
                linkDirectionalArrowRelPos={1}
                linkCurvature={0.25}
                onNodeClick={handleNodeClick}
                onNodeHover={handleNodeHover}
                cooldownTicks={isPlaying ? 100 : 0}
                onEngineStop={() => {
                    if (fgRef.current && isPlaying) {
                        fgRef.current.zoomToFit(400);
                    }
                }}
                backgroundColor="transparent"
                width={width}
                height={height}
                d3VelocityDecay={graphSettings.friction}
                d3Force="charge"
                enablePointerInteraction={true}
                enableZoomInteraction={true}
                enablePanInteraction={true}
            />

            {/* Status indicator */}
            <div className="absolute bottom-4 left-4 text-xs text-gray-400">
                {filteredData.nodes.length} nodes • {filteredData.edges.length} connections
                {isPlaying ? ' • Physics running' : ' • Physics paused'}
            </div>

            {/* Legend */}
            <div className="absolute bottom-4 right-4 bg-black/50 backdrop-blur-md p-3 rounded-lg border border-gold/30 text-xs">
                <div className="grid grid-cols-2 gap-2 text-gray-300">
                    <div className="flex items-center gap-2">
                        <div className="w-3 h-3 bg-gold rounded-full"></div>
                        <span>Company</span>
                    </div>
                    <div className="flex items-center gap-2">
                        <div className="w-3 h-3 bg-sapphire rounded-full"></div>
                        <span>Person</span>
                    </div>
                    <div className="flex items-center gap-2">
                        <div className="w-3 h-3 bg-emerald rounded-full"></div>
                        <span>Address</span>
                    </div>
                    <div className="flex items-center gap-2">
                        <div className="w-3 h-3 bg-ruby rounded-full"></div>
                        <span>Debt</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default memo(EnhancedForceGraph);