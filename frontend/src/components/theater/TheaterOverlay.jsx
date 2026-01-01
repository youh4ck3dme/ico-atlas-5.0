import React, { useState, useEffect, useCallback } from 'react';
import { useTheater } from '../../contexts/TheaterContext';
import audioManager from '../../utils/AudioManager';
import '../../styles/theater.css';

const TheaterOverlay = () => {
    const { completeIntro, skipIntro, isIntroPlaying, isMuted } = useTheater();
    const [phase, setPhase] = useState('vault'); // vault, spinning, access, opening, done
    const [showAccessText, setShowAccessText] = useState(false);

    useEffect(() => {
        if (!isIntroPlaying) return;

        // Initialize audio
        audioManager.init();
        audioManager.setMuted(isMuted);

        // Start animation sequence
        const sequence = async () => {
            // Phase 1: Vault appears (already showing)
            await delay(500);

            // Play vault sound
            audioManager.playVaultOpen();

            // Phase 2: Vault spinning
            setPhase('spinning');
            await delay(2000);

            // Phase 3: Access granted
            setPhase('access');
            setShowAccessText(true);
            audioManager.playAccessGranted();
            await delay(1500);

            // Phase 4: Doors opening
            setPhase('opening');
            audioManager.playSwoosh();
            await delay(1500);

            // Phase 5: Complete
            setPhase('done');
            completeIntro();
        };

        sequence();
    }, [isIntroPlaying, isMuted, completeIntro]);

    const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

    const handleSkip = useCallback(() => {
        audioManager.playClick();
        skipIntro();
    }, [skipIntro]);

    if (!isIntroPlaying) return null;

    return (
        <div className={`theater-overlay ${phase === 'opening' ? 'door-opening' : ''}`}>
            {/* Scanlines effect */}
            <div className="scanlines" />

            {/* Vault Door */}
            {phase !== 'opening' && phase !== 'done' && (
                <div className={`vault-door ${phase === 'spinning' ? 'vault-spinning' : ''}`}>
                    <div className="vault-handle">
                        <div className="vault-handle-bar horizontal" />
                        <div className="vault-handle-bar vertical" />
                        <div className="vault-center" />
                    </div>
                </div>
            )}

            {/* Access Text */}
            <div className={`access-text ${showAccessText ? 'visible' : ''}`}>
                <div className="access-title">Prístup schválený</div>
                <div className="access-subtitle">Pripájanie k databáze...</div>
            </div>

            {/* Door Panels */}
            {phase === 'opening' && (
                <>
                    <div className="door-left">
                        <div style={{
                            position: 'absolute',
                            right: '40px',
                            top: '50%',
                            transform: 'translateY(-50%)',
                            width: '8px',
                            height: '60px',
                            background: 'linear-gradient(180deg, #D4AF37, #B8860B)',
                            borderRadius: '4px',
                            boxShadow: '0 0 10px rgba(212, 175, 55, 0.5)'
                        }} />
                    </div>
                    <div className="door-right">
                        <div style={{
                            position: 'absolute',
                            left: '40px',
                            top: '50%',
                            transform: 'translateY(-50%)',
                            width: '8px',
                            height: '60px',
                            background: 'linear-gradient(180deg, #D4AF37, #B8860B)',
                            borderRadius: '4px',
                            boxShadow: '0 0 10px rgba(212, 175, 55, 0.5)'
                        }} />
                    </div>
                </>
            )}

            {/* Skip Button */}
            <button className="skip-button" onClick={handleSkip}>
                Preskočiť →
            </button>
        </div>
    );
};

export default TheaterOverlay;
