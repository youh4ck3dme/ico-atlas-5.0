import React, { useState, useCallback } from 'react';
import { Download, Archive, FileText, Check, Stamp } from 'lucide-react';
import { useTheater } from '../../contexts/TheaterContext';
import audioManager from '../../utils/AudioManager';
import '../../styles/theater.css';

const ExportPanel = ({ graphRef }) => {
    const { filteredGraphData, centralNode } = useTheater();
    const [stampActive, setStampActive] = useState(null);
    const [downloadingItem, setDownloadingItem] = useState(null);

    const showStampEffect = (type) => {
        setStampActive(type);
        audioManager.playStamp();
        setTimeout(() => setStampActive(null), 600);
    };

    const handleExportPNG = useCallback(async () => {
        if (!graphRef?.current) return;

        setDownloadingItem('png');
        showStampEffect('png');

        try {
            // Try to get canvas from force-graph
            const canvas = graphRef.current.getGraphCanvas
                ? graphRef.current.getGraphCanvas()
                : document.querySelector('.theater-graph-container canvas');

            if (canvas) {
                const url = canvas.toDataURL('image/png');
                const link = document.createElement('a');
                link.download = `firemne-vztahy-${centralNode?.label || 'export'}-${Date.now()}.png`;
                link.href = url;
                link.click();
            } else {
                console.warn('Canvas not found');
            }
        } catch (error) {
            console.error('PNG export error:', error);
        } finally {
            setTimeout(() => setDownloadingItem(null), 500);
        }
    }, [graphRef, centralNode]);

    const handleExportJSON = useCallback(() => {
        setDownloadingItem('json');
        showStampEffect('json');

        try {
            const dataStr = JSON.stringify(filteredGraphData, null, 2);
            const dataBlob = new Blob([dataStr], { type: 'application/json' });
            const url = URL.createObjectURL(dataBlob);

            const link = document.createElement('a');
            link.download = `firemne-vztahy-${centralNode?.label || 'export'}-${Date.now()}.json`;
            link.href = url;
            link.click();

            URL.revokeObjectURL(url);
        } catch (error) {
            console.error('JSON export error:', error);
        } finally {
            setTimeout(() => setDownloadingItem(null), 500);
        }
    }, [filteredGraphData, centralNode]);

    const handleExportReport = useCallback(() => {
        setDownloadingItem('report');
        showStampEffect('report');

        try {
            // Generate HTML report
            const nodes = filteredGraphData.nodes || [];
            const edges = filteredGraphData.edges || [];

            const companies = nodes.filter(n => n.type === 'company');
            const persons = nodes.filter(n => n.type === 'person');
            const addresses = nodes.filter(n => n.type === 'address');
            const highRisk = nodes.filter(n => (n.risk_score || 0) > 5);

            const reportHtml = `
<!DOCTYPE html>
<html lang="sk">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Analýza firemných vzťahov - ${centralNode?.label || 'Report'}</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { 
      font-family: 'Courier New', monospace; 
      background: #0A0A0A; 
      color: #ffffff; 
      padding: 40px;
      line-height: 1.6;
    }
    .header { 
      text-align: center; 
      padding: 40px; 
      border: 2px solid #D4AF37;
      margin-bottom: 40px;
      background: linear-gradient(135deg, #1a1a2e, #0A0A0A);
    }
    .header h1 { 
      color: #D4AF37; 
      font-size: 2rem;
      text-shadow: 0 0 20px rgba(212, 175, 55, 0.5);
      margin-bottom: 10px;
    }
    .header .date { color: #888; font-size: 0.9rem; }
    .section { 
      margin-bottom: 30px; 
      padding: 20px;
      border: 1px solid #D4AF37;
      background: rgba(26, 26, 46, 0.5);
    }
    .section h2 { 
      color: #D4AF37; 
      margin-bottom: 15px;
      font-size: 1.2rem;
      border-bottom: 1px solid rgba(212, 175, 55, 0.3);
      padding-bottom: 10px;
    }
    .stat { 
      display: flex; 
      justify-content: space-between;
      padding: 8px 0;
      border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    .stat-value { color: #D4AF37; font-weight: bold; }
    .entity { 
      padding: 10px; 
      margin: 8px 0;
      background: rgba(0,0,0,0.3);
      border-left: 3px solid #D4AF37;
    }
    .entity.risk { border-left-color: #ef4444; }
    .entity-name { color: #D4AF37; font-weight: bold; }
    .entity-type { 
      display: inline-block;
      padding: 2px 8px;
      background: rgba(212, 175, 55, 0.2);
      font-size: 0.75rem;
      margin-left: 10px;
    }
    .footer { 
      text-align: center; 
      padding: 20px;
      color: #666;
      font-size: 0.8rem;
      border-top: 1px solid rgba(212, 175, 55, 0.3);
      margin-top: 40px;
    }
    .confidential {
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%) rotate(-30deg);
      font-size: 8rem;
      color: rgba(212, 175, 55, 0.05);
      pointer-events: none;
      white-space: nowrap;
    }
  </style>
</head>
<body>
  <div class="confidential">DÔVERNÉ</div>
  
  <div class="header">
    <h1>📊 ANALÝZA FIREMNÝCH VZŤAHOV</h1>
    <div class="date">Vygenerované: ${new Date().toLocaleString('sk-SK')}</div>
    ${centralNode ? `<div style="margin-top: 15px; color: #D4AF37;">Centrálny subjekt: ${centralNode.label}</div>` : ''}
  </div>
  
  <div class="section">
    <h2>📈 Súhrn</h2>
    <div class="stat"><span>Celkový počet entít:</span> <span class="stat-value">${nodes.length}</span></div>
    <div class="stat"><span>Firmy:</span> <span class="stat-value">${companies.length}</span></div>
    <div class="stat"><span>Osoby:</span> <span class="stat-value">${persons.length}</span></div>
    <div class="stat"><span>Adresy:</span> <span class="stat-value">${addresses.length}</span></div>
    <div class="stat"><span>Vzťahy:</span> <span class="stat-value">${edges.length}</span></div>
    <div class="stat"><span>Vysokorizikové entity:</span> <span class="stat-value" style="color: #ef4444;">${highRisk.length}</span></div>
  </div>
  
  ${companies.length > 0 ? `
  <div class="section">
    <h2>🏢 Firmy</h2>
    ${companies.map(c => `
      <div class="entity ${(c.risk_score || 0) > 5 ? 'risk' : ''}">
        <span class="entity-name">${c.label}</span>
        <span class="entity-type">${c.country || 'N/A'}</span>
        ${c.ico ? `<div style="color: #888; font-size: 0.85rem;">IČO: ${c.ico}</div>` : ''}
        ${c.risk_score ? `<div style="color: ${c.risk_score > 5 ? '#ef4444' : '#fbbf24'}; font-size: 0.85rem;">Riziko: ${c.risk_score}/10</div>` : ''}
      </div>
    `).join('')}
  </div>
  ` : ''}
  
  ${persons.length > 0 ? `
  <div class="section">
    <h2>👤 Osoby</h2>
    ${persons.map(p => `
      <div class="entity">
        <span class="entity-name">${p.label}</span>
        ${p.details ? `<div style="color: #888; font-size: 0.85rem;">${p.details}</div>` : ''}
      </div>
    `).join('')}
  </div>
  ` : ''}
  
  ${highRisk.length > 0 ? `
  <div class="section" style="border-color: #ef4444;">
    <h2 style="color: #ef4444;">⚠️ Rizikové entity</h2>
    ${highRisk.map(r => `
      <div class="entity risk">
        <span class="entity-name">${r.label}</span>
        <span class="entity-type">${r.type}</span>
        <div style="color: #ef4444; font-size: 0.85rem;">Riziko: ${r.risk_score}/10</div>
        ${r.virtual_seat ? '<div style="color: #fbbf24; font-size: 0.85rem;">⚠ Virtuálne sídlo</div>' : ''}
      </div>
    `).join('')}
  </div>
  ` : ''}
  
  <div class="footer">
    <p>Tento report bol automaticky vygenerovaný systémom ILUMINATE SYSTEM.</p>
    <p>Dáta pochádzajú z verejných registrov SR, CZ, PL a HU.</p>
  </div>
</body>
</html>
      `;

            const dataBlob = new Blob([reportHtml], { type: 'text/html' });
            const url = URL.createObjectURL(dataBlob);

            const link = document.createElement('a');
            link.download = `report-${centralNode?.label || 'export'}-${Date.now()}.html`;
            link.href = url;
            link.click();

            URL.revokeObjectURL(url);
        } catch (error) {
            console.error('Report export error:', error);
        } finally {
            setTimeout(() => setDownloadingItem(null), 500);
        }
    }, [filteredGraphData, centralNode]);

    const hasData = filteredGraphData.nodes && filteredGraphData.nodes.length > 0;

    return (
        <div className="export-panel">
            {/* Export PNG */}
            <button
                className="export-button"
                onClick={handleExportPNG}
                disabled={!hasData || downloadingItem === 'png'}
                title="Exportovať graf ako obrázok"
            >
                {downloadingItem === 'png' ? (
                    <Check size={18} className="text-green-400" />
                ) : (
                    <Download size={18} />
                )}
                <span>Stiahnuť dôkaz</span>

                {/* Stamp Effect */}
                <div className={`stamp-effect ${stampActive === 'png' ? 'active' : ''}`}>
                    <div className="stamp-icon">
                        <Stamp size={32} />
                    </div>
                </div>
            </button>

            {/* Export JSON */}
            <button
                className="export-button"
                onClick={handleExportJSON}
                disabled={!hasData || downloadingItem === 'json'}
                title="Uložiť dáta do archívu"
            >
                {downloadingItem === 'json' ? (
                    <Check size={18} className="text-green-400" />
                ) : (
                    <Archive size={18} />
                )}
                <span>Uložiť do archívu</span>

                <div className={`stamp-effect ${stampActive === 'json' ? 'active' : ''}`}>
                    <div className="stamp-icon">
                        <Stamp size={32} />
                    </div>
                </div>
            </button>

            {/* Export Report */}
            <button
                className="export-button"
                onClick={handleExportReport}
                disabled={!hasData || downloadingItem === 'report'}
                title="Generovať HTML report"
            >
                {downloadingItem === 'report' ? (
                    <Check size={18} className="text-green-400" />
                ) : (
                    <FileText size={18} />
                )}
                <span>Generovať hlásenie</span>

                <div className={`stamp-effect ${stampActive === 'report' ? 'active' : ''}`}>
                    <div className="stamp-icon">
                        <Stamp size={32} />
                    </div>
                </div>
            </button>
        </div>
    );
};

export default ExportPanel;
