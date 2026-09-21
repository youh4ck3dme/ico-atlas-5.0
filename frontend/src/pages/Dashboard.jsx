import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import IluminatiLogo from '../components/IluminatiLogo';
import { exportBatchToExcel } from '../utils/export';
import { Download } from 'lucide-react';

const Dashboard = () => {
  const { user, logout, refreshUser } = useAuth();
  const navigate = useNavigate();
  const [searchHistory, setSearchHistory] = useState([]);
  const [favorites, setFavorites] = useState([]);
  const [tierLimits, setTierLimits] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const token = localStorage.getItem('access_token');
      
      // Načítať tier limits
      const limitsResponse = await fetch('http://localhost:8000/api/auth/tier/limits', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (limitsResponse.ok) {
        const limits = await limitsResponse.json();
        setTierLimits(limits);
      }

      // Načítať search history
      const historyResponse = await fetch('http://localhost:8000/api/search/history', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (historyResponse.ok) {
        const history = await historyResponse.json();
        setSearchHistory(history.slice(0, 10)); // Posledných 10
      }

      // Načítať favorites
      const favoritesResponse = await fetch('http://localhost:8000/api/user/favorites', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (favoritesResponse.ok) {
        const favoritesData = await favoritesResponse.json();
        setFavorites(favoritesData.favorites || []);
      }
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUpgrade = async (tier) => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`http://localhost:8000/api/payment/checkout?tier=${tier}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        if (data.url) {
          window.location.href = data.url; // Redirect to Stripe Checkout
        }
      }
    } catch (error) {
      console.error('Error creating checkout:', error);
    }
  };

  const getTierColor = (tier) => {
    switch (tier) {
      case 'free':
        return 'bg-gray-500';
      case 'pro':
        return 'bg-blue-500';
      case 'enterprise':
        return 'bg-purple-500';
      default:
        return 'bg-gray-500';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-indigo-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-indigo-900">
      <nav className="bg-white/10 backdrop-blur-lg border-b border-white/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <IluminatiLogo />
            <div className="flex items-center space-x-4">
              <span className="text-white">{user?.email}</span>
              <button
                onClick={logout}
                className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition-colors"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* User Profile Card */}
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-6 mb-6 border border-white/20">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-white mb-2">
                {user?.full_name || 'User'}
              </h2>
              <p className="text-blue-200">{user?.email}</p>
            </div>
            <div className="text-right">
              <div className={`inline-block px-4 py-2 rounded-lg text-white font-semibold ${getTierColor(user?.tier)}`}>
                {user?.tier?.toUpperCase() || 'FREE'}
              </div>
              {user?.tier === 'free' && (
                <button
                  onClick={() => handleUpgrade('pro')}
                  className="mt-2 block w-full bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
                >
                  Upgrade to PRO
                </button>
              )}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Usage Statistics */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-6 border border-white/20">
            <h3 className="text-xl font-bold text-white mb-4">Usage Statistics</h3>
            {tierLimits ? (
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between text-white mb-2">
                    <span>Searches per day</span>
                    <span className="font-semibold">
                      {tierLimits.searches_per_day === -1 ? 'Unlimited' : tierLimits.searches_per_day}
                    </span>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-white mb-2">
                    <span>Max graph nodes</span>
                    <span className="font-semibold">
                      {tierLimits.max_graph_nodes === -1 ? 'Unlimited' : tierLimits.max_graph_nodes}
                    </span>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-white mb-2">
                    <span>PDF Export</span>
                    <span className="font-semibold">
                      {tierLimits.can_export_pdf ? '✅ Enabled' : '❌ Disabled'}
                    </span>
                  </div>
                </div>
              </div>
            ) : (
              <p className="text-blue-200">Loading limits...</p>
            )}
          </div>

          {/* Search History */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-6 border border-white/20">
            <h3 className="text-xl font-bold text-white mb-4">Recent Searches</h3>
            {searchHistory.length > 0 ? (
              <div className="space-y-2">
                {searchHistory.map((search, index) => (
                  <div
                    key={index}
                    className="bg-white/5 rounded-lg p-3 text-white"
                  >
                    <div className="font-semibold">{search.query}</div>
                    <div className="text-sm text-blue-200">
                      {new Date(search.timestamp).toLocaleDateString()}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-blue-200">No search history yet</p>
            )}
          </div>
        </div>

        {/* Favorite Companies */}
        <div className="mt-6 bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-6 border border-white/20">
          <h3 className="text-xl font-bold text-white mb-4">Favorite Companies</h3>
          {favorites.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {favorites.map((favorite) => (
                <div
                  key={favorite.id}
                  className="bg-white/5 rounded-lg p-4 text-white hover:bg-white/10 transition-colors"
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex-1">
                      <div className="font-semibold text-lg">{favorite.company_name}</div>
                      <div className="text-sm text-blue-200">
                        {favorite.company_identifier} • {favorite.country}
                      </div>
                    </div>
                    <button
                      onClick={async () => {
                        try {
                          const token = localStorage.getItem('access_token');
                          const response = await fetch(
                            `http://localhost:8000/api/user/favorites/${favorite.id}`,
                            {
                              method: 'DELETE',
                              headers: {
                                'Authorization': `Bearer ${token}`,
                              },
                            }
                          );
                          if (response.ok) {
                            setFavorites(favorites.filter(f => f.id !== favorite.id));
                          }
                        } catch (error) {
                          console.error('Error removing favorite:', error);
                        }
                      }}
                      className="text-red-400 hover:text-red-300 ml-2"
                      title="Remove from favorites"
                    >
                      ✕
                    </button>
                  </div>
                  {favorite.risk_score !== null && (
                    <div className="mt-2">
                      <span className={`px-2 py-1 rounded text-xs font-semibold ${
                        favorite.risk_score >= 7 ? 'bg-red-500/20 text-red-300' :
                        favorite.risk_score >= 4 ? 'bg-orange-500/20 text-orange-300' :
                        'bg-green-500/20 text-green-300'
                      }`}>
                        Risk: {favorite.risk_score.toFixed(1)}
                      </span>
                    </div>
                  )}
                  {favorite.notes && (
                    <div className="mt-2 text-sm text-blue-200 italic">
                      "{favorite.notes}"
                    </div>
                  )}
                  <button
                    onClick={() => navigate(`/?q=${favorite.company_identifier}`)}
                    className="mt-3 w-full bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors text-sm"
                  >
                    View Details
                  </button>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-blue-200">No favorite companies yet. Add companies to favorites from search results.</p>
          )}
        </div>

        {/* Quick Actions */}
        <div className="mt-6 bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-6 border border-white/20">
          <h3 className="text-xl font-bold text-white mb-4">Quick Actions</h3>
          <div className="flex flex-wrap gap-4">
            <button
              onClick={() => navigate('/')}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg transition-colors"
            >
              New Search
            </button>
            {user?.tier === 'enterprise' && (
              <>
                <button
                  onClick={() => navigate('/api-keys')}
                  className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg transition-colors"
                >
                  API Keys
                </button>
                <button
                  onClick={() => navigate('/webhooks')}
                  className="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-lg transition-colors"
                >
                  Webhooks
                </button>
                <button
                  onClick={() => navigate('/erp-integrations')}
                  className="bg-teal-600 hover:bg-teal-700 text-white px-6 py-3 rounded-lg transition-colors"
                >
                  ERP Integrations
                </button>
                <button
                  onClick={() => navigate('/analytics')}
                  className="bg-pink-600 hover:bg-pink-700 text-white px-6 py-3 rounded-lg transition-colors"
                >
                  Analytics
                </button>
              </>
            )}
            {user?.tier === 'free' && (
              <button
                onClick={() => handleUpgrade('pro')}
                className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg transition-colors"
              >
                Upgrade to PRO
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

