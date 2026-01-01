import React, { useState, useEffect } from 'react';
import { X, ExternalLink, AlertTriangle } from 'lucide-react';
import { useTheater } from '../../contexts/TheaterContext';
import audioManager from '../../utils/AudioManager';
import { CompanyIcon, PersonIcon, LocationIcon, RiskIcon } from './PremiumIcons';
import '../../styles/theater.css';

// Country flags mapping
const countryFlags = {
    SK: '🇸🇰',
    CZ: '🇨🇿',
    PL: '🇵🇱',
    HU: '🇭🇺'
};

const NodeCard = () => {
    const { selectedNode, isNodeCardOpen, closeNodeCard } = useTheater();
    const [isOpening, setIsOpening] = useState(false);
    const [showContent, setShowContent] = useState(false);

    useEffect(() => {
        if (isNodeCardOpen && selectedNode) {
            // Start door opening animation
            setIsOpening(true);
            audioManager.playSwoosh();

            // Show content after doors open
            const timer = setTimeout(() => {
                setShowContent(true);
                audioManager.playPulse();
            }, 400);

            return () => clearTimeout(timer);
        } else {
            setIsOpening(false);
            setShowContent(false);
        }
    }, [isNodeCardOpen, selectedNode]);

    // ESC key handler
    useEffect(() => {
        const handleEsc = (e) => {
            if (e.key === 'Escape' && isNodeCardOpen) {
                handleClose();
            }
        };
        window.addEventListener('keydown', handleEsc);
        return () => window.removeEventListener('keydown', handleEsc);
    }, [isNodeCardOpen]);

    const handleClose = () => {
        audioManager.playClick();
        closeNodeCard();
    };

    const renderNodeIcon = () => {
        if (!selectedNode) return <CompanyIcon size={32} />;
        const isRisk = (selectedNode.risk_score || 0) > 5;

        switch (selectedNode.type) {
            case 'company':
                return <CompanyIcon size={32} risk={isRisk} />;
            case 'person':
                return <PersonIcon size={32} />;
            case 'address':
                return <LocationIcon size={32} virtual={selectedNode.virtual_seat} />;
            case 'debt':
                return <RiskIcon size={32} level={selectedNode.risk_score || 8} />;
            default:
                return <CompanyIcon size={32} />;
        }
    };

    const getNodeColor = () => {
        if (!selectedNode) return '#D4AF37';
        switch (selectedNode.type) {
            case 'company':
                return (selectedNode.risk_score || 0) > 5 ? '#ef4444' : '#D4AF37';
            case 'person': return '#60a5fa';
            case 'address': return '#34d399';
            case 'debt': return '#f87171';
            default: return '#D4AF37';
        }
    };

    if (!isNodeCardOpen || !selectedNode) return null;

    const color = getNodeColor();

    return (
        <div className="node-card-backdrop" onClick={handleClose}>
            <div
                className={`node-card-container ${isOpening ? 'node-card-opening' : ''}`}
                onClick={(e) => e.stopPropagation()}
            >
                {/* Door Left */}
                <div className="node-card-door-left">
                    <div className="door-handle" style={{ marginLeft: 'auto', marginRight: '20px' }} />
                </div>

                {/* Door Right */}
                <div className="node-card-door-right">
                    <div className="door-handle" style={{ marginRight: 'auto', marginLeft: '20px' }} />
                </div>

                {/* Card Content */}
                <div className="node-card-content">
                    {/* Close Button */}
                    <button className="node-card-close" onClick={handleClose}>
                        <X size={18} />
                    </button>

                    {showContent && (
                        <>
                            {/* Header */}
                            <div className="node-card-header">
                                <div
                                    className="node-card-logo"
                                    style={{
                                        borderColor: color,
                                        background: `linear-gradient(135deg, ${color}20, ${color}10)`
                                    }}
                                >
                                    {renderNodeIcon()}
                                </div>
                                <div className="flex-1">
                                    <h3 className="node-card-title" style={{ color }}>
                                        {selectedNode.label || selectedNode.id}
                                    </h3>
                                    <div className="flex gap-2 items-center flex-wrap mt-2">
                                        <span className="node-card-badge">
                                            {selectedNode.type}
                                        </span>
                                        {selectedNode.country && (
                                            <span className="node-card-badge" style={{
                                                background: 'rgba(96, 165, 250, 0.2)',
                                                borderColor: '#60a5fa',
                                                color: '#60a5fa'
                                            }}>
                                                {countryFlags[selectedNode.country]} {selectedNode.country}
                                            </span>
                                        )}
                                    </div>
                                </div>
                            </div>

                            {/* Details */}
                            <div className="node-card-details">
                                {selectedNode.ico && (
                                    <div className="node-card-row">
                                        <span className="node-card-label">IČO</span>
                                        <span className="node-card-value">{selectedNode.ico}</span>
                                    </div>
                                )}

                                {selectedNode.founded && (
                                    <div className="node-card-row">
                                        <span className="node-card-label">Založené</span>
                                        <span className="node-card-value">{selectedNode.founded}</span>
                                    </div>
                                )}

                                {selectedNode.details && (
                                    <div className="node-card-row" style={{ flexDirection: 'column', alignItems: 'flex-start', gap: '0.5rem' }}>
                                        <span className="node-card-label">Detaily</span>
                                        <span className="node-card-value" style={{ fontSize: '0.875rem', fontWeight: 'normal' }}>
                                            {selectedNode.details}
                                        </span>
                                    </div>
                                )}

                                {selectedNode.risk_score !== undefined && selectedNode.risk_score > 0 && (
                                    <div className="node-card-row" style={{ flexDirection: 'column', alignItems: 'stretch', gap: '0.5rem' }}>
                                        <div className="flex justify-between">
                                            <span className="node-card-label">Rizikové skóre</span>
                                            <span className="node-card-value" style={{
                                                color: selectedNode.risk_score > 5 ? '#ef4444' : '#fbbf24'
                                            }}>
                                                {selectedNode.risk_score}/10
                                            </span>
                                        </div>
                                        <div className="w-full bg-gray-700 rounded-full h-2">
                                            <div
                                                className="h-2 rounded-full transition-all duration-500"
                                                style={{
                                                    width: `${(selectedNode.risk_score / 10) * 100}%`,
                                                    background: selectedNode.risk_score > 5
                                                        ? 'linear-gradient(90deg, #fbbf24, #ef4444)'
                                                        : 'linear-gradient(90deg, #34d399, #fbbf24)'
                                                }}
                                            />
                                        </div>
                                    </div>
                                )}

                                {selectedNode.virtual_seat && (
                                    <div className="flex items-center gap-2 p-3 bg-amber-900/30 border border-amber-500/30 rounded-lg">
                                        <AlertTriangle size={18} className="text-amber-400" />
                                        <span className="text-sm text-amber-300 font-mono">Virtuálne sídlo</span>
                                    </div>
                                )}
                            </div>

                            {/* Actions */}
                            <div className="mt-6 pt-4 border-t border-[#D4AF37]/20 flex gap-3">
                                {selectedNode.ico && (
                                    <button
                                        className="flex-1 flex items-center justify-center gap-2 p-3 bg-[#D4AF37]/10 border border-[#D4AF37]/30 rounded-lg text-[#D4AF37] hover:bg-[#D4AF37]/20 transition-all font-mono text-sm"
                                        onClick={() => {
                                            audioManager.playClick();
                                            // Could open external link to register
                                            window.open(`https://finstat.sk/${selectedNode.ico}`, '_blank');
                                        }}
                                    >
                                        <ExternalLink size={16} />
                                        Otvoriť v registri
                                    </button>
                                )}
                            </div>
                        </>
                    )}
                </div>
            </div>
        </div>
    );
};

export default NodeCard;
