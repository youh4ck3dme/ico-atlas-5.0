import React, { useRef, useState } from 'react';
import { Upload, FileSpreadsheet, FileJson, FileText, Loader2 } from 'lucide-react';
import DataParser from '../../utils/DataParser';
import audioManager from '../../utils/AudioManager';
import { useToast } from '../../contexts/ToastContext';
import { useTheater } from '../../contexts/TheaterContext';

const ImportPanel = () => {
    const { setGraphData, setCentralNode } = useTheater();
    const { addToast } = useToast();
    const [isImporting, setIsImporting] = useState(false);
    const fileInputRef = useRef(null);

    const handleFileSelect = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        setIsImporting(true);
        audioManager.playServerHum(); // Loading sound

        try {
            const result = await DataParser.parse(file);

            if (result.nodes && result.nodes.length > 0) {
                // Update Graph
                setGraphData(result);
                setCentralNode(result.nodes[0]); // Focus first node

                audioManager.playAccessGranted(); // Success sound
                audioManager.playVaultOpen(); // Dramatic effect
                addToast(`Import úspešný: ${result.nodes.length} uzlov`, 'success');
            } else {
                audioManager.playError();
                addToast('Súbor neobsahuje žiadne platné dáta', 'error');
            }
        } catch (error) {
            console.error('Import error:', error);
            audioManager.playError();
            addToast(`Chyba importu: ${error.message}`, 'error');
        } finally {
            setIsImporting(false);
            if (fileInputRef.current) {
                fileInputRef.current.value = ''; // Reset input
            }
        }
    };

    const triggerImport = () => {
        audioManager.playClick();
        fileInputRef.current.click();
    };

    return (
        <div className="import-panel">
            <h3 className="filter-title">IMPORT DÁT</h3>

            <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileSelect}
                style={{ display: 'none' }}
                accept=".csv,.xlsx,.xls,.json,.pdf"
            />

            <button
                className="import-button"
                onClick={triggerImport}
                disabled={isImporting}
            >
                {isImporting ? (
                    <Loader2 size={16} className="animate-spin" />
                ) : (
                    <Upload size={16} />
                )}
                <span>NAHRAŤ SÚBOR</span>
            </button>

            <div className="import-formats">
                <span title="Excel"><FileSpreadsheet size={14} /></span>
                <span title="CSV"><FileText size={14} /></span>
                <span title="JSON"><FileJson size={14} /></span>
            </div>

            <div className="import-hint">
                Podporované: .xlsx, .csv, .json, .pdf
            </div>
        </div>
    );
};

export default ImportPanel;
