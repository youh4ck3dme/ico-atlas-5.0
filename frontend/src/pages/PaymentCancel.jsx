import { Link } from 'react-router-dom';
import IluminatiLogo from '../components/IluminatiLogo';

const PaymentCancel = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-indigo-900 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-8 border border-white/20 text-center">
        <IluminatiLogo className="mx-auto mb-6" />
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-white mb-2">Payment Cancelled</h1>
          <p className="text-blue-200">Your payment was cancelled. No charges were made.</p>
        </div>
        <div className="space-y-4">
          <Link
            to="/dashboard"
            className="block w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors"
          >
            Back to Dashboard
          </Link>
          <Link
            to="/payment/checkout"
            className="block w-full bg-white/10 hover:bg-white/20 text-white font-semibold py-3 px-4 rounded-lg transition-colors border border-white/20"
          >
            Try Again
          </Link>
        </div>
      </div>
    </div>
  );
};

export default PaymentCancel;

