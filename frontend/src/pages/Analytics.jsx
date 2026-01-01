import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import ProtectedRoute from '../components/ProtectedRoute';
import IluminatiLogo from '../components/IluminatiLogo';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import {
  TrendingUp,
  Activity,
  Users,
  AlertTriangle,
  Globe,
  Loader2,
} from 'lucide-react';
import Disclaimer from '../components/Disclaimer';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

const Analytics = () => {
  const { user, token } = useAuth();
  const [loading, setLoading] = useState(true);
  const [dashboardData, setDashboardData] = useState(null);
  const [selectedPeriod, setSelectedPeriod] = useState(30);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (user?.tier === 'enterprise') {
      loadAnalytics();
    }
  }, [user, selectedPeriod]);

  const loadAnalytics = async () => {
    try {
      setLoading(true);
      setError(null);

      // Načítať kompletný dashboard
      const response = await fetch(
        `http://localhost:8000/api/analytics/dashboard`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        if (response.status === 403) {
          setError('Analytics dashboard is only available for Enterprise tier');
        } else {
          setError('Failed to load analytics data');
        }
        return;
      }

      const data = await response.json();
      setDashboardData(data.data);
    } catch (error) {
      console.error('Error loading analytics:', error);
      setError('Error loading analytics data');
    } finally {
      setLoading(false);
    }
  };

  if (user?.tier !== 'enterprise') {
    return (
      <ProtectedRoute requiredTier="enterprise">
        <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
          <div className="container mx-auto px-4 py-8">
            <div className="bg-white rounded-lg shadow-lg p-8 text-center">
              <AlertTriangle className="w-16 h-16 text-yellow-500 mx-auto mb-4" />
              <h2 className="text-2xl font-bold text-slate-800 mb-2">
                Enterprise Feature
              </h2>
              <p className="text-slate-600 mb-6">
                Analytics dashboard is only available for Enterprise tier users.
              </p>
              <button
                onClick={() => (window.location.href = '/dashboard')}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                Go to Dashboard
              </button>
            </div>
          </div>
        </div>
      </ProtectedRoute>
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-12 h-12 text-blue-600 animate-spin mx-auto mb-4" />
          <p className="text-slate-600">Loading analytics...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
        <div className="container mx-auto px-4 py-8">
          <div className="bg-white rounded-lg shadow-lg p-8 text-center">
            <AlertTriangle className="w-16 h-16 text-red-500 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-slate-800 mb-2">Error</h2>
            <p className="text-slate-600 mb-6">{error}</p>
            <button
              onClick={loadAnalytics}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Retry
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!dashboardData) {
    return null;
  }

  const { search_trends, risk_distribution, user_activity, api_usage } =
    dashboardData;

  // Formátovať dáta pre grafy
  const searchTrendsData = search_trends?.data || [];
  const riskDistData = risk_distribution?.distribution || [];
  const tierDistData = user_activity?.tier_distribution
    ? Object.entries(user_activity.tier_distribution).map(([tier, count]) => ({
        name: tier.charAt(0).toUpperCase() + tier.slice(1),
        value: count,
      }))
    : [];

  return (
    <ProtectedRoute requiredTier="enterprise">
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
        {/* Header */}
        <div className="bg-white shadow-sm border-b border-slate-200">
          <div className="container mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <IluminatiLogo className="w-10 h-10" />
                <div>
                  <h1 className="text-2xl font-bold text-slate-800">
                    Analytics Dashboard
                  </h1>
                  <p className="text-sm text-slate-600">
                    Business Intelligence & Insights
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <select
                  value={selectedPeriod}
                  onChange={(e) => setSelectedPeriod(Number(e.target.value))}
                  className="px-4 py-2 border border-slate-300 rounded-lg text-sm"
                >
                  <option value={7}>Last 7 days</option>
                  <option value={30}>Last 30 days</option>
                  <option value={90}>Last 90 days</option>
                </select>
                <button
                  onClick={loadAnalytics}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm"
                >
                  Refresh
                </button>
              </div>
            </div>
          </div>
        </div>

        <div className="container mx-auto px-4 py-8">
          {/* Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="bg-white rounded-lg shadow-lg p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-600 mb-1">Total Searches</p>
                  <p className="text-3xl font-bold text-slate-800">
                    {search_trends?.total || 0}
                  </p>
                </div>
                <TrendingUp className="w-12 h-12 text-blue-600" />
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-lg p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-600 mb-1">Active Users</p>
                  <p className="text-3xl font-bold text-slate-800">
                    {user_activity?.active_users || 0}
                  </p>
                </div>
                <Users className="w-12 h-12 text-green-600" />
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-lg p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-600 mb-1">High Risk</p>
                  <p className="text-3xl font-bold text-red-600">
                    {risk_distribution?.high_risk_count || 0}
                  </p>
                </div>
                <AlertTriangle className="w-12 h-12 text-red-600" />
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-lg p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-slate-600 mb-1">API Calls</p>
                  <p className="text-3xl font-bold text-slate-800">
                    {api_usage?.total_calls || 0}
                  </p>
                </div>
                <Activity className="w-12 h-12 text-purple-600" />
              </div>
            </div>
          </div>

          {/* Charts Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            {/* Search Trends */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-bold text-slate-800 mb-4 flex items-center gap-2">
                <TrendingUp className="w-5 h-5" />
                Search Trends
              </h3>
              {searchTrendsData.length > 0 ? (
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={searchTrendsData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line
                      type="monotone"
                      dataKey="count"
                      stroke="#3b82f6"
                      strokeWidth={2}
                      name="Searches"
                    />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <p className="text-slate-500 text-center py-12">
                  No search data available
                </p>
              )}
              {search_trends?.peak_hour && (
                <p className="text-sm text-slate-600 mt-4">
                  Peak hour: {search_trends.peak_hour}:00 | Peak day:{' '}
                  {search_trends.peak_day}
                </p>
              )}
            </div>

            {/* Risk Distribution */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-bold text-slate-800 mb-4 flex items-center gap-2">
                <AlertTriangle className="w-5 h-5" />
                Risk Score Distribution
              </h3>
              {riskDistData.length > 0 ? (
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={riskDistData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="score" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="count" fill="#ef4444" name="Companies" />
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <p className="text-slate-500 text-center py-12">
                  No risk data available
                </p>
              )}
              {risk_distribution?.average_score && (
                <p className="text-sm text-slate-600 mt-4">
                  Average risk score:{' '}
                  {risk_distribution.average_score.toFixed(2)}
                </p>
              )}
            </div>

            {/* Tier Distribution */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-bold text-slate-800 mb-4 flex items-center gap-2">
                <Users className="w-5 h-5" />
                User Tier Distribution
              </h3>
              {tierDistData.length > 0 ? (
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={tierDistData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) =>
                        `${name}: ${(percent * 100).toFixed(0)}%`
                      }
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {tierDistData.map((entry, index) => (
                        <Cell
                          key={`cell-${index}`}
                          fill={COLORS[index % COLORS.length]}
                        />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              ) : (
                <p className="text-slate-500 text-center py-12">
                  No user data available
                </p>
              )}
            </div>

            {/* API Usage */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-bold text-slate-800 mb-4 flex items-center gap-2">
                <Activity className="w-5 h-5" />
                API Usage
              </h3>
              {api_usage?.most_used_endpoints &&
              api_usage.most_used_endpoints.length > 0 ? (
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart
                    data={api_usage.most_used_endpoints}
                    layout="vertical"
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" />
                    <YAxis dataKey="endpoint" type="category" width={150} />
                    <Tooltip />
                    <Bar dataKey="count" fill="#8b5cf6" name="Calls" />
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <p className="text-slate-500 text-center py-12">
                  No API usage data available
                </p>
              )}
              {api_usage?.error_rate !== undefined && (
                <p className="text-sm text-slate-600 mt-4">
                  Error rate: {api_usage.error_rate}% | Calls/day:{' '}
                  {api_usage.calls_per_day?.toFixed(1) || 0}
                </p>
              )}
            </div>
          </div>

          {/* Additional Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h4 className="font-bold text-slate-800 mb-4">User Activity</h4>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-slate-600">New Users:</span>
                  <span className="font-semibold">
                    {user_activity?.new_users || 0}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-600">Retention Rate:</span>
                  <span className="font-semibold">
                    {user_activity?.retention_rate || 0}%
                  </span>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-lg p-6">
              <h4 className="font-bold text-slate-800 mb-4">Risk Summary</h4>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-slate-600">High Risk:</span>
                  <span className="font-semibold text-red-600">
                    {risk_distribution?.high_risk_count || 0}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-600">Medium Risk:</span>
                  <span className="font-semibold text-orange-600">
                    {risk_distribution?.medium_risk_count || 0}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-600">Low Risk:</span>
                  <span className="font-semibold text-green-600">
                    {risk_distribution?.low_risk_count || 0}
                  </span>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-lg p-6">
              <h4 className="font-bold text-slate-800 mb-4">Feature Usage</h4>
              <div className="space-y-2 text-sm">
                {user_activity?.feature_usage
                  ? Object.entries(user_activity.feature_usage).map(
                      ([feature, count]) => (
                        <div key={feature} className="flex justify-between">
                          <span className="text-slate-600 capitalize">
                            {feature}:
                          </span>
                          <span className="font-semibold">{count}</span>
                        </div>
                      )
                    )
                  : (
                    <p className="text-slate-500">No data available</p>
                  )}
              </div>
            </div>
          </div>

          {/* Disclaimer s zdrojmi dát */}
          <Disclaimer 
            sources={[
              { name: 'Obchodný register SR (ORSR)', url: 'https://www.orsr.sk' },
              { name: 'Živnostenský register SR (ZRSR)', url: 'https://www.zrsr.sk' },
              { name: 'Register účtovných závierok (RUZ)', url: 'https://www.registeruz.sk' },
              { name: 'ARES (ČR)', url: 'https://wwwinfo.mfcr.cz' },
              { name: 'Finančná správa SR', url: 'https://www.financnasprava.sk' },
            ]}
            showFullText={false}
          />
        </div>
      </div>
    </ProtectedRoute>
  );
};

export default Analytics;

