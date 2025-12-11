import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Send, Eye, EyeOff, Plus, ArrowUpRight, ArrowDownLeft } from 'lucide-react';
import toast from 'react-hot-toast';

export default function Dashboard() {
  const { user, api, logout } = useAuth();
  const [wallets, setWallets] = useState([]);
  const [balance, setBalance] = useState(0);
  const [transfer, setTransfer] = useState({ user_id: '', amount: 0, currency: 'BTC' });
  const [showBalance, setShowBalance] = useState(false);
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    fetchWallets();
    fetchLogs();
  }, []);

  const fetchWallets = async () => {
    try {
      const res = await api.get('/users/me/wallets');
      setWallets(res.data);
      const total = res.data.reduce((sum, w) => sum + w.balance, 0);
      setBalance(total);
    } catch (err) {
      console.error('Failed to fetch wallets:', err);
    }
  };

  const fetchLogs = async () => {
    try {
      const res = await api.get('/ai/logs');
      setLogs(res.data || []);
    } catch (err) {
      console.error('Failed to fetch logs:', err);
    }
  };

  const handleTransfer = async (e) => {
    e.preventDefault();
    try {
      await api.post('/wallets/transfer', transfer);
      toast.success('Transfer sent!');
      setTransfer({ user_id: '', amount: 0, currency: 'BTC' });
      fetchWallets();
      addLog(`Transferred ${transfer.amount} ${transfer.currency} to user ${transfer.user_id}`);
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Transfer failed');
    }
  };

  const addLog = (message) => {
    setLogs([{ timestamp: new Date().toISOString(), message }, ...logs]);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-black rounded-lg flex items-center justify-center">
              <span className="text-white font-bold">AI</span>
            </div>
            <h1 className="text-2xl font-bold text-black">Dashboard</h1>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-700">{user?.email}</span>
            <button onClick={logout} className="text-gray-600 hover:text-black text-sm font-medium">
              Sign out
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Balance Card */}
        <div className="bg-black text-white rounded-lg p-8 mb-8">
          <p className="text-gray-400 text-sm mb-2">Total Balance</p>
          <div className="flex items-center justify-between">
            <div>
              <div className="flex items-center gap-3">
                <span className="text-5xl font-bold">
                  {showBalance ? balance.toFixed(4) : '••••'}
                </span>
                <button onClick={() => setShowBalance(!showBalance)}>
                  {showBalance ? <EyeOff size={24} /> : <Eye size={24} />}
                </button>
              </div>
              <p className="text-gray-400 mt-2">USD equivalent shown in dashboard</p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Transfer Section */}
          <div className="lg:col-span-1 bg-white rounded-lg p-6 border border-gray-200">
            <h2 className="text-xl font-bold mb-4">Send Funds</h2>
            <form onSubmit={handleTransfer} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-900 mb-2">Recipient User ID</label>
                <input
                  type="text"
                  value={transfer.user_id}
                  onChange={(e) => setTransfer({ ...transfer, user_id: e.target.value })}
                  placeholder="user123"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-900 mb-2">Amount</label>
                <input
                  type="number"
                  value={transfer.amount}
                  onChange={(e) => setTransfer({ ...transfer, amount: parseFloat(e.target.value) })}
                  placeholder="0.5"
                  step="0.001"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-900 mb-2">Currency</label>
                <select
                  value={transfer.currency}
                  onChange={(e) => setTransfer({ ...transfer, currency: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black"
                >
                  <option>BTC</option>
                  <option>ETH</option>
                  <option>USDT</option>
                  <option>USD</option>
                </select>
              </div>
              <button
                type="submit"
                className="w-full bg-black text-white py-2 rounded-lg font-medium hover:bg-gray-800 transition flex items-center justify-center gap-2"
              >
                <Send size={18} /> Send
              </button>
            </form>
          </div>

          {/* Wallets & Logs */}
          <div className="lg:col-span-2 space-y-6">
            {/* Wallets */}
            <div className="bg-white rounded-lg p-6 border border-gray-200">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-bold">Wallets</h2>
                <button className="text-blue-600 hover:text-blue-700 flex items-center gap-1">
                  <Plus size={18} /> Add
                </button>
              </div>
              <div className="space-y-3">
                {wallets.length > 0 ? (
                  wallets.map((wallet) => (
                    <div key={wallet.id} className="flex justify-between p-3 bg-gray-50 rounded-lg border border-gray-200">
                      <div>
                        <p className="font-medium text-black">{wallet.currency}</p>
                        <p className="text-sm text-gray-500">{wallet.address.slice(0, 10)}...</p>
                      </div>
                      <p className="font-bold">{wallet.balance} {wallet.currency}</p>
                    </div>
                  ))
                ) : (
                  <p className="text-gray-500 text-sm">No wallets yet. Add one to get started.</p>
                )}
              </div>
            </div>

            {/* AI Logs / Eye */}
            <div className="bg-white rounded-lg p-6 border border-gray-200">
              <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                <div className="w-3 h-3 bg-blue-500 rounded-full animate-pulse"></div>
                AI Eye (Activity Logs)
              </h2>
              <div className="space-y-2 max-h-64 overflow-y-auto">
                {logs.length > 0 ? (
                  logs.map((log, idx) => (
                    <div key={idx} className="text-sm p-2 bg-gray-50 rounded border-l-2 border-blue-500">
                      <p className="text-gray-700">{log.message}</p>
                      <p className="text-xs text-gray-500">{new Date(log.timestamp).toLocaleTimeString()}</p>
                    </div>
                  ))
                ) : (
                  <p className="text-gray-500 text-sm">No activity yet</p>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
