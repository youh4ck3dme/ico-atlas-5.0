import React, { useRef, useState, useCallback, useEffect, useMemo, forwardRef, useImperativeHandle } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import { Building2, User, MapPin, AlertTriangle, ZoomIn, ZoomOut, RotateCcw, Maximize2 } from 'lucide-react';
import { useTheater } from '../../contexts/TheaterContext';
import audioManager from '../../utils/AudioManager';
import '../../styles/theater.css';

const TheaterGraph = forwardRef((props, ref) => {
    const fgRef = useRef();
    const containerRef = useRef();

    // Expose fgRef to parent
    useImperativeHandle(ref, () => fgRef.current);

    const {
        filteredGraphData,
        centralNode,
        openNodeCard,
        isSearching
    } = useTheater();

    const [dimensions, setDimensions] = useState({ width: 800, height: 600 });
    const [showExplosion, setShowExplosion] = useState(false);
    const [explosionCenter, setExplosionCenter] = useState({ x: 400, y: 300 });

    // Transform edges to links format
    const graphData = useMemo(() => ({
        nodes: filteredGraphData.nodes || [],
        links: (filteredGraphData.edges || []).map(edge => ({
            source: edge.source,
            target: edge.target,
            type: edge.type || 'RELATED'
        }))
    }), [filteredGraphData]);

    // Update dimensions on resize
    useEffect(() => {
        const updateDimensions = () => {
            if (containerRef.current) {
                const rect = containerRef.current.getBoundingClientRect();
                setDimensions({ width: rect.width, height: Math.max(500, rect.height) });
            }
        };

        updateDimensions();
        window.addEventListener('resize', updateDimensions);
        return () => window.removeEventListener('resize', updateDimensions);
    }, []);

    // Explosion effect when new search completes
    useEffect(() => {
        if (centralNode && graphData.nodes.length > 0 && !isSearching) {
            setShowExplosion(true);
            setExplosionCenter({ x: dimensions.width / 2, y: dimensions.height / 2 });
            audioManager.playSwoosh();

            setTimeout(() => setShowExplosion(false), 1500);
        }
    }, [centralNode, graphData.nodes.length, isSearching, dimensions]);

    // Node color based on type and risk
    const getNodeColor = useCallback((node) => {
        if (!node || !node.type) return '#D4AF37';

        // Central node is always golden bright
        if (centralNode && node.id === centralNode.id) {
            return '#FFD700';
        }

        switch (node.type) {
            case 'company':
                return (node.risk_score || 0) > 5 ? '#ef4444' : '#D4AF37';
            case 'person':
                return '#60a5fa';
            case 'address':
                return '#34d399';
            case 'debt':
                return '#f87171';
            default:
                return '#D4AF37';
        }
    }, [centralNode]);

    // Node size based on type
    const getNodeSize = useCallback((node) => {
        if (!node || !node.type) return 8;

        // Central node is larger
        if (centralNode && node.id === centralNode.id) {
            return 18;
        }

        switch (node.type) {
            case 'company':
                return 12;
            case 'person':
                return 8;
            case 'address':
                return 6;
            case 'debt':
                return 10;
            default:
                return 8;
        }
    }, [centralNode]);

    // Link color based on type
    const getLinkColor = useCallback((link) => {
        if (!link) return 'rgba(212, 175, 55, 0.5)';
        const linkType = link.type || 'RELATED';
        switch (linkType) {
            case 'OWNED_BY':
                return 'rgba(212, 175, 55, 0.7)';
            case 'MANAGED_BY':
                return 'rgba(96, 165, 250, 0.7)';
            case 'LOCATED_AT':
                return 'rgba(52, 211, 153, 0.7)';
            case 'HAS_DEBT':
                return 'rgba(239, 68, 68, 0.8)';
            default:
                return 'rgba(212, 175, 55, 0.5)';
        }
    }, []);

    // Custom node canvas drawing
    const drawNode = useCallback((node, ctx, globalScale) => {
        const size = getNodeSize(node);
        const color = getNodeColor(node);
        const isCentral = centralNode && node.id === centralNode.id;

        // Glow effect for central and high-risk nodes
        if (isCentral || (node.risk_score || 0) > 5) {
            ctx.shadowColor = color;
            ctx.shadowBlur = isCentral ? 20 : 12;
        }

        // Draw main circle
        ctx.beginPath();
        ctx.arc(node.x, node.y, size, 0, 2 * Math.PI);
        ctx.fillStyle = color;
        ctx.fill();

        // Inner circle for depth
        ctx.beginPath();
        ctx.arc(node.x, node.y, size * 0.6, 0, 2 * Math.PI);
        ctx.fillStyle = isCentral ? '#0A0A0A' : 'rgba(0, 0, 0, 0.3)';
        ctx.fill();

        // Reset shadow
        ctx.shadowColor = 'transparent';
        ctx.shadowBlur = 0;

        // Draw label if zoomed in enough
        if (globalScale > 0.8) {
            const label = node.label || node.id;
            const fontSize = Math.max(10, 12 / globalScale);
            ctx.font = `${fontSize}px 'Courier New', monospace`;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'top';
            ctx.fillStyle = '#ffffff';
            ctx.fillText(label.substring(0, 20), node.x, node.y + size + 4);
        }
    }, [getNodeColor, getNodeSize, centralNode]);

    // Handle node click
    const handleNodeClick = useCallback((node) => {
        if (node) {
            audioManager.playClick();
            openNodeCard(node);
        }
    }, [openNodeCard]);

    // Handle node hover
    const handleNodeHover = useCallback((node) => {
        document.body.style.cursor = node ? 'pointer' : 'default';
        if (node) {
            audioManager.playBeep();
        }
    }, []);

    // Zoom controls
    const handleZoomIn = useCallback(() => {
        if (fgRef.current) {
            fgRef.current.zoom(1.5, 300);
            audioManager.playClick();
        }
    }, []);

    const handleZoomOut = useCallback(() => {
        if (fgRef.current) {
            fgRef.current.zoom(0.75, 300);
            audioManager.playClick();
        }
    }, []);

    const handleReset = useCallback(() => {
        if (fgRef.current) {
            fgRef.current.zoomToFit(400);
            audioManager.playClick();
        }
    }, []);

    const handleFullscreen = useCallback(() => {
        if (containerRef.current) {
            if (document.fullscreenElement) {
                document.exitFullscreen();
            } else {
                containerRef.current.requestFullscreen();
            }
            audioManager.playClick();
        }
    }, []);

    // Graph engine stop handler
    const handleEngineStop = useCallback(() => {
        if (fgRef.current && graphData.nodes.length > 0) {
            fgRef.current.zoomToFit(400, 50);
        }
    }, [graphData.nodes.length]);

    if (!graphData.nodes.length) {
        return (
            <div className="theater-graph-container" ref={containerRef} style={{ minHeight: '500px' }}>
                <div className="flex items-center justify-center h-full text-center p-8">
                    <div>
                        <Building2 size={64} className="mx-auto mb-4 text-[#D4AF37] opacity-30" />
                        <p className="text-[#D4AF37] font-mono text-lg opacity-50">
                            Zadajte IČO alebo názov firmy pre zobrazenie vzťahov
                        </p>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="theater-graph-container" ref={containerRef} style={{ minHeight: '500px', position: 'relative' }}>
            {/* Toolbar */}
            <div className="absolute top-4 right-4 z-10 flex gap-2">
                <button
                    onClick={handleZoomIn}
                    className="p-2 bg-[#0A0A0A]/80 backdrop-blur-md border border-[#D4AF37]/30 rounded-lg text-[#D4AF37] hover:bg-[#D4AF37]/20 transition-all"
                    title="Priblížiť"
                >
                    <ZoomIn size={18} />
                </button>
                <button
                    onClick={handleZoomOut}
                    className="p-2 bg-[#0A0A0A]/80 backdrop-blur-md border border-[#D4AF37]/30 rounded-lg text-[#D4AF37] hover:bg-[#D4AF37]/20 transition-all"
                    title="Oddialiť"
                >
                    <ZoomOut size={18} />
                </button>
                <button
                    onClick={handleReset}
                    className="p-2 bg-[#0A0A0A]/80 backdrop-blur-md border border-[#D4AF37]/30 rounded-lg text-[#D4AF37] hover:bg-[#D4AF37]/20 transition-all"
                    title="Resetovať pohľad"
                >
                    <RotateCcw size={18} />
                </button>
                <button
                    onClick={handleFullscreen}
                    className="p-2 bg-[#0A0A0A]/80 backdrop-blur-md border border-[#D4AF37]/30 rounded-lg text-[#D4AF37] hover:bg-[#D4AF37]/20 transition-all"
                    title="Celá obrazovka"
                >
                    <Maximize2 size={18} />
                </button>
            </div>

            {/* Network Explosion Effect */}
            {showExplosion && (
                <div className="network-explosion" style={{ left: explosionCenter.x, top: explosionCenter.y }}>
                    {[...Array(12)].map((_, i) => (
                        <div
                            key={i}
                            className="explosion-ray"
                            style={{
                                transform: `rotate(${i * 30}deg)`,
                                animationDelay: `${i * 0.05}s`
                            }}
                        />
                    ))}
                </div>
            )}

            {/* Central Node Pulse */}
            {centralNode && (
                <div
                    className="central-node-pulse"
                    style={{
                        left: explosionCenter.x - 20,
                        top: explosionCenter.y - 20,
                        width: 40,
                        height: 40
                    }}
                />
            )}

            {/* Force Graph */}
            <ForceGraph2D
                ref={fgRef}
                graphData={graphData}
                nodeCanvasObject={drawNode}
                nodePointerAreaPaint={(node, color, ctx) => {
                    ctx.beginPath();
                    ctx.arc(node.x, node.y, getNodeSize(node) + 5, 0, 2 * Math.PI);
                    ctx.fillStyle = color;
                    ctx.fill();
                }}
                linkColor={getLinkColor}
                linkWidth={2}
                linkDirectionalArrowLength={6}
                linkDirectionalArrowRelPos={1}
                linkCurvature={0.2}
                onNodeClick={handleNodeClick}
                onNodeHover={handleNodeHover}
                cooldownTicks={100}
                onEngineStop={handleEngineStop}
                backgroundColor="transparent"
                width={dimensions.width}
                height={dimensions.height}
                d3AlphaDecay={0.02}
                d3VelocityDecay={0.3}
            />

            {/* Legend */}
            <div className="absolute bottom-4 left-4 flex gap-4 p-3 bg-[#0A0A0A]/80 backdrop-blur-md border border-[#D4AF37]/30 rounded-lg">
                <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-[#D4AF37]" />
                    <span className="text-xs text-gray-400 font-mono">Firma</span>
                </div>
                <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-[#60a5fa]" />
                    <span className="text-xs text-gray-400 font-mono">Osoba</span>
                </div>
                <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-[#34d399]" />
                    <span className="text-xs text-gray-400 font-mono">Adresa</span>
                </div>
                <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-[#ef4444]" />
                    <span className="text-xs text-gray-400 font-mono">Riziko</span>
                </div>
            </div>
        </div>
    );
});

TheaterGraph.displayName = 'TheaterGraph';

export default TheaterGraph;
