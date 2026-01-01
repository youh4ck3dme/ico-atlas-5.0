import React from 'react';
import { AlertTriangle, RefreshCw, Home } from 'lucide-react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
    this.setState({
      error,
      errorInfo
    });
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <ErrorFallback 
          error={this.state.error} 
          onReset={this.handleReset}
        />
      );
    }

    return this.props.children;
  }
}

function ErrorFallback({ error, onReset }) {
  // ErrorFallback musí byť mimo ErrorBoundary class, ale potrebuje navigate
  // Použijeme window.location namiesto navigate

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-lg shadow-corp border border-slate-200 p-8 text-center">
        <div className="mb-6">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-red-100 mb-4">
            <AlertTriangle size={32} className="text-red-600" />
          </div>
          <h1 className="text-2xl font-bold text-slate-900 mb-2">
            Niečo sa pokazilo
          </h1>
          <p className="text-slate-600 text-sm">
            Ospravedlňujeme sa za nepríjemnosť. Aplikácia narazila na neočakávanú chybu.
          </p>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-slate-50 rounded-lg text-left">
            <p className="text-xs font-mono text-slate-500 break-all">
              {error.toString()}
            </p>
          </div>
        )}

        <div className="flex gap-3 justify-center">
          <button
            onClick={onReset}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2 text-sm font-medium"
          >
            <RefreshCw size={16} />
            Obnoviť stránku
          </button>
          <button
            onClick={() => window.location.href = '/'}
            className="px-4 py-2 bg-slate-200 text-slate-700 rounded-lg hover:bg-slate-300 transition-colors flex items-center gap-2 text-sm font-medium"
          >
            <Home size={16} />
            Domov
          </button>
        </div>

        <p className="mt-6 text-xs text-slate-500">
          Ak problém pretrváva, kontaktujte podporu.
        </p>
      </div>
    </div>
  );
}

export default ErrorBoundary;

