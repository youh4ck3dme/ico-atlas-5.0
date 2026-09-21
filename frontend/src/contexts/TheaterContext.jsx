import React, { createContext, useContext, useState, useCallback, useMemo } from 'react';

const TheaterContext = createContext(null);

export const useTheater = () => {
    const context = useContext(TheaterContext);
    if (!context) {
        throw new Error('useTheater must be used within TheaterProvider');
    }
    return context;
};

export const TheaterProvider = ({ children }) => {
    // Intro state
    const [introComplete, setIntroComplete] = useState(false);
    const [isIntroPlaying, setIsIntroPlaying] = useState(true);

    // Audio state
    const [isMuted, setIsMuted] = useState(false);
    const [audioVolume, setAudioVolume] = useState(0.5);

    // Search state
    const [searchQuery, setSearchQuery] = useState('');
    const [isSearching, setIsSearching] = useState(false);
    const [centralNode, setCentralNode] = useState(null);

    // Graph state
    const [graphData, setGraphData] = useState({ nodes: [], edges: [] });
    const [selectedNode, setSelectedNode] = useState(null);
    const [isNodeCardOpen, setIsNodeCardOpen] = useState(false);

    // Filter state
    const [filters, setFilters] = useState({
        showOwnership: true,
        showManagement: true,
        showLocation: true,
        showDebts: true,
        riskScoreMin: 0,
        riskScoreMax: 10,
        countries: ['SK', 'CZ', 'PL', 'HU']
    });

    // Actions
    const completeIntro = useCallback(() => {
        setIsIntroPlaying(false);
        setIntroComplete(true);
    }, []);

    const skipIntro = useCallback(() => {
        setIsIntroPlaying(false);
        setIntroComplete(true);
    }, []);

    const toggleMute = useCallback(() => {
        setIsMuted(prev => !prev);
    }, []);

    const openNodeCard = useCallback((node) => {
        setSelectedNode(node);
        setIsNodeCardOpen(true);
    }, []);

    const closeNodeCard = useCallback(() => {
        setIsNodeCardOpen(false);
        setSelectedNode(null);
    }, []);

    const updateFilter = useCallback((key, value) => {
        setFilters(prev => ({ ...prev, [key]: value }));
    }, []);

    const resetFilters = useCallback(() => {
        setFilters({
            showOwnership: true,
            showManagement: true,
            showLocation: true,
            showDebts: true,
            riskScoreMin: 0,
            riskScoreMax: 10,
            countries: ['SK', 'CZ', 'PL', 'HU']
        });
    }, []);

    // Filtered graph data
    const filteredGraphData = useMemo(() => {
        if (!graphData.nodes.length) return graphData;

        const filteredEdges = graphData.edges.filter(edge => {
            if (edge.type === 'OWNED_BY' && !filters.showOwnership) return false;
            if (edge.type === 'MANAGED_BY' && !filters.showManagement) return false;
            if (edge.type === 'LOCATED_AT' && !filters.showLocation) return false;
            if (edge.type === 'HAS_DEBT' && !filters.showDebts) return false;
            return true;
        });

        const connectedNodeIds = new Set();
        filteredEdges.forEach(edge => {
            connectedNodeIds.add(edge.source);
            connectedNodeIds.add(edge.target);
        });

        const filteredNodes = graphData.nodes.filter(node => {
            // Always show central node
            if (node.id === centralNode?.id) return true;

            // Check connection
            if (!connectedNodeIds.has(node.id)) return false;

            // Check risk score
            const riskScore = node.risk_score || 0;
            if (riskScore < filters.riskScoreMin || riskScore > filters.riskScoreMax) return false;

            // Check country
            if (node.country && !filters.countries.includes(node.country)) return false;

            return true;
        });

        return { nodes: filteredNodes, edges: filteredEdges };
    }, [graphData, filters, centralNode]);

    const value = {
        // State
        introComplete,
        isIntroPlaying,
        isMuted,
        audioVolume,
        searchQuery,
        isSearching,
        centralNode,
        graphData,
        selectedNode,
        isNodeCardOpen,
        filters,
        filteredGraphData,

        // Actions
        completeIntro,
        skipIntro,
        toggleMute,
        setAudioVolume,
        setSearchQuery,
        setIsSearching,
        setCentralNode,
        setGraphData,
        openNodeCard,
        closeNodeCard,
        updateFilter,
        resetFilters
    };

    return (
        <TheaterContext.Provider value={value}>
            {children}
        </TheaterContext.Provider>
    );
};

export default TheaterContext;
