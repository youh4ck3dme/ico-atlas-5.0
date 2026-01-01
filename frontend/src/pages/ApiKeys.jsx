import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import ProtectedRoute from '../components/ProtectedRoute';
import IluminatiLogo from '../components/IluminatiLogo';
import { Copy, Trash2, Plus, Key, Eye, EyeOff, CheckCircle, AlertCircle } from 'lucide-react';

const ApiKeys = () => {
  const { user, token } = useAuth();
  const [apiKeys, setApiKeys] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newKey, setNewKey] = useState(null);
  const [copiedKeyId, setCopiedKeyId] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    expires_days: '',
    permissions: ['read'],
    ip_whitelist: ''
  });

  useEffect(() => {
    if (user?.tier === 'enterprise') {
      loadApiKeys();
    }
  }, [user]);

  const loadApiKeys = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/enterprise/keys', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setApiKeys(data.keys || []);
      }
    } catch (error) {
      console.error('Error loading API keys:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateKey = async (e) => {
    e.preventDefault();
    
    try {
      const payload = {
        name: formData.name,
        permissions: formData.permissions,
      };

      if (formData.expires_days) {
        payload.expires_days = parseInt(formData.expires_days);
      }

      if (formData.ip_whitelist) {
        payload.ip_whitelist = formData.ip_whitelist.split(',').map(ip => ip.trim()).filter(ip => ip);
      }

      const response = await fetch('http://localhost:8000/api/enterprise/keys', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        const data = await response.json();
        setNewKey(data.data);
        setShowCreateForm(false);
        setFormData({
          name: '',
          expires_days: '',
          permissions: ['read'],
          ip_whitelist: ''
        });
        loadApiKeys();
      }
    } catch (error) {
      console.error('Error creating API key:', error);
    }
  };

  const handleRevokeKey = async (keyId) => {
    if (!confirm('Are you sure you want to revoke this API key?')) {
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/api/enterprise/keys/${keyId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        loadApiKeys();
      }
    } catch (error) {
      console.error('Error revoking API key:', error);
    }
  };

  const copyToClipboard = (text, keyId) => {
    navigator.clipboard.writeText(text);
    setCopiedKeyId(keyId);
    setTimeout(() => setCopiedKeyId(null), 2000);
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Never';
    return new Date(dateString).toLocaleDateString();
  };

  if (user?.tier !== 'enterprise') {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-indigo-900 flex items-center justify-center p-4">
          <div className="max-w-md w-full bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-8 border border-white/20 text-center">
            <IluminatiLogo className="mx-auto mb-6" />
            <AlertCircle className="w-16 h-16 text-yellow-400 mx-auto mb-4" />
            <h1 className="text-2xl font-bold text-white mb-2">Enterprise Tier Required</h1>
            <p className="text-blue-200 mb-6">API Keys are only available for Enterprise tier users.</p>
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
              <h1 className="text-3xl font-bold text-white mb-2">API Keys</h1>
              <p className="text-blue-200">Manage your API keys for programmatic access</p>
            </div>
            <button
              onClick={() => setShowCreateForm(!showCreateForm)}
              className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-3 rounded-lg transition-colors flex items-center gap-2"
            >
              <Plus size={20} />
              Create API Key
            </button>
          </div>

          {/* New Key Display */}
          {newKey && (
            <div className="bg-green-500/20 border border-green-500 rounded-lg p-6 mb-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-2">
                  <CheckCircle className="text-green-400" size={24} />
                  <h3 className="text-xl font-bold text-white">API Key Created!</h3>
                </div>
                <button
                  onClick={() => setNewKey(null)}
                  className="text-white hover:text-green-200"
                >
                  ×
                </button>
              </div>
              <div className="bg-black/30 rounded-lg p-4 mb-4">
                <div className="flex items-center justify-between">
                  <code className="text-green-300 font-mono text-sm break-all">{newKey.key}</code>
                  <button
                    onClick={() => copyToClipboard(newKey.key, 'new')}
                    className="ml-4 text-green-300 hover:text-green-200"
                  >
                    {copiedKeyId === 'new' ? <CheckCircle size={20} /> : <Copy size={20} />}
                  </button>
                </div>
              </div>
              <p className="text-yellow-300 text-sm font-semibold">
                ⚠️ Save this key now! It will not be shown again.
              </p>
            </div>
          )}

          {/* Create Form */}
          {showCreateForm && (
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-6 mb-6 border border-white/20">
              <h2 className="text-xl font-bold text-white mb-4">Create New API Key</h2>
              <form onSubmit={handleCreateKey} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-white mb-2">Name</label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    required
                    className="w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-blue-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="e.g., Production API Key"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-white mb-2">Expires in (days)</label>
                  <input
                    type="number"
                    value={formData.expires_days}
                    onChange={(e) => setFormData({ ...formData, expires_days: e.target.value })}
                    className="w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-blue-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Leave empty for no expiration"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-white mb-2">Permissions</label>
                  <div className="space-y-2">
                    <label className="flex items-center text-white">
                      <input
                        type="checkbox"
                        checked={formData.permissions.includes('read')}
                        onChange={(e) => {
                          if (e.target.checked) {
                            setFormData({ ...formData, permissions: [...formData.permissions, 'read'] });
                          } else {
                            setFormData({ ...formData, permissions: formData.permissions.filter(p => p !== 'read') });
                          }
                        }}
                        className="mr-2"
                      />
                      Read
                    </label>
                    <label className="flex items-center text-white">
                      <input
                        type="checkbox"
                        checked={formData.permissions.includes('write')}
                        onChange={(e) => {
                          if (e.target.checked) {
                            setFormData({ ...formData, permissions: [...formData.permissions, 'write'] });
                          } else {
                            setFormData({ ...formData, permissions: formData.permissions.filter(p => p !== 'write') });
                          }
                        }}
                        className="mr-2"
                      />
                      Write
                    </label>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-white mb-2">IP Whitelist (comma-separated)</label>
                  <input
                    type="text"
                    value={formData.ip_whitelist}
                    onChange={(e) => setFormData({ ...formData, ip_whitelist: e.target.value })}
                    className="w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-blue-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="e.g., 192.168.1.1, 10.0.0.1"
                  />
                </div>

                <div className="flex gap-4">
                  <button
                    type="submit"
                    className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-2 rounded-lg transition-colors"
                  >
                    Create Key
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

          {/* API Keys List */}
          {loading ? (
            <div className="text-center text-white py-12">Loading...</div>
          ) : apiKeys.length === 0 ? (
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-12 border border-white/20 text-center">
              <Key className="w-16 h-16 text-blue-300 mx-auto mb-4" />
              <h3 className="text-xl font-bold text-white mb-2">No API Keys</h3>
              <p className="text-blue-200 mb-6">Create your first API key to get started</p>
              <button
                onClick={() => setShowCreateForm(true)}
                className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-3 rounded-lg transition-colors"
              >
                Create API Key
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              {apiKeys.map((key) => (
                <div
                  key={key.id}
                  className={`bg-white/10 backdrop-blur-lg rounded-lg p-6 border ${
                    key.is_active ? 'border-white/20' : 'border-red-500/50'
                  }`}
                >
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="text-lg font-bold text-white">{key.name}</h3>
                        {key.is_active ? (
                          <span className="px-2 py-1 bg-green-500/20 text-green-300 text-xs rounded">Active</span>
                        ) : (
                          <span className="px-2 py-1 bg-red-500/20 text-red-300 text-xs rounded">Revoked</span>
                        )}
                      </div>
                      <div className="flex items-center gap-2 mb-2">
                        <code className="text-blue-300 font-mono text-sm">{key.prefix}****</code>
                        <button
                          onClick={() => copyToClipboard(key.prefix + '****', key.id)}
                          className="text-blue-300 hover:text-blue-200"
                        >
                          {copiedKeyId === key.id ? <CheckCircle size={16} /> : <Copy size={16} />}
                        </button>
                      </div>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-blue-200">
                        <div>
                          <span className="font-semibold">Created:</span> {formatDate(key.created_at)}
                        </div>
                        <div>
                          <span className="font-semibold">Expires:</span> {formatDate(key.expires_at) || 'Never'}
                        </div>
                        <div>
                          <span className="font-semibold">Last Used:</span> {formatDate(key.last_used_at)}
                        </div>
                        <div>
                          <span className="font-semibold">Usage:</span> {key.usage_count} requests
                        </div>
                      </div>
                      <div className="mt-2 flex gap-2">
                        {key.permissions.map((perm) => (
                          <span key={perm} className="px-2 py-1 bg-blue-500/20 text-blue-300 text-xs rounded">
                            {perm}
                          </span>
                        ))}
                      </div>
                    </div>
                    {key.is_active && (
                      <button
                        onClick={() => handleRevokeKey(key.id)}
                        className="text-red-400 hover:text-red-300 p-2"
                        title="Revoke key"
                      >
                        <Trash2 size={20} />
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </ProtectedRoute>
  );
};

export default ApiKeys;

