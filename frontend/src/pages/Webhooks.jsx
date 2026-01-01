import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import ProtectedRoute from '../components/ProtectedRoute';
import IluminatiLogo from '../components/IluminatiLogo';
import { Copy, Trash2, Plus, Webhook, CheckCircle, AlertCircle, Eye, EyeOff, Clock } from 'lucide-react';

const AVAILABLE_EVENTS = [
    'company.created',
    'company.updated',
    'risk_score.changed',
    'subscription.activated',
    'subscription.cancelled'
];

const Webhooks = () => {
  const { user, token } = useAuth();
  const [webhooks, setWebhooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newWebhook, setNewWebhook] = useState(null);
  const [selectedWebhook, setSelectedWebhook] = useState(null);
  const [logs, setLogs] = useState([]);
  const [copiedSecretId, setCopiedSecretId] = useState(null);
  const [formData, setFormData] = useState({
    url: '',
    events: [],
    secret: ''
  });

  useEffect(() => {
    if (user?.tier === 'enterprise') {
      loadWebhooks();
    }
  }, [user]);

  const loadWebhooks = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/enterprise/webhooks', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setWebhooks(data.webhooks || []);
      }
    } catch (error) {
      console.error('Error loading webhooks:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadWebhookLogs = async (webhookId) => {
    try {
      const response = await fetch(`http://localhost:8000/api/enterprise/webhooks/${webhookId}/logs?limit=20`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setLogs(data.logs || []);
      }
    } catch (error) {
      console.error('Error loading webhook logs:', error);
    }
  };

  const handleCreateWebhook = async (e) => {
    e.preventDefault();
    
    if (formData.events.length === 0) {
      alert('Please select at least one event type');
      return;
    }

    try {
      const payload = {
        url: formData.url,
        events: formData.events,
      };

      if (formData.secret) {
        payload.secret = formData.secret;
      }

      const response = await fetch('http://localhost:8000/api/enterprise/webhooks', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        const data = await response.json();
        setNewWebhook(data.data);
        setShowCreateForm(false);
        setFormData({
          url: '',
          events: [],
          secret: ''
        });
        loadWebhooks();
      }
    } catch (error) {
      console.error('Error creating webhook:', error);
    }
  };

  const handleDeleteWebhook = async (webhookId) => {
    if (!confirm('Are you sure you want to delete this webhook?')) {
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/api/enterprise/webhooks/${webhookId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        loadWebhooks();
        if (selectedWebhook === webhookId) {
          setSelectedWebhook(null);
          setLogs([]);
        }
      }
    } catch (error) {
      console.error('Error deleting webhook:', error);
    }
  };

  const toggleEvent = (event) => {
    if (formData.events.includes(event)) {
      setFormData({ ...formData, events: formData.events.filter(e => e !== event) });
    } else {
      setFormData({ ...formData, events: [...formData.events, event] });
    }
  };

  const copyToClipboard = (text, id) => {
    navigator.clipboard.writeText(text);
    setCopiedSecretId(id);
    setTimeout(() => setCopiedSecretId(null), 2000);
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Never';
    return new Date(dateString).toLocaleString();
  };

  if (user?.tier !== 'enterprise') {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-indigo-900 flex items-center justify-center p-4">
          <div className="max-w-md w-full bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-8 border border-white/20 text-center">
            <IluminatiLogo className="mx-auto mb-6" />
            <AlertCircle className="w-16 h-16 text-yellow-400 mx-auto mb-4" />
            <h1 className="text-2xl font-bold text-white mb-2">Enterprise Tier Required</h1>
            <p className="text-blue-200 mb-6">Webhooks are only available for Enterprise tier users.</p>
            <a
              href="/payment/checkout?tier=enterprise"
              className="inline-block bg-purple-600 hover:bg-purple-700 text-white font-semibold px-6 py-3 rounded-lg transition-colors"
            >
              Upgrade to Enterprise
            </a>
          </div>
        </div>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-indigo-900">
        <nav className="bg-white/10 backdrop-blur-lg border-b border-white/20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <IluminatiLogo />
              <a href="/dashboard" className="text-white hover:text-blue-200">Back to Dashboard</a>
            </div>
          </div>
        </nav>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex justify-between items-center mb-8">
            <div>
              <h1 className="text-3xl font-bold text-white mb-2">Webhooks</h1>
              <p className="text-blue-200">Manage real-time event notifications</p>
            </div>
            <button
              onClick={() => setShowCreateForm(!showCreateForm)}
              className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-3 rounded-lg transition-colors flex items-center gap-2"
            >
              <Plus size={20} />
              Create Webhook
            </button>
          </div>

          {/* New Webhook Display */}
          {newWebhook && (
            <div className="bg-green-500/20 border border-green-500 rounded-lg p-6 mb-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-2">
                  <CheckCircle className="text-green-400" size={24} />
                  <h3 className="text-xl font-bold text-white">Webhook Created!</h3>
                </div>
                <button
                  onClick={() => setNewWebhook(null)}
                  className="text-white hover:text-green-200"
                >
                  ×
                </button>
              </div>
              <div className="space-y-3">
                <div>
                  <label className="block text-sm font-medium text-white mb-1">Secret Key</label>
                  <div className="flex items-center gap-2">
                    <code className="flex-1 bg-black/30 rounded-lg p-3 text-green-300 font-mono text-sm break-all">
                      {newWebhook.secret}
                    </code>
                    <button
                      onClick={() => copyToClipboard(newWebhook.secret, 'new')}
                      className="text-green-300 hover:text-green-200"
                    >
                      {copiedSecretId === 'new' ? <CheckCircle size={20} /> : <Copy size={20} />}
                    </button>
                  </div>
                </div>
                <p className="text-yellow-300 text-sm font-semibold">
                  ⚠️ Save this secret now! It will not be shown again. Use it to verify webhook signatures.
                </p>
              </div>
            </div>
          )}

          {/* Create Form */}
          {showCreateForm && (
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-6 mb-6 border border-white/20">
              <h2 className="text-xl font-bold text-white mb-4">Create New Webhook</h2>
              <form onSubmit={handleCreateWebhook} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-white mb-2">Webhook URL</label>
                  <input
                    type="url"
                    value={formData.url}
                    onChange={(e) => setFormData({ ...formData, url: e.target.value })}
                    required
                    className="w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-blue-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="https://your-app.com/webhooks/iluminati"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-white mb-2">Events</label>
                  <div className="space-y-2 bg-white/5 rounded-lg p-4">
                    {AVAILABLE_EVENTS.map((event) => (
                      <label key={event} className="flex items-center text-white cursor-pointer hover:bg-white/5 p-2 rounded">
                        <input
                          type="checkbox"
                          checked={formData.events.includes(event)}
                          onChange={() => toggleEvent(event)}
                          className="mr-3"
                        />
                        <code className="text-sm">{event}</code>
                      </label>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-white mb-2">Secret (optional)</label>
                  <input
                    type="text"
                    value={formData.secret}
                    onChange={(e) => setFormData({ ...formData, secret: e.target.value })}
                    className="w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-blue-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Leave empty to auto-generate"
                  />
                  <p className="text-xs text-blue-200 mt-1">Used for HMAC signature verification</p>
                </div>

                <div className="flex gap-4">
                  <button
                    type="submit"
                    className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-2 rounded-lg transition-colors"
                  >
                    Create Webhook
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowCreateForm(false)}
                    className="bg-white/10 hover:bg-white/20 text-white font-semibold px-6 py-2 rounded-lg transition-colors"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          )}

          {/* Webhooks List */}
          {loading ? (
            <div className="text-center text-white py-12">Loading...</div>
          ) : webhooks.length === 0 ? (
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-12 border border-white/20 text-center">
              <Webhook className="w-16 h-16 text-blue-300 mx-auto mb-4" />
              <h3 className="text-xl font-bold text-white mb-2">No Webhooks</h3>
              <p className="text-blue-200 mb-6">Create your first webhook to receive real-time event notifications</p>
              <button
                onClick={() => setShowCreateForm(true)}
                className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-3 rounded-lg transition-colors"
              >
                Create Webhook
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Webhooks List */}
              <div className="lg:col-span-2 space-y-4">
                {webhooks.map((webhook) => (
                  <div
                    key={webhook.id}
                    className={`bg-white/10 backdrop-blur-lg rounded-lg p-6 border ${
                      webhook.is_active ? 'border-white/20' : 'border-red-500/50'
                    }`}
                  >
                    <div className="flex justify-between items-start mb-4">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <Webhook className="text-blue-300" size={20} />
                          <code className="text-white font-mono text-sm break-all">{webhook.url}</code>
                          {webhook.is_active ? (
                            <span className="px-2 py-1 bg-green-500/20 text-green-300 text-xs rounded">Active</span>
                          ) : (
                            <span className="px-2 py-1 bg-red-500/20 text-red-300 text-xs rounded">Inactive</span>
                          )}
                        </div>
                        <div className="flex flex-wrap gap-2 mb-3">
                          {webhook.events.map((event) => (
                            <span key={event} className="px-2 py-1 bg-blue-500/20 text-blue-300 text-xs rounded">
                              {event}
                            </span>
                          ))}
                        </div>
                        <div className="grid grid-cols-2 gap-4 text-sm text-blue-200">
                          <div>
                            <span className="font-semibold">Created:</span> {formatDate(webhook.created_at)}
                          </div>
                          <div>
                            <span className="font-semibold">Last Delivered:</span> {formatDate(webhook.last_delivered_at)}
                          </div>
                          <div>
                            <span className="font-semibold">Success:</span> {webhook.success_count}
                          </div>
                          <div>
                            <span className="font-semibold">Failures:</span> {webhook.failure_count}
                          </div>
                        </div>
                      </div>
                      <div className="flex gap-2">
                        <button
                          onClick={() => {
                            setSelectedWebhook(webhook.id);
                            loadWebhookLogs(webhook.id);
                          }}
                          className="text-blue-400 hover:text-blue-300 p-2"
                          title="View logs"
                        >
                          <Eye size={20} />
                        </button>
                        <button
                          onClick={() => handleDeleteWebhook(webhook.id)}
                          className="text-red-400 hover:text-red-300 p-2"
                          title="Delete webhook"
                        >
                          <Trash2 size={20} />
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Logs Panel */}
              {selectedWebhook && (
                <div className="lg:col-span-1 bg-white/10 backdrop-blur-lg rounded-lg p-6 border border-white/20">
                  <div className="flex justify-between items-center mb-4">
                    <h3 className="text-lg font-bold text-white">Delivery Logs</h3>
                    <button
                      onClick={() => setSelectedWebhook(null)}
                      className="text-white hover:text-blue-200"
                    >
                      ×
                    </button>
                  </div>
                  <div className="space-y-2 max-h-96 overflow-y-auto">
                    {logs.length === 0 ? (
                      <p className="text-blue-200 text-sm">No deliveries yet</p>
                    ) : (
                      logs.map((log) => (
                        <div
                          key={log.id}
                          className={`p-3 rounded text-sm ${
                            log.success ? 'bg-green-500/10 border border-green-500/30' : 'bg-red-500/10 border border-red-500/30'
                          }`}
                        >
                          <div className="flex items-center gap-2 mb-1">
                            {log.success ? (
                              <CheckCircle className="text-green-400" size={16} />
                            ) : (
                              <AlertCircle className="text-red-400" size={16} />
                            )}
                            <code className="text-white text-xs">{log.event_type}</code>
                          </div>
                          <div className="text-blue-200 text-xs">
                            <Clock size={12} className="inline mr-1" />
                            {formatDate(log.delivery_time)}
                          </div>
                          {log.response_status && (
                            <div className="text-xs text-blue-300 mt-1">
                              Status: {log.response_status}
                            </div>
                          )}
                          {log.error_message && (
                            <div className="text-xs text-red-300 mt-1">
                              {log.error_message}
                            </div>
                          )}
                        </div>
                      ))
                    )}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </ProtectedRoute>
  );
};

export default Webhooks;

