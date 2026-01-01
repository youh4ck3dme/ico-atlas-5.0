/**
 * Export utility funkcie pre PDF a CSV
 */
import { API_URL } from '../config/api';

/**
 * Exportuje graf do CSV
 */
export const exportToCSV = (data) => {
  if (!data || !data.nodes || !data.edges) {
    alert('Žiadne dáta na export');
    return;
  }

  // CSV hlavička
  let csv = 'Typ,ID,Label,Krajina,Risk Score,Detaily\n';
  
  // Nodes
  data.nodes.forEach(node => {
    const row = [
      node.type,
      node.id,
      `"${node.label}"`,
      node.country,
      node.risk_score || 0,
      `"${(node.details || '').replace(/"/g, '""')}"`
    ].join(',');
    csv += row + '\n';
  });
  
  // Edges
  csv += '\nVzťahy:\n';
  csv += 'Source,Target,Type\n';
  data.edges.forEach(edge => {
    csv += `${edge.source},${edge.target},${edge.type}\n`;
  });

  // Download
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);
  link.setAttribute('href', url);
  link.setAttribute('download', `iluminati-export-${new Date().toISOString().split('T')[0]}.csv`);
  link.style.visibility = 'hidden';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

/**
 * Exportuje graf do PDF (pomocou html2pdf alebo window.print)
 */
export const exportToPDF = async (elementId = 'results-section') => {
  try {
    // Metóda 1: Použitie window.print (najjednoduchšie)
    const element = document.getElementById(elementId);
    if (!element) {
      alert('Element na export sa nenašiel');
      return;
    }

    // Vytvoriť nové okno s obsahom
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
      <!DOCTYPE html>
      <html>
        <head>
          <title>ILUMINATI SYSTEM - Export</title>
          <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            h1 { color: #0B4EA2; }
            .node { margin: 10px 0; padding: 10px; border: 1px solid #ddd; }
            .risk-high { background-color: #fee2e2; }
            .risk-medium { background-color: #fed7aa; }
            .risk-low { background-color: #dbeafe; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #0B4EA2; color: white; }
            @media print {
              body { padding: 0; }
            }
          </style>
        </head>
        <body>
          <h1>ILUMINATI SYSTEM - Export</h1>
          <p>Dátum: ${new Date().toLocaleString('sk-SK')}</p>
          ${element.innerHTML}
        </body>
      </html>
    `);
    printWindow.document.close();
    
    // Počakať na načítanie a vytlačiť
    setTimeout(() => {
      printWindow.print();
    }, 250);
    
  } catch (error) {
    console.error('PDF export error:', error);
    alert('Export do PDF sa nepodaril. Použite tlač (Ctrl+P).');
  }
};

/**
 * Exportuje dáta do JSON
 */
export const exportToJSON = (data) => {
  if (!data) {
    alert('Žiadne dáta na export');
    return;
  }

  const json = JSON.stringify(data, null, 2);
  const blob = new Blob([json], { type: 'application/json' });
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);
  link.setAttribute('href', url);
  link.setAttribute('download', `iluminati-export-${new Date().toISOString().split('T')[0]}.json`);
  link.style.visibility = 'hidden';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

/**
 * Exportuje graf do Excel (xlsx) - volá backend API
 */
export const exportToExcel = async (data, token = null) => {
  if (!data || !data.nodes || !data.edges) {
    alert('Žiadne dáta na export');
    return;
  }

  try {
        // API_URL je importovaný z config/api.js
    const headers = {
      'Content-Type': 'application/json',
    };
    
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_URL}/api/export/excel`, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', `iluminati-export-${new Date().toISOString().split('T')[0]}.xlsx`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Excel export error:', error);
    alert('Export do Excel sa nepodaril. Skúste to znova alebo použite CSV export.');
  }
};

/**
 * Exportuje batch firiem do Excel (xlsx) - volá backend API
 */
export const exportBatchToExcel = async (companies, token = null) => {
  if (!companies || companies.length === 0) {
    alert('Žiadne firmy na export');
    return;
  }

  try {
        // API_URL je importovaný z config/api.js
    const headers = {
      'Content-Type': 'application/json',
    };
    
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_URL}/api/export/batch-excel`, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify(companies),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', `iluminati-batch-export-${new Date().toISOString().split('T')[0]}.xlsx`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Batch Excel export error:', error);
    alert('Export do Excel sa nepodaril. Skúste to znova.');
  }
};

