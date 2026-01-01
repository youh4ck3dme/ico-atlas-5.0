/**
 * AudioManager - Web Audio API based sound effects manager for Theater Mode
 * Only initializes after user gesture to avoid browser warnings
 */

class AudioManager {
    constructor() {
        this.audioContext = null;
        this.masterGain = null;
        this.isMuted = false;
        this.volume = 0.5;
        this.sounds = {};
        this.initialized = false;
        this.pendingInit = false;
    }

    /**
     * Initialize audio context - only call after user gesture!
     */
    async init() {
        if (this.initialized || this.pendingInit) return true;

        this.pendingInit = true;

        try {
            // Create context only after user gesture
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();

            // Resume if suspended
            if (this.audioContext.state === 'suspended') {
                await this.audioContext.resume();
            }

            this.masterGain = this.audioContext.createGain();
            this.masterGain.connect(this.audioContext.destination);
            this.masterGain.gain.value = this.isMuted ? 0 : this.volume;
            this.initialized = true;
            this.pendingInit = false;

            // Pre-generate sounds
            this.generateSounds();
            return true;
        } catch (error) {
            console.warn('AudioManager: Could not initialize audio', error);
            this.pendingInit = false;
            return false;
        }
    }

    generateSounds() {
        // Generate various synthesized sounds
        this.sounds = {
            beep: this.createBeepSound,
            vaultOpen: this.createVaultOpenSound,
            serverHum: this.createServerHumSound,
            stamp: this.createStampSound,
            accessGranted: this.createAccessGrantedSound,
            click: this.createClickSound,
            swoosh: this.createSwooshSound,
            pulse: this.createPulseSound,
            error: this.createErrorSound
        };
    }

    // Resume audio context (required for user gesture)
    async resume() {
        if (this.audioContext && this.audioContext.state === 'suspended') {
            await this.audioContext.resume();
        }
    }

    // Set volume (0-1)
    setVolume(value) {
        this.volume = Math.max(0, Math.min(1, value));
        if (this.masterGain) {
            this.masterGain.gain.setValueAtTime(this.isMuted ? 0 : this.volume, this.audioContext.currentTime);
        }
    }

    // Toggle mute
    toggleMute() {
        this.isMuted = !this.isMuted;
        if (this.masterGain) {
            this.masterGain.gain.setValueAtTime(this.isMuted ? 0 : this.volume, this.audioContext.currentTime);
        }
        return this.isMuted;
    }

    setMuted(muted) {
        this.isMuted = muted;
        if (this.masterGain) {
            this.masterGain.gain.setValueAtTime(this.isMuted ? 0 : this.volume, this.audioContext.currentTime);
        }
    }

    // Create oscillator-based beep
    createBeepSound = () => {
        if (!this.audioContext || this.isMuted) return;

        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();

        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(880, this.audioContext.currentTime);
        oscillator.frequency.exponentialRampToValueAtTime(1760, this.audioContext.currentTime + 0.1);

        gainNode.gain.setValueAtTime(0.3, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.1);

        oscillator.connect(gainNode);
        gainNode.connect(this.masterGain);

        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + 0.1);
    }

    // Vault opening sound (heavy mechanical)
    createVaultOpenSound = () => {
        if (!this.audioContext || this.isMuted) return;

        const duration = 2;
        const now = this.audioContext.currentTime;

        // Low rumble
        const rumbleOsc = this.audioContext.createOscillator();
        const rumbleGain = this.audioContext.createGain();
        rumbleOsc.type = 'sawtooth';
        rumbleOsc.frequency.setValueAtTime(50, now);
        rumbleOsc.frequency.linearRampToValueAtTime(30, now + duration);
        rumbleGain.gain.setValueAtTime(0.4, now);
        rumbleGain.gain.exponentialRampToValueAtTime(0.01, now + duration);
        rumbleOsc.connect(rumbleGain);
        rumbleGain.connect(this.masterGain);
        rumbleOsc.start(now);
        rumbleOsc.stop(now + duration);

        // Metal clang
        const clangOsc = this.audioContext.createOscillator();
        const clangGain = this.audioContext.createGain();
        clangOsc.type = 'square';
        clangOsc.frequency.setValueAtTime(200, now + 1.5);
        clangOsc.frequency.exponentialRampToValueAtTime(100, now + 2);
        clangGain.gain.setValueAtTime(0, now);
        clangGain.gain.setValueAtTime(0.5, now + 1.5);
        clangGain.gain.exponentialRampToValueAtTime(0.01, now + 2);
        clangOsc.connect(clangGain);
        clangGain.connect(this.masterGain);
        clangOsc.start(now);
        clangOsc.stop(now + 2);
    }

    // Server hum ambient
    createServerHumSound = () => {
        if (!this.audioContext || this.isMuted) return;

        const duration = 5;
        const now = this.audioContext.currentTime;

        // Base hum
        const humOsc = this.audioContext.createOscillator();
        const humGain = this.audioContext.createGain();
        humOsc.type = 'sine';
        humOsc.frequency.setValueAtTime(60, now);
        humGain.gain.setValueAtTime(0.1, now);
        humGain.gain.setValueAtTime(0.15, now + duration / 2);
        humGain.gain.exponentialRampToValueAtTime(0.01, now + duration);
        humOsc.connect(humGain);
        humGain.connect(this.masterGain);
        humOsc.start(now);
        humOsc.stop(now + duration);

        // Light processing sounds
        for (let i = 0; i < 3; i++) {
            const blipOsc = this.audioContext.createOscillator();
            const blipGain = this.audioContext.createGain();
            const blipTime = now + 1 + i * 1.2;
            blipOsc.type = 'sine';
            blipOsc.frequency.setValueAtTime(2000 + Math.random() * 1000, blipTime);
            blipGain.gain.setValueAtTime(0, now);
            blipGain.gain.setValueAtTime(0.1, blipTime);
            blipGain.gain.exponentialRampToValueAtTime(0.01, blipTime + 0.05);
            blipOsc.connect(blipGain);
            blipGain.connect(this.masterGain);
            blipOsc.start(now);
            blipOsc.stop(blipTime + 0.1);
        }
    }

    // Stamp sound
    createStampSound = () => {
        if (!this.audioContext || this.isMuted) return;

        const now = this.audioContext.currentTime;

        // Impact thud
        const thudOsc = this.audioContext.createOscillator();
        const thudGain = this.audioContext.createGain();
        thudOsc.type = 'sine';
        thudOsc.frequency.setValueAtTime(150, now);
        thudOsc.frequency.exponentialRampToValueAtTime(50, now + 0.2);
        thudGain.gain.setValueAtTime(0.6, now);
        thudGain.gain.exponentialRampToValueAtTime(0.01, now + 0.3);
        thudOsc.connect(thudGain);
        thudGain.connect(this.masterGain);
        thudOsc.start(now);
        thudOsc.stop(now + 0.3);

        // Paper rustle (noise)
        const bufferSize = this.audioContext.sampleRate * 0.1;
        const noiseBuffer = this.audioContext.createBuffer(1, bufferSize, this.audioContext.sampleRate);
        const output = noiseBuffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
            output[i] = Math.random() * 2 - 1;
        }
        const noiseSource = this.audioContext.createBufferSource();
        const noiseGain = this.audioContext.createGain();
        const noiseFilter = this.audioContext.createBiquadFilter();
        noiseSource.buffer = noiseBuffer;
        noiseFilter.type = 'highpass';
        noiseFilter.frequency.value = 3000;
        noiseGain.gain.setValueAtTime(0.15, now);
        noiseGain.gain.exponentialRampToValueAtTime(0.01, now + 0.1);
        noiseSource.connect(noiseFilter);
        noiseFilter.connect(noiseGain);
        noiseGain.connect(this.masterGain);
        noiseSource.start(now);
        noiseSource.stop(now + 0.1);
    }

    // Access granted fanfare
    createAccessGrantedSound = () => {
        if (!this.audioContext || this.isMuted) return;

        const now = this.audioContext.currentTime;
        const notes = [523.25, 659.25, 783.99, 1046.50]; // C5, E5, G5, C6

        notes.forEach((freq, i) => {
            const osc = this.audioContext.createOscillator();
            const gain = this.audioContext.createGain();
            const startTime = now + i * 0.15;

            osc.type = 'sine';
            osc.frequency.setValueAtTime(freq, startTime);
            gain.gain.setValueAtTime(0, now);
            gain.gain.setValueAtTime(0.3, startTime);
            gain.gain.exponentialRampToValueAtTime(0.01, startTime + 0.4);

            osc.connect(gain);
            gain.connect(this.masterGain);
            osc.start(now);
            osc.stop(startTime + 0.5);
        });
    }

    // Simple click
    createClickSound = () => {
        if (!this.audioContext || this.isMuted) return;

        const now = this.audioContext.currentTime;
        const osc = this.audioContext.createOscillator();
        const gain = this.audioContext.createGain();

        osc.type = 'sine';
        osc.frequency.setValueAtTime(1000, now);
        gain.gain.setValueAtTime(0.2, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.03);

        osc.connect(gain);
        gain.connect(this.masterGain);
        osc.start(now);
        osc.stop(now + 0.03);
    }

    // Swoosh for transitions
    createSwooshSound = () => {
        if (!this.audioContext || this.isMuted) return;

        const now = this.audioContext.currentTime;

        // White noise with filter sweep
        const bufferSize = this.audioContext.sampleRate * 0.5;
        const noiseBuffer = this.audioContext.createBuffer(1, bufferSize, this.audioContext.sampleRate);
        const output = noiseBuffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
            output[i] = Math.random() * 2 - 1;
        }

        const noiseSource = this.audioContext.createBufferSource();
        const noiseGain = this.audioContext.createGain();
        const noiseFilter = this.audioContext.createBiquadFilter();

        noiseSource.buffer = noiseBuffer;
        noiseFilter.type = 'bandpass';
        noiseFilter.frequency.setValueAtTime(500, now);
        noiseFilter.frequency.exponentialRampToValueAtTime(4000, now + 0.3);
        noiseFilter.Q.value = 1;

        noiseGain.gain.setValueAtTime(0.01, now);
        noiseGain.gain.linearRampToValueAtTime(0.25, now + 0.1);
        noiseGain.gain.exponentialRampToValueAtTime(0.01, now + 0.4);

        noiseSource.connect(noiseFilter);
        noiseFilter.connect(noiseGain);
        noiseGain.connect(this.masterGain);
        noiseSource.start(now);
        noiseSource.stop(now + 0.5);
    }

    // Pulse for node highlighting
    createPulseSound = () => {
        if (!this.audioContext || this.isMuted) return;

        const now = this.audioContext.currentTime;
        const osc = this.audioContext.createOscillator();
        const gain = this.audioContext.createGain();

        osc.type = 'sine';
        osc.frequency.setValueAtTime(440, now);
        osc.frequency.linearRampToValueAtTime(660, now + 0.2);

        gain.gain.setValueAtTime(0.01, now);
        gain.gain.linearRampToValueAtTime(0.15, now + 0.1);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.3);

        osc.connect(gain);
        gain.connect(this.masterGain);
        osc.start(now);
        osc.stop(now + 0.3);
    }

    // Error sound (low buzz)
    createErrorSound = () => {
        if (!this.audioContext || this.isMuted) return;

        const now = this.audioContext.currentTime;
        const osc = this.audioContext.createOscillator();
        const gain = this.audioContext.createGain();

        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(120, now);
        osc.frequency.linearRampToValueAtTime(80, now + 0.3);

        gain.gain.setValueAtTime(0.3, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.3);

        osc.connect(gain);
        gain.connect(this.masterGain);
        osc.start(now);
        osc.stop(now + 0.3);
    }

    // Play a specific sound
    play(soundName) {
        if (!this.initialized) {
            this.init().then(() => {
                this.resume().then(() => {
                    if (this.sounds[soundName]) {
                        this.sounds[soundName]();
                    }
                });
            });
        } else {
            this.resume().then(() => {
                if (this.sounds[soundName]) {
                    this.sounds[soundName]();
                }
            });
        }
    }

    // Convenience methods
    playBeep() { this.play('beep'); }
    playVaultOpen() { this.play('vaultOpen'); }
    playServerHum() { this.play('serverHum'); }
    playStamp() { this.play('stamp'); }
    playAccessGranted() { this.play('accessGranted'); }
    playClick() { this.play('click'); }
    playSwoosh() { this.play('swoosh'); }
    playPulse() { this.play('pulse'); }
    playError() { this.play('error'); }
}

// Singleton instance
const audioManager = new AudioManager();

export default audioManager;
