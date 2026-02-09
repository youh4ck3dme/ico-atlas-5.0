import React, { useRef, useState, useCallback, useEffect, memo } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import {
    Maximize, Minimize, ZoomIn, ZoomOut, RotateCcw,
    Layers, Search, Filter, Settings, Share2, Download, Route, Crosshair
} from 'lucide-react';
import html2canvas from 'html2canvas';
import InspectorPanel from './InspectorPanel';
import GraphContextMenu from './GraphContextMenu';
import GraphControls from './GraphControls';

// --- 3D ICON PATHS (Canvas Calls) ---
const drawIsometricBuilding = (ctx, x, y, size, color) => {
    const topColor = adjustColor(color, 40);
    const sideColor1 = color;
    const sideColor2 = adjustColor(color, -20);

    const h = size;
    const w = size * 0.8;

    // Top Face
    ctx.beginPath();
    ctx.moveTo(x, y - h);
    ctx.lineTo(x + w, y - h - w / 2);
    ctx.lineTo(x, y - h - w);
    ctx.lineTo(x - w, y - h - w / 2);
    ctx.closePath();
    ctx.fillStyle = topColor;
    ctx.fill();
    ctx.strokeStyle = 'rgba(255,255,255,0.2)';
    ctx.stroke();

    // Right Face
    ctx.beginPath();
    ctx.moveTo(x, y - h);
    ctx.lineTo(x + w, y - h - w / 2);
    ctx.lineTo(x + w, y - w / 2);
    ctx.lineTo(x, y);
    ctx.closePath();
    ctx.fillStyle = sideColor2;
    ctx.fill();
    ctx.stroke();

    // Left Face
    ctx.beginPath();
    ctx.moveTo(x, y - h);
    ctx.lineTo(x - w, y - h - w / 2);
    ctx.lineTo(x - w, y - w / 2);
    ctx.lineTo(x, y);
    ctx.closePath();
    ctx.fillStyle = sideColor1;
    ctx.fill();
    ctx.stroke();
};

const drawAvatar = (ctx, x, y, size, color) => {
    // Head -> Sphere gradient
    const gradient = ctx.createRadialGradient(x, y - size / 2, size / 5, x, y - size / 2, size);
    gradient.addColorStop(0, '#ffffff');
    gradient.addColorStop(1, color);

    ctx.beginPath();
    ctx.arc(x, y - size / 2, size / 0.8, 0, Math.PI * 2);
    ctx.fillStyle = gradient;
    ctx.fill();

    // Shoulders
    ctx.beginPath();
    ctx.arc(x, y + size, size * 1.2, Math.PI, 0); // half circle upside down
    ctx.fillStyle = adjustColor(color, -20);
    ctx.fill();
};

const drawShield = (ctx, x, y, size, color) => {
    ctx.beginPath();
    ctx.moveTo(x, y - size); // Top point
    ctx.bezierCurveTo(x + size, y - size, x + size, y, x, y + size * 1.2); // Right curve
    ctx.bezierCurveTo(x - size, y, x - size, y - size, x, y - size); // Left curve
    ctx.closePath();

    const gradient = ctx.createLinearGradient(x - size, y - size, x + size, y + size);
    gradient.addColorStop(0, color);
    gradient.addColorStop(1, adjustColor(color, -40));

    ctx.fillStyle = gradient;
    ctx.fill();
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 1;
    ctx.stroke();

    // Warning Symbol
    ctx.fillStyle = '#ffffff';
    ctx.font = `bold ${size}px serif`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('!', x, y);
};

// Utils
const adjustColor = (color, amount) => {
    return '#' + color.replace(/^#/, '').replace(/../g, color => ('0' + Math.min(255, Math.max(0, parseInt(color, 16) + amount)).toString(16)).substr(-2));
}

const NexusGraph = ({
    data,
    onNodeClick,
    width = 800,
    height = 600,
    enableRealTime = true
}) => {
    const fgRef = useRef();
    const [isFullscreen, setIsFullscreen] = useState(false);
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedNode, setSelectedNode] = useState(null);
    const [contextMenu, setContextMenu] = useState(null);
    const [filters, setFilters] = useState({
        showCompanies: true,
        showPeople: true,
        showRisks: true
    });

    // --- FOCUS MODE STATE ---
    const [focusMode, setFocusMode] = useState(false);

    // --- PATHFINDING STATE ---
    const [pathMode, setPathMode] = useState(false);
    const [pathStart, setPathStart] = useState(null);
    const [pathEnd, setPathEnd] = useState(null);
    const [shortestPath, setShortestPath] = useState({ nodes: new Set(), links: new Set() });

    // --- PATHFINDING ALGORITHM (BFS) ---
    useEffect(() => {
        if (!pathStart || !pathEnd || !data) {
            setShortestPath({ nodes: new Set(), links: new Set() });
            return;
        }

        const queue = [[pathStart.id]];
        const visited = new Set([pathStart.id]);
        const parent = {};

        let found = false;
        while (queue.length > 0) {
            const path = queue.shift();
            const node = path[path.length - 1];

            if (node === pathEnd.id) {
                found = true;
                break;
            }

            const neighbors = data.edges
                .filter(e => {
                    const s = typeof e.source === 'object' ? e.source.id : e.source;
                    const t = typeof e.target === 'object' ? e.target.id : e.target;
                    return s === node || t === node;
                })
                .map(e => {
                    const s = typeof e.source === 'object' ? e.source.id : e.source;
                    const t = typeof e.target === 'object' ? e.target.id : e.target;
                    return s === node ? t : s;
                });

            for (const neighbor of neighbors) {
                if (!visited.has(neighbor)) {
                    visited.add(neighbor);
                    parent[neighbor] = node;
                    queue.push([...path, neighbor]);
                }
            }
        }

        if (found) {
            const pathNodes = new Set();
            const pathLinks = new Set();
            let curr = pathEnd.id;
            pathNodes.add(curr);

            while (curr !== pathStart.id) {
                const prev = parent[curr];
                pathNodes.add(prev);

                // Find link
                const link = data.edges.find(e => {
                    const s = typeof e.source === 'object' ? e.source.id : e.source;
                    const t = typeof e.target === 'object' ? e.target.id : e.target;
                    return (s === curr && t === prev) || (s === prev && t === curr);
                });
                if (link) pathLinks.add(link);

                curr = prev;
            }
            setShortestPath({ nodes: pathNodes, links: pathLinks });
        } else {
            setShortestPath({ nodes: new Set(), links: new Set() });
        }

    }, [pathStart, pathEnd, data]);

    // --- FILTERED DATA ---
    const filteredData = React.useMemo(() => {
        if (!data) return { nodes: [], links: [] };

        // --- FOCUS MODE LOGIC ---
        if (focusMode && selectedNode) {
            const neighborIds = new Set();
            neighborIds.add(selectedNode.id);

            data.edges.forEach(link => {
                const s = typeof link.source === 'object' ? link.source.id : link.source;
                const t = typeof link.target === 'object' ? link.target.id : link.target;
                if (s === selectedNode.id) neighborIds.add(t);
                if (t === selectedNode.id) neighborIds.add(s);
            });

            const validNodes = data.nodes.filter(n => neighborIds.has(n.id));
            const validLinks = data.edges.filter(link => {
                const s = typeof link.source === 'object' ? link.source.id : link.source;
                const t = typeof link.target === 'object' ? link.target.id : link.target;
                return neighborIds.has(s) && neighborIds.has(t);
            });
            return { nodes: validNodes, links: validLinks };
        }

        const validNodes = data.nodes.filter(node => {
            if (node.type === 'company' && !filters.showCompanies) return false;
            if (node.type === 'person' && !filters.showPeople) return false;
            if (node.type === 'debt' && !filters.showRisks) return false; // Assuming 'debt' is risk for now
            if (searchQuery && !node.label.toLowerCase().includes(searchQuery.toLowerCase())) return false;
            return true;
        });

        const nodeIds = new Set(validNodes.map(n => n.id));
        const validLinks = data.edges.filter(link =>
            nodeIds.has(typeof link.source === 'object' ? link.source.id : link.source) &&
            nodeIds.has(typeof link.target === 'object' ? link.target.id : link.target)
        );

        return { nodes: validNodes, links: validLinks };
    }, [data, filters, searchQuery, focusMode, selectedNode]);

    // --- NODE CANVAS RENDERER ---
    const nodeCanvasObject = useCallback((node, ctx, globalScale) => {
        const label = node.label || node.id;
        const fontSize = 12 / globalScale;

        const isPathNode = shortestPath.nodes.has(node.id);
        const isStart = pathStart?.id === node.id;
        const isEnd = pathEnd?.id === node.id;

        let size = node.val ? node.val : (node.type === 'company' ? 8 : 5);
        if (node.id === selectedNode?.id || isPathNode) size *= 1.5; // Highlight selected or path

        let colorOverride = null;
        if (isStart) colorOverride = '#10b981'; // Green Start
        if (isEnd) colorOverride = '#f43f5e'; // Rose End
        if (isPathNode && !isStart && !isEnd) colorOverride = '#a855f7'; // Purple Path

        if (node.type === 'company') {
            drawIsometricBuilding(ctx, node.x, node.y, size * 0.8, colorOverride || '#D4AF37'); // Gold
        } else if (node.type === 'person') {
            drawAvatar(ctx, node.x, node.y, size * 0.6, colorOverride || '#3b82f6'); // Blue
        } else if (node.risk_score > 7) {
            drawShield(ctx, node.x, node.y, size * 0.8, colorOverride || '#ef4444'); // Red
        } else {
            // Fallback sphere
            ctx.beginPath();
            ctx.arc(node.x, node.y, size, 0, 2 * Math.PI, false);
            ctx.fillStyle = colorOverride || '#94a3b8';
            ctx.fill();
        }

        // Label on Zoom or Hover or Path
        if (globalScale > 1.2 || node.highlighted || node.id === selectedNode?.id || isPathNode) {
            ctx.font = `${fontSize}px 'Inter', sans-serif`;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillStyle = isPathNode ? '#fff' : 'rgba(255, 255, 255, 0.9)';

            if (isPathNode) {
                ctx.shadowColor = '#a855f7';
                ctx.shadowBlur = 10;
            } else {
                ctx.shadowColor = 'black';
                ctx.shadowBlur = 4;
            }

            ctx.fillText(label, node.x, node.y + size + 8);
            ctx.shadowBlur = 0;
        }
    }, [selectedNode, shortestPath, pathStart, pathEnd]);

    const handleNodeClickInternal = useCallback((node) => {
        if (pathMode) {
            if (!pathStart) {
                setPathStart(node);
            } else if (!pathEnd) {
                setPathEnd(node);
            } else {
                // Reset if both set
                setPathStart(node);
                setPathEnd(null);
            }
            return;
        }

        setSelectedNode(node);
        if (onNodeClick) onNodeClick(node);

        // Center view on node
        fgRef.current.centerAt(node.x, node.y, 1000);
        fgRef.current.zoom(2, 1000);
        setContextMenu(null);
    }, [onNodeClick, pathMode, pathStart, pathEnd]);

    const handleRightClick = useCallback((node, event) => {
        // Prevent default browser context menu is handled by graph lib? 
        // ForceGraph2D doesn't natively block context menu easily on nodes without customization
        // But we can use onNodeRightClick
        setContextMenu({
            x: event.clientX,
            y: event.clientY,
            node: node
        });
    }, []);

    const linkCanvasObject = useCallback((link, ctx, globalScale) => {
        // Thin laser lines
        ctx.beginPath();
        ctx.moveTo(link.source.x, link.source.y);
        ctx.lineTo(link.target.x, link.target.y);

        // Highlight links connected to selected node or Path
        const isConnected = selectedNode && (link.source.id === selectedNode.id || link.target.id === selectedNode.id);
        const isPathLink = shortestPath.links.has(link);

        if (isPathLink) {
            ctx.strokeStyle = '#a855f7'; // Purple path
            ctx.lineWidth = 3 / globalScale;
            ctx.shadowColor = '#a855f7';
            ctx.shadowBlur = 5;
        } else {
            ctx.strokeStyle = isConnected ? 'rgba(255, 215, 0, 0.6)' : 'rgba(71, 85, 105, 0.4)'; // Gold if connected, else Slate
            ctx.lineWidth = (isConnected ? 2 : 0.5) / globalScale;
            ctx.shadowBlur = 0;
        }

        ctx.stroke();
        ctx.shadowBlur = 0; // Reset
    }, [selectedNode, shortestPath]);

    const handleExport = useCallback(() => {
        const element = document.getElementById('nexus-graph-container');
        if (element) {
            html2canvas(element, {
                backgroundColor: '#020617',
                scale: 2 // High res
            }).then(canvas => {
                const link = document.createElement('a');
                link.download = `nexus-intelligence-export-${Date.now()}.png`;
                link.href = canvas.toDataURL('image/png');
                link.click();
            });
        }
    }, []);

    return (
        <div id="nexus-graph-container" className={`relative flex flex-col bg-[#020617] border border-slate-800 rounded-xl overflow-hidden shadow-2xl ${isFullscreen ? 'fixed inset-0 z-50' : 'h-full w-full'}`}>

            {/* --- GLASS HEADER --- */}
            <div className="absolute top-0 left-0 right-0 z-10 flex flex-col md:flex-row items-center justify-between p-4 bg-slate-900/40 backdrop-blur-md border-b border-white/5 gap-4 md:gap-0 transition-all">
                <div className="flex items-center justify-between w-full md:w-auto">
                    <div className="flex items-center gap-3">
                        <div className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></div>
                        <span className="text-xs font-mono text-emerald-500 tracking-widest uppercase">NEXUS PRIME /// ONLINE</span>
                    </div>
                </div>

                <div className="flex items-center gap-2 bg-slate-800/50 rounded-lg p-1 border border-white/5 w-full md:w-auto">
                    <Search size={14} className="text-slate-400 ml-2 shrink-0" />
                    <input
                        className="bg-transparent border-none text-xs text-white placeholder-slate-500 focus:ring-0 w-full md:w-64 font-mono"
                        placeholder="SEARCH ENTITY OR ID..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                    />
                </div>

                <div className="absolute top-4 right-4 md:static flex gap-2">
                    <button
                        onClick={() => {
                            if (!selectedNode && !focusMode) return; // Don't enable if nothing selected
                            setFocusMode(!focusMode);
                        }}
                        className={`p-2 rounded-lg transition-colors ${focusMode ? 'bg-amber-600 text-white' : 'hover:bg-white/10 text-slate-400 hover:text-white'} ${!selectedNode && !focusMode ? 'opacity-50 cursor-not-allowed' : ''}`}
                        title="Focus Mode (Isolate Selection)"
                    >
                        <Crosshair size={16} />
                    </button>
                    <button
                        onClick={() => {
                            setPathMode(!pathMode);
                            setPathStart(null);
                            setPathEnd(null);
                            setShortestPath({ nodes: new Set(), links: new Set() });
                        }}
                        className={`p-2 rounded-lg transition-colors ${pathMode ? 'bg-purple-600 text-white' : 'hover:bg-white/10 text-slate-400 hover:text-white'}`}
                        title="Pathfinding Mode (Select 2 Nodes)"
                    >
                        <Route size={16} />
                    </button>
                    <button
                        onClick={handleExport}
                        className="p-2 hover:bg-white/10 rounded-lg text-slate-400 hover:text-white transition-colors"
                        title="Export Intelligence Snapshot"
                    >
                        <Download size={16} />
                    </button>
                    <button className="p-2 hover:bg-white/10 rounded-lg text-slate-400 hover:text-white transition-colors hidden md:block">
                        <Maximize size={16} onClick={() => setIsFullscreen(!isFullscreen)} />
                    </button>
                </div>
            </div>

            {/* --- GRAPH CANVAS --- */}
            <div className="flex-1 relative cursor-crosshair" onContextMenu={(e) => e.preventDefault()}>
                <ForceGraph2D
                    ref={fgRef}
                    graphData={filteredData}
                    width={typeof window !== 'undefined' ? (isFullscreen ? window.innerWidth : width) : width}
                    height={typeof window !== 'undefined' ? (isFullscreen ? window.innerHeight : height) : height}

                    nodeCanvasObject={nodeCanvasObject}
                    linkCanvasObject={linkCanvasObject}

                    onNodeClick={handleNodeClickInternal}
                    onNodeRightClick={handleRightClick}
                    onBackgroundClick={() => {
                        setSelectedNode(null);
                        setContextMenu(null);
                    }}

                    backgroundColor="#020617"
                    linkColor={() => 'rgba(71, 85, 105, 0.2)'}
                    linkWidth={1}

                    d3VelocityDecay={0.6} // Heavier feel
                    d3AlphaDecay={0.01}
                />
            </div>

            {/* --- GLASS INSPECTOR PANEL (Right) --- */}
            <InspectorPanel
                selectedNode={selectedNode}
                onClose={() => setSelectedNode(null)}
            />

            {/* --- SYSTEM STATUS PANEL (ONLY IF NO NODE SELECTED) --- */}
            {!selectedNode && (
                <div className="hidden md:block absolute top-20 right-4 w-64 bg-slate-900/60 backdrop-blur-xl border border-white/5 rounded-lg p-4 shadow-xl pointer-events-none">
                    <div className="text-xs font-mono text-slate-500 mb-2 border-b border-white/5 pb-1">SYSTEM STATUS</div>
                    <div className="flex justify-between items-center mb-2">
                        <span className="text-xs text-slate-300">NODES</span>
                        <span className="text-xs font-bold text-amber-500">{data?.nodes?.length || 0}</span>
                    </div>
                    <div className="flex justify-between items-center">
                        <span className="text-xs text-slate-300">LINKS</span>
                        <span className="text-xs font-bold text-blue-500">{data?.edges?.length || 0}</span>
                    </div>
                </div>
            )}

            {/* --- GRAPH CONTROLS (Left Bottom) --- */}
            <GraphControls filters={filters} onFilterChange={setFilters} />

            {/* --- CONTEXT MENU --- */}
            {contextMenu && (
                <GraphContextMenu
                    x={contextMenu.x}
                    y={contextMenu.y}
                    node={contextMenu.node}
                    onClose={() => setContextMenu(null)}
                />
            )}

        </div>
    );
};

export default memo(NexusGraph);
