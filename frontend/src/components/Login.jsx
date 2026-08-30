import React, { useState } from 'react';
import { login, registerAccount } from '../services/api';
import { ShieldAlert, KeyRound, Loader2, UserPlus } from 'lucide-react';

const inputClass = 'w-full bg-slate-800/50 border border-slate-600 rounded-lg px-4 py-2.5 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all';

export default function Login({ onLogin }) {
  const [isCreatingAccount, setIsCreatingAccount] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [account, setAccount] = useState({ full_name: '', email: '', state: '', district: '', role: 'citizen' });
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const switchMode = () => {
    setIsCreatingAccount((current) => !current);
    setError(null);
    setPassword('');
    setConfirmPassword('');
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null);

    if (isCreatingAccount && password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    setLoading(true);
    try {
      const user = isCreatingAccount
        ? await registerAccount({ ...account, username, password })
        : await login(username, password);
      onLogin(user);
    } catch (err) {
      setError(err.message || (isCreatingAccount ? 'Unable to create your account.' : 'Login failed. Please check your credentials.'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center p-4 relative overflow-auto">
      <div className="absolute top-[-10%] left-[-10%] w-96 h-96 bg-blue-600/20 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[30rem] h-[30rem] bg-indigo-600/10 rounded-full blur-3xl pointer-events-none" />

      <div className="w-full max-w-md bg-slate-900/60 backdrop-blur-xl border border-slate-700/50 p-8 rounded-2xl shadow-2xl relative z-10 my-6">
        <div className="flex flex-col items-center mb-8">
          <div className="w-16 h-16 bg-blue-500/20 rounded-2xl flex items-center justify-center mb-4 border border-blue-500/30">
            <ShieldAlert className="w-8 h-8 text-blue-400" />
          </div>
          <h1 className="text-3xl font-bold text-white tracking-tight mb-2">TerrainTrace</h1>
          <p className="text-slate-400 text-center text-sm">
            {isCreatingAccount ? 'Create your monitoring account' : 'AI-Powered Landslide Early Warning & GIS Monitoring Platform'}
          </p>
        </div>

        {error && (
          <div className="bg-red-500/10 border border-red-500/30 text-red-400 p-3 rounded-lg mb-6 text-sm flex items-start gap-2" role="alert">
            <ShieldAlert className="w-4 h-4 mt-0.5 shrink-0" />
            <p>{error}</p>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {isCreatingAccount && (
            <>
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1" htmlFor="full-name">Full name</label>
                <input id="full-name" type="text" value={account.full_name} onChange={(e) => setAccount({ ...account, full_name: e.target.value })} className={inputClass} placeholder="Your full name" required />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1" htmlFor="email">Email address</label>
                <input id="email" type="email" value={account.email} onChange={(e) => setAccount({ ...account, email: e.target.value })} className={inputClass} placeholder="you@example.com" required />
              </div>
            </>
          )}

          <div>
            <label className="block text-sm font-medium text-slate-300 mb-1" htmlFor="username">Username</label>
            <input id="username" type="text" value={username} onChange={(e) => setUsername(e.target.value)} className={inputClass} placeholder="Choose a username" autoComplete="username" required />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-300 mb-1" htmlFor="password">Password</label>
            <input id="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} className={inputClass} placeholder="Enter your password" autoComplete={isCreatingAccount ? 'new-password' : 'current-password'} minLength={isCreatingAccount ? 8 : undefined} required />
          </div>

          {isCreatingAccount && (
            <>
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1" htmlFor="confirm-password">Confirm password</label>
                <input id="confirm-password" type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} className={inputClass} placeholder="Re-enter your password" autoComplete="new-password" minLength="8" required />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1" htmlFor="state">State</label>
                  <input id="state" type="text" value={account.state} onChange={(e) => setAccount({ ...account, state: e.target.value })} className={inputClass} placeholder="e.g. Meghalaya" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1" htmlFor="district">District</label>
                  <input id="district" type="text" value={account.district} onChange={(e) => setAccount({ ...account, district: e.target.value })} className={inputClass} placeholder="Optional" />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1" htmlFor="role">Account type</label>
                <select id="role" value={account.role} onChange={(e) => setAccount({ ...account, role: e.target.value })} className={inputClass}>
                  <option value="citizen">Citizen</option>
                  <option value="field_officer">Field officer</option>
                </select>
              </div>
            </>
          )}

          <button type="submit" disabled={loading} className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5 rounded-lg transition-colors flex items-center justify-center gap-2 mt-6 disabled:opacity-50 disabled:cursor-not-allowed">
            {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : isCreatingAccount ? <UserPlus className="w-5 h-5" /> : <KeyRound className="w-5 h-5" />}
            {loading ? (isCreatingAccount ? 'Creating account...' : 'Authenticating...') : (isCreatingAccount ? 'Create account' : 'Sign in')}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-slate-400">
          {isCreatingAccount ? 'Already have an account?' : 'New to TerraintTrace?'}{' '}
          <button type="button" onClick={switchMode} className="font-semibold text-blue-400 hover:text-blue-300 focus:outline-none focus:underline">
            {isCreatingAccount ? 'Sign in' : 'Create an account'}
          </button>
        </p>

        {!isCreatingAccount && (
          <div className="mt-6 pt-6 border-t border-slate-700/50">
            <div className="bg-slate-800/50 rounded-lg p-3 text-xs text-slate-400">
              <p className="font-semibold text-slate-300 mb-1">Demo credentials:</p>
              <p>Admin: <span className="font-mono text-blue-300">admin / admin123</span></p>
              <p>Officer: <span className="font-mono text-blue-300">officer / officer123</span></p>
              <p>Field staff: <span className="font-mono text-blue-300">field1 / field123</span></p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
