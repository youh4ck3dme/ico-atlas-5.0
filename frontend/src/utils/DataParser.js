import * as XLSX from 'xlsx';
import * as pdfjsLib from 'pdfjs-dist';

// Configure PDF.js worker
pdfjsLib.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.min.js`;

/**
 * Universal Data Parser for Theater Mode
 * Supports: CSV, Excel (.xlsx, .xls), JSON, PDF
 */
class DataParser {

    // Main parse method
    static async parse(file) {
        const type = file.name.split('.').pop().toLowerCase();

        switch (type) {
            case 'csv':
                return this.parseCSV(file);
            case 'xlsx':
            case 'xls':
                return this.parseExcel(file);
            case 'json':
                return this.parseJSON(file);
            case 'pdf':
                return this.parsePDF(file);
            default:
                throw new Error(`Nepodporovaný formát súboru: .${type}`);
        }
    }

    // Parse CSV
    static async parseCSV(file) {
        const text = await this.readFileAsText(file);
        const rows = text.split('\n').map(row => row.split(/,|;/)); // Support comma or semicolon

        // Simple data detection - assume headers are first row if useful
        const headers = rows[0].map(h => h.trim().toLowerCase());
        const data = rows.slice(1).filter(r => r.length > 1);

        const nodes = [];
        const edges = [];

        data.forEach((row, i) => {
            if (row.length < 2) return;

            // Try to identify columns
            const nameIdx = headers.findIndex(h => h.includes('názov') || h.includes('name') || h.includes('firma'));
            const icoIdx = headers.findIndex(h => h.includes('ico') || h.includes('ičo') || h.includes('id'));

            const name = nameIdx > -1 ? row[nameIdx] : row[0]; // Fallback to first col
            const ico = icoIdx > -1 ? row[icoIdx] : (nameIdx === 0 ? row[1] : row[nameIdx > -1 ? 0 : 1]); // Fallback logic

            const id = `import-node-${i}`;

            nodes.push({
                id: id,
                label: name.trim(),
                type: 'company',
                ico: ico ? ico.trim() : '',
                details: 'Importované z CSV'
            });
        });

        return { nodes, edges };
    }

    // Parse Excel
    static async parseExcel(file) {
        const buffer = await this.readFileAsArrayBuffer(file);
        const workbook = XLSX.read(buffer, { type: 'array' });
        const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
        const data = XLSX.utils.sheet_to_json(firstSheet);

        const nodes = [];
        const edges = [];

        data.forEach((row, i) => {
            // Flexible field matching
            const name = row['Obchodné meno'] || row['Názov'] || row['Name'] || row['Firma'] || Object.values(row)[0];
            const ico = row['IČO'] || row['ICO'] || row['ID'] || '';
            const type = row['Právna forma'] || row['Type'] || 'company';

            if (!name) return;

            const id = `import-excel-${i}`;

            nodes.push({
                id: id,
                label: String(name).trim(),
                type: 'company',
                ico: String(ico).trim(),
                details: String(type),
                dataQuality: 'excel-import'
            });
        });

        return { nodes, edges };
    }

    // Parse JSON
    static async parseJSON(file) {
        const text = await this.readFileAsText(file);
        try {
            const data = JSON.parse(text);

            // Expected format: { nodes: [], edges: [] } or simple array
            if (data.nodes && Array.isArray(data.nodes)) {
                return data; // Assume valid format
            } else if (Array.isArray(data)) {
                // Array of companies
                const nodes = data.map((item, i) => ({
                    id: item.id || `json-node-${i}`,
                    label: item.name || item.nazov || item.label || 'Unknown',
                    type: item.type || 'company',
                    ...item
                }));
                return { nodes, edges: [] };
            }

            throw new Error('Neznáma štruktúra JSON');
        } catch (e) {
            throw new Error('Chyba pri parsovaní JSON: ' + e.message);
        }
    }

    // Parse PDF (Extract text)
    static async parsePDF(file) {
        const buffer = await this.readFileAsArrayBuffer(file);
        const pdf = await pdfjsLib.getDocument({ data: buffer }).promise;
        let fullText = '';

        for (let i = 1; i <= pdf.numPages; i++) {
            const page = await pdf.getPage(i);
            const textContent = await page.getTextContent();
            const pageText = textContent.items.map(item => item.str).join(' ');
            fullText += pageText + '\n';
        }

        // Basic extraction heuristics for IČO and Company Names
        const nodes = [];
        const lines = fullText.split('\n');

        // Regex for IČO (8 digits)
        const icoRegex = /\b\d{8}\b/g;
        const icos = fullText.match(icoRegex) || [];

        // Simple node creation from found IČOs
        icos.forEach((ico, i) => {
            nodes.push({
                id: `pdf-node-${i}`,
                label: `Firma ${ico}`, // Cannot easily extract name without backend NLP
                type: 'company',
                ico: ico,
                details: 'Nájdené v PDF'
            });
        });

        return { nodes, edges: [], rawText: fullText };
    }

    // Helper: Read file as Text
    static readFileAsText(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => resolve(e.target.result);
            reader.onerror = (e) => reject(e);
            reader.readAsText(file);
        });
    }

    // Helper: Read file as ArrayBuffer
    static readFileAsArrayBuffer(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => resolve(e.target.result);
            reader.onerror = (e) => reject(e);
            reader.readAsArrayBuffer(file);
        });
    }
}

export default DataParser;
