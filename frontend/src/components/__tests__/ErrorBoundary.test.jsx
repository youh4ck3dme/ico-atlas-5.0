import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import ErrorBoundary from '../ErrorBoundary';

// Komponenta, ktorá vyhodí chybu
const ThrowError = ({ shouldThrow }) => {
  if (shouldThrow) {
    throw new Error('Test error');
  }
  return <div>No error</div>;
};

describe('ErrorBoundary', () => {
  it('renders children when there is no error', () => {
    render(
      <ErrorBoundary>
        <div>Test content</div>
      </ErrorBoundary>
    );
    
    expect(screen.getByText('Test content')).toBeInTheDocument();
  });

  it('catches errors and displays error fallback', () => {
    // Suppress console.error pre tento test
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    
    render(
      <ErrorBoundary>
        <ThrowError shouldThrow={true} />
      </ErrorBoundary>
    );
    
    expect(screen.getByText('Niečo sa pokazilo')).toBeInTheDocument();
    expect(screen.getByText(/Ospravedlňujeme sa za nepríjemnosť/)).toBeInTheDocument();
    expect(screen.getByText('Obnoviť stránku')).toBeInTheDocument();
    expect(screen.getByText('Domov')).toBeInTheDocument();
    
    consoleSpy.mockRestore();
  });

  it('displays error message when error occurs', () => {
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    
    render(
      <ErrorBoundary>
        <ThrowError shouldThrow={true} />
      </ErrorBoundary>
    );
    
    expect(screen.getByText(/Test error/)).toBeInTheDocument();
    
    consoleSpy.mockRestore();
  });
});

