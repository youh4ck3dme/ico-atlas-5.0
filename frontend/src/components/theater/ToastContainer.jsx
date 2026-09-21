import React from 'react';
import { X, AlertCircle, CheckCircle, Info } from 'lucide-react';
import { useToast } from '../../contexts/ToastContext';
import '../../styles/theater.css';

const ToastContainer = () => {
    const { toasts, removeToast } = useToast();

    return (
        <div className="toast-container">
            {toasts.map(toast => (
                <div key={toast.id} className={`toast-item toast-${toast.type}`}>
                    <div className="toast-icon">
                        {toast.type === 'error' && <AlertCircle size={20} />}
                        {toast.type === 'success' && <CheckCircle size={20} />}
                        {toast.type === 'info' && <Info size={20} />}
                    </div>
                    <div className="toast-message">{toast.message}</div>
                    <button
                        className="toast-close"
                        onClick={() => removeToast(toast.id)}
                    >
                        <X size={16} />
                    </button>
                    <div className="toast-progress" style={{ animationDuration: `${toast.duration}ms` }} />
                </div>
            ))}
        </div>
    );
};

export default ToastContainer;
