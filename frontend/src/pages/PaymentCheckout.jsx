import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import ProtectedRoute from '../components/ProtectedRoute';
import IluminatiLogo from '../components/IluminatiLogo';

const PaymentCheckout = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const tier = searchParams.get('tier') || 'pro';
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const tiers = {
    pro: {
      name: 'PRO',
      price: '$19.99',
      priceId: 'price_pro_monthly',
      features: [
        '100 searches per day',
        'Up to 100 graph nodes',
        'PDF export enabled',
        'Advanced risk analysis',
        'Priority support',
      ],
    },
    enterprise: {
      name: 'ENTERPRISE',
      price: '$99.99',
      priceId: 'price_enterprise_monthly',
      features: [
        'Unlimited searches',
        'Up to 500 graph nodes',
        'PDF export enabled',
        'Advanced risk analysis',
        'API access',
        'Dedicated support',
        'Custom integrations',
      ],
    },
  };

  const handleCheckout = async (selectedTier) => {
    setLoading(true);
    setError('');

    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`http://localhost:8000/api/payment/checkout?tier=${selectedTier}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to create checkout session');
      }

      const data = await response.json();
      if (data.url) {
        // Redirect to Stripe Checkout
        window.location.href = data.url;
      } else {
        throw new Error('No checkout URL received');
      }
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const selectedTierData = tiers[tier] || tiers.pro;

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-indigo-900">
        <nav className="bg-white/10 backdrop-blur-lg border-b border-white/20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <IluminatiLogo />
              <button
                onClick={() => navigate('/dashboard')}
                className="text-white hover:text-blue-200"
              >
                Back to Dashboard
              </button>
            </div>
          </div>
        </nav>

        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-white mb-2">Upgrade Your Plan</h1>
            <p className="text-blue-200">Choose the plan that's right for you</p>
          </div>

          {error && (
            <div className="bg-red-500/20 border border-red-500 text-red-100 px-4 py-3 rounded-lg mb-6">
              {error}
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* PRO Tier */}
            <div className={`bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-8 border-2 ${
              tier === 'pro' ? 'border-blue-500' : 'border-white/20'
            }`}>
              <div className="text-center mb-6">
                <h3 className="text-2xl font-bold text-white mb-2">PRO</h3>
                <div className="text-4xl font-bold text-white mb-2">$19.99</div>
                <div className="text-blue-200">per month</div>
              </div>
              <ul className="space-y-3 mb-6">
                {tiers.pro.features.map((feature, index) => (
                  <li key={index} className="flex items-start text-white">
                    <span className="text-green-400 mr-2">✓</span>
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>
              <button
                onClick={() => handleCheckout('pro')}
                disabled={loading || user?.tier === 'pro'}
                className={`w-full py-3 px-4 rounded-lg font-semibold transition-colors ${
                  user?.tier === 'pro'
                    ? 'bg-gray-500 cursor-not-allowed'
                    : 'bg-blue-600 hover:bg-blue-700 text-white'
                }`}
              >
                {user?.tier === 'pro' ? 'Current Plan' : loading ? 'Processing...' : 'Upgrade to PRO'}
              </button>
            </div>

            {/* ENTERPRISE Tier */}
            <div className={`bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-8 border-2 ${
              tier === 'enterprise' ? 'border-purple-500' : 'border-white/20'
            }`}>
              <div className="text-center mb-6">
                <h3 className="text-2xl font-bold text-white mb-2">ENTERPRISE</h3>
                <div className="text-4xl font-bold text-white mb-2">$99.99</div>
                <div className="text-blue-200">per month</div>
              </div>
              <ul className="space-y-3 mb-6">
                {tiers.enterprise.features.map((feature, index) => (
                  <li key={index} className="flex items-start text-white">
                    <span className="text-green-400 mr-2">✓</span>
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>
              <button
                onClick={() => handleCheckout('enterprise')}
                disabled={loading || user?.tier === 'enterprise'}
                className={`w-full py-3 px-4 rounded-lg font-semibold transition-colors ${
                  user?.tier === 'enterprise'
                    ? 'bg-gray-500 cursor-not-allowed'
                    : 'bg-purple-600 hover:bg-purple-700 text-white'
                }`}
              >
                {user?.tier === 'enterprise' ? 'Current Plan' : loading ? 'Processing...' : 'Upgrade to ENTERPRISE'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
};

export default PaymentCheckout;

