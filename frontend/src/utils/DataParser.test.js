import { describe, it, expect, vi } from 'vitest';
import DataParser from './DataParser';

// Mock pdfjs-dist
vi.mock('pdfjs-dist', () => ({
    GlobalWorkerOptions: {
        workerSrc: ''
    },
    version: 'mocked',
    getDocument: vi.fn().mockReturnValue({
        promise: Promise.resolve({
            numPages: 1,
            getPage: vi.fn().mockResolvedValue({
                getTextContent: vi.fn().mockResolvedValue({
                    items: [{ str: '12345678' }]
                })
            })
        })
    })
}));

// Mock xlsx
vi.mock('xlsx', () => ({
    read: vi.fn(),
    utils: {
        sheet_to_json: vi.fn()
    }
}));

// Mock FileReader
class MockFileReader {
    readAsText(file) {
        setTimeout(() => {
            if (this.onload) {
                this.onload({ target: { result: file.content || '' } });
            }
        }, 0);
    }
    readAsArrayBuffer(file) {
        setTimeout(() => {
            if (this.onload) {
                this.onload({ target: { result: new ArrayBuffer(8) } });
            }
        }, 0);
    }
}
global.FileReader = MockFileReader;

describe('DataParser', () => {
    it('should parse JSON correctly', async () => {
        const mockFile = {
            name: 'test.json',
            content: JSON.stringify([
                { id: '1', name: 'Test Firm', type: 'company' }
            ])
        };

        const result = await DataParser.parseJSON(mockFile);
        expect(result.nodes).toHaveLength(1);
        expect(result.nodes[0].label).toBe('Test Firm');
    });

    it('should parse CSV correctly', async () => {
        const mockFile = {
            name: 'test.csv',
            content: 'Názov;IČO\nTest s.r.o.;12345678'
        };

        const result = await DataParser.parseCSV(mockFile);
        expect(result.nodes).toHaveLength(1);
        expect(result.nodes[0].label).toBe('Test s.r.o.');
        expect(result.nodes[0].ico).toBe('12345678');
    });

    it('should throw error for unsupported format', async () => {
        const mockFile = { name: 'test.txt' };
        await expect(DataParser.parse(mockFile)).rejects.toThrow('Nepodporovaný formát súboru');
    });
});
