import { describe, it, expect, vi } from 'vitest';
import DataParser from './DataParser';

// Mocking dependencies
vi.mock('xlsx', () => ({
    read: vi.fn(() => ({
        SheetNames: ['Sheet1'],
        Sheets: {
            Sheet1: {}
        }
    })),
    utils: {
        sheet_to_json: vi.fn(() => [
            { 'Názov': 'Test Firma s.r.o.', 'IČO': '12345678', 'Právna forma': 's.r.o.' }
        ])
    }
}));

vi.mock('pdfjs-dist', () => ({
    version: '3.0',
    GlobalWorkerOptions: { workerSrc: '' },
    getDocument: vi.fn(() => ({
        promise: Promise.resolve({
            numPages: 1,
            getPage: vi.fn(() => Promise.resolve({
                getTextContent: vi.fn(() => Promise.resolve({
                    items: [{ str: 'Zmluva pre 12345678' }]
                }))
            }))
        })
    }))
}));

describe('DataParser', () => {
    it('should parse JSON correctly', async () => {
        const mockFile = new File([JSON.stringify({
            nodes: [{ id: '1', label: 'Test', type: 'company' }],
            edges: []
        })], 'test.json', { type: 'application/json' });

        // Mocking readFileAsText to avoid browser specific errors
        vi.spyOn(DataParser, 'readFileAsText').mockResolvedValue(
            JSON.stringify({ nodes: [{ id: '1', label: 'Test', type: 'company' }], edges: [] })
        );

        const result = await DataParser.parseJSON(mockFile);
        expect(result.nodes).toHaveLength(1);
        expect(result.nodes[0].label).toBe('Test');
    });

    it('should parse CSV correctly', async () => {
        const csvContent = 'Názov,IČO\nTest Firma,12345678';
        const mockFile = new File([csvContent], 'test.csv', { type: 'text/csv' });

        vi.spyOn(DataParser, 'readFileAsText').mockResolvedValue(csvContent);

        const result = await DataParser.parseCSV(mockFile);
        expect(result.nodes).toHaveLength(1);
        expect(result.nodes[0].label).toBe('Test Firma');
        expect(result.nodes[0].ico).toBe('12345678');
    });

    it('should throw error for unsupported type', async () => {
        const mockFile = new File([''], 'test.txt');
        await expect(DataParser.parse(mockFile)).rejects.toThrow('Nepodporovaný formát súboru');
    });
});
