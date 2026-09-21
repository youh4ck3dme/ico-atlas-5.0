import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const ErpIntegrations = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [connections, setConnections] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedErp, setSelectedErp] = useState('pohoda');
  const [formData, setFormData] = useState({
    api_key: '',
    company_id: '',
    base_url: '',
    username: '',
    password: '',
    server_url: '',
    company_db: ''
  });
  const [syncLogs, setSyncLogs] = useState({});
  const [syncing, setSyncing] = useState({});

  useEffect(() => {
    if (user?.tier !== 'enterprise') {
      return;
    }
    loadConnections();
  }, [user]);

  const loadConnections = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/enterprise/erp/connections', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setConnections(data.connections || []);
      }
    } catch (error) {
      console.error('Error loading connections:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddConnection = async (e) => {
    e.preventDefault();
    
    const connectionData = {};
    if (selectedErp === 'pohoda' || selectedErp === 'money_s3') {
      connectionData.api_key = formData.api_key;
      connectionData.company_id = formData.company_id;
      connectionData.base_url = formData.base_url || (selectedErp === 'pohoda' ? 'https://api.pohoda.sk' : 'https://api.moneys3.cz');
    } else if (selectedErp === 'sap') {
      connectionData.server_url = formData.server_url;
      connectionData.username = formData.username;
      connectionData.password = formData.password;
      connectionData.company_db = formData.company_db;
    }

    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/enterprise/erp/connect', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          erp_type: selectedErp,
          connection_data: connectionData,
          sync_frequency: 'daily'
        })
      });

      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          setShowAddModal(false);
          setFormData({
            api_key: '',
            company_id: '',
            base_url: '',
            username: '',
            password: '',
            server_url: '',
            company_db: ''
          });
          loadConnections();
        } else {
          alert('Failed to create connection: ' + (data.message || 'Unknown error'));
        }
      } else {
        const error = await response.json();
        alert('Error: ' + (error.detail || 'Unknown error'));
      }
    } catch (error) {
      console.error('Error creating connection:', error);
      alert('Error creating connection');
    }
  };

  const handleActivate = async (connectionId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/enterprise/erp/${connectionId}/activate`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        loadConnections();
      } else {
        const error = await response.json();
        alert('Error: ' + (error.detail || 'Failed to activate'));
      }
    } catch (error) {
      console.error('Error activating connection:', error);
      alert('Error activating connection');
    }
  };

  const handleDeactivate = async (connectionId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/enterprise/erp/${connectionId}/deactivate`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        loadConnections();
      } else {
        const error = await response.json();
        alert('Error: ' + (error.detail || 'Failed to deactivate'));
      }
    } catch (error) {
      console.error('Error deactivating connection:', error);
      alert('Error deactivating connection');
    }
  };

  const handleSync = async (connectionId) => {
    setSyncing({ ...syncing, [connectionId]: true });
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/enterprise/erp/${connectionId}/sync?sync_type=incremental`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        alert(`Sync completed! Records synced: ${data.records_synced || 0}`);
        loadConnections();
        loadSyncLogs(connectionId);
      } else {
        const error = await response.json();
        alert('Error: ' + (error.detail || 'Sync failed'));
      }
    } catch (error) {
      console.error('Error syncing:', error);
      alert('Error syncing data');
    } finally {
      setSyncing({ ...syncing, [connectionId]: false });
    }
  };

  const loadSyncLogs = async (connectionId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/enterprise/erp/${connectionId}/logs?limit=10`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setSyncLogs({ ...syncLogs, [connectionId]: data.logs || [] });
      }
    } catch (error) {
      console.error('Error loading sync logs:', error);
    }
  };

  if (user?.tier !== 'enterprise') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center p-4">
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-8 border border-white/20 max-w-md w-full text-center">
          <h1 className="text-2xl font-bold text-white mb-2">Enterprise Tier Required</h1>
          <p className="text-blue-200 mb-6">ERP integrations are only available for Enterprise tier users.</p>
          <button
            onClick={() => navigate('/payment/checkout?tier=enterprise')}
            className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg transition-colors"
          >
            Upgrade to Enterprise
          </button>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center">
        <div className="text-white text-xl">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">ERP Integrations</h1>
          <p className="text-blue-200">Connect your ERP system to enhance risk analysis</p>
        </div>

        <div className="mb-6">
          <button
            onClick={() => setShowAddModal(true)}
            className="bg-teal-600 hover:bg-teal-700 text-white px-6 py-3 rounded-lg transition-colors"
          >
            + Add ERP Connection
          </button>
        </div>

        <div className="grid gap-6">
          {connections.length === 0 ? (
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-8 border border-white/20 text-center">
              <p className="text-white text-lg mb-4">No ERP connections yet</p>
              <button
                onClick={() => setShowAddModal(true)}
                className="bg-teal-600 hover:bg-teal-700 text-white px-6 py-3 rounded-lg transition-colors"
              >
                Add Your First Connection
              </button>
            </div>
          ) : (
            connections.map((conn) => (
              <div key={conn.id} className="bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-6 border border-white/20">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-2xl font-bold text-white mb-2">
                      {conn.erp_type.toUpperCase()}
                    </h3>
                    <p className="text-blue-200">
                      Status: <span className={`font-bold ${conn.status === 'active' ? 'text-green-400' : 'text-red-400'}`}>
                        {conn.status.toUpperCase()}
                      </span>
                    </p>
                    {conn.company_name && (
                      <p className="text-blue-200">Company: {conn.company_name}</p>
                    )}
                  </div>
                  <div className="flex gap-2">
                    {conn.status === 'active' ? (
                      <>
                        <button
                          onClick={() => handleSync(conn.id)}
                          disabled={syncing[conn.id]}
                          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors disabled:opacity-50"
                        >
                          {syncing[conn.id] ? 'Syncing...' : 'Sync Now'}
                        </button>
                        <button
                          onClick={() => handleDeactivate(conn.id)}
                          className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition-colors"
                        >
                          Deactivate
                        </button>
                      </>
                    ) : (
                      <button
                        onClick={() => handleActivate(conn.id)}
                        className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-colors"
                      >
                        Activate
                      </button>
                    )}
                  </div>
                </div>

                <div className="mt-4 text-sm text-blue-200">
                  <p>Last sync: {conn.last_sync_at ? new Date(conn.last_sync_at).toLocaleString() : 'Never'}</p>
                  <p>Next sync: {conn.next_sync_at ? new Date(conn.next_sync_at).toLocaleString() : 'Not scheduled'}</p>
                  <p>Sync frequency: {conn.sync_frequency}</p>
                </div>

                {conn.status === 'active' && (
                  <button
                    onClick={() => {
                      if (!syncLogs[conn.id]) {
                        loadSyncLogs(conn.id);
                      }
                    }}
                    className="mt-4 text-blue-400 hover:text-blue-300 text-sm"
                  >
                    {syncLogs[conn.id] ? 'Hide' : 'Show'} Sync Logs
                  </button>
                )}

                {syncLogs[conn.id] && (
                  <div className="mt-4 bg-black/20 rounded-lg p-4">
                    <h4 className="text-white font-bold mb-2">Recent Sync Logs</h4>
                    {syncLogs[conn.id].length === 0 ? (
                      <p className="text-blue-200 text-sm">No sync logs yet</p>
                    ) : (
                      <div className="space-y-2">
                        {syncLogs[conn.id].slice(0, 5).map((log) => (
                          <div key={log.id} className="text-sm text-blue-200">
                            <span className={log.status === 'success' ? 'text-green-400' : 'text-red-400'}>
                              {log.status.toUpperCase()}
                            </span>
                            {' '}
                            - {log.records_synced} records synced
                            {' '}
                            - {new Date(log.started_at).toLocaleString()}
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))
          )}
        </div>

        {showAddModal && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
            <div className="bg-slate-800 rounded-2xl shadow-2xl p-8 max-w-md w-full border border-white/20">
              <h2 className="text-2xl font-bold text-white mb-4">Add ERP Connection</h2>
              
              <form onSubmit={handleAddConnection}>
                <div className="mb-4">
                  <label className="block text-white mb-2">ERP System</label>
                  <select
                    value={selectedErp}
                    onChange={(e) => setSelectedErp(e.target.value)}
                    className="w-full bg-slate-700 text-white px-4 py-2 rounded-lg"
                  >
                    <option value="pohoda">Pohoda (SK)</option>
                    <option value="money_s3">Money S3 (CZ)</option>
                    <option value="sap">SAP</option>
                  </select>
                </div>

                {selectedErp === 'pohoda' || selectedErp === 'money_s3' ? (
                  <>
                    <div className="mb-4">
                      <label className="block text-white mb-2">API Key</label>
                      <input
                        type="text"
                        value={formData.api_key}
                        onChange={(e) => setFormData({ ...formData, api_key: e.target.value })}
                        className="w-full bg-slate-700 text-white px-4 py-2 rounded-lg"
                        required
                      />
                    </div>
                    <div className="mb-4">
                      <label className="block text-white mb-2">Company ID</label>
                      <input
                        type="text"
                        value={formData.company_id}
                        onChange={(e) => setFormData({ ...formData, company_id: e.target.value })}
                        className="w-full bg-slate-700 text-white px-4 py-2 rounded-lg"
                        required
                      />
                    </div>
                    <div className="mb-4">
                      <label className="block text-white mb-2">Base URL (optional)</label>
                      <input
                        type="text"
                        value={formData.base_url}
                        onChange={(e) => setFormData({ ...formData, base_url: e.target.value })}
                        className="w-full bg-slate-700 text-white px-4 py-2 rounded-lg"
                        placeholder={selectedErp === 'pohoda' ? 'https://api.pohoda.sk' : 'https://api.moneys3.cz'}
                      />
                    </div>
                  </>
                ) : (
                  <>
                    <div className="mb-4">
                      <label className="block text-white mb-2">Server URL</label>
                      <input
                        type="text"
                        value={formData.server_url}
                        onChange={(e) => setFormData({ ...formData, server_url: e.target.value })}
                        className="w-full bg-slate-700 text-white px-4 py-2 rounded-lg"
                        required
                      />
                    </div>
                    <div className="mb-4">
                      <label className="block text-white mb-2">Username</label>
                      <input
                        type="text"
                        value={formData.username}
                        onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                        className="w-full bg-slate-700 text-white px-4 py-2 rounded-lg"
                        required
                      />
                    </div>
                    <div className="mb-4">
                      <label className="block text-white mb-2">Password</label>
                      <input
                        type="password"
                        value={formData.password}
                        onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                        className="w-full bg-slate-700 text-white px-4 py-2 rounded-lg"
                        required
                      />
                    </div>
                    <div className="mb-4">
                      <label className="block text-white mb-2">Company DB</label>
                      <input
                        type="text"
                        value={formData.company_db}
                        onChange={(e) => setFormData({ ...formData, company_db: e.target.value })}
                        className="w-full bg-slate-700 text-white px-4 py-2 rounded-lg"
                        required
                      />
                    </div>
                  </>
                )}

                <div className="flex gap-4">
                  <button
                    type="submit"
                    className="flex-1 bg-teal-600 hover:bg-teal-700 text-white px-6 py-3 rounded-lg transition-colors"
                  >
                    Connect
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowAddModal(false)}
                    className="flex-1 bg-slate-600 hover:bg-slate-700 text-white px-6 py-3 rounded-lg transition-colors"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ErpIntegrations;

