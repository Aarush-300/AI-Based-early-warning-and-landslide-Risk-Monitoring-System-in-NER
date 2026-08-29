import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { setActiveModule } from '../store/navigationSlice';
import { 
  Wifi, 
  WifiOff, 
  RefreshCw, 
  Globe, 
  Layers, 
  Activity, 
  Radio, 
  Truck, 
  FileText, 
  Bell,
  Mountain,
  ArrowUpCircle
} from 'lucide-react';
import { LANGUAGES, TRANSLATIONS } from '../services/i18n';
import { OfflineVault, syncPendingOfflineReports } from '../services/api';

export default function Navbar({ 
  currentLang, 
  setCurrentLang, 
  alerts = [],
  overview = null,
  onLogout,
  user
}) {
  const dispatch = useDispatch();
  const currentTab = useSelector((state) => state.navigation.activeModule);

  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [pendingCount, setPendingCount] = useState(0);
  const [syncing, setSyncing] = useState(false);

  const t = TRANSLATIONS[currentLang] || TRANSLATIONS.en;

  const checkPending = async () => {
    try {
      const list = await OfflineVault.getAllPendingReports();
      setPendingCount(list.length);
    } catch (e) {
      console.warn(e);
    }
  };

  useEffect(() => {
    const handleOnline = () => {
      setIsOnline(true);
      handleSync();
    };
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    checkPending();
    const interval = setInterval(checkPending, 5000);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
      clearInterval(interval);
    };
  }, []);

  const handleSync = async () => {
    if (pendingCount === 0 || syncing) return;
    setSyncing(true);
    try {
      await syncPendingOfflineReports();
      await checkPending();
    } catch (err) {
      console.error('Sync error:', err);
    } finally {
      setSyncing(false);
    }
  };

  const navItems = [
    { id: 'map', label: t.nav_map, icon: Layers },
    { id: 'analytics', label: t.nav_analytics, icon: Activity },
    { id: 'roads', label: t.nav_roads, icon: Truck },
    { id: 'sensors', label: t.nav_sensors, icon: Radio },
    { id: 'reports', label: t.nav_reports, icon: FileText },
    { id: 'alerts', label: t.nav_alerts, icon: Bell, badge: alerts.length }
  ];

  const activeRedAlert = alerts.find(a => a.severity === 'EMERGENCY') || alerts[0];

  return (
    <header className="sticky top-0 z-50 bg-slate-900/80 backdrop-blur-xl border-b border-slate-800 shadow-xl transition-all duration-300">
      {/* Top emergency broadcast ticker */}
      {activeRedAlert && (
        <div className="bg-gradient-to-r from-red-700 via-rose-600 to-red-800 text-white text-xs px-4 py-1.5 flex items-center justify-between font-semibold shadow-inner">
          <div className="flex items-center gap-2 overflow-hidden whitespace-nowrap">
            <span className="flex h-2 w-2 relative">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-white opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-white"></span>
            </span>
            <span className="bg-black/30 uppercase tracking-wider px-2 py-0.5 rounded text-[10px] font-bold">
              EARLY WARNING
            </span>
            <span className="truncate">
              {activeRedAlert.translations?.[currentLang]?.title || activeRedAlert.title}
            </span>
          </div>
          <button 
            onClick={() => dispatch(setActiveModule('alerts'))}
            className="ml-4 underline hover:text-red-100 text-[11px] whitespace-nowrap"
          >
            View CAP Directive &rarr;
          </button>
        </div>
      )}

      {/* Main Navbar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Branding */}
          <div className="flex items-center gap-3 cursor-pointer group" onClick={() => dispatch(setActiveModule('map'))}>
            <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-indigo-500 to-blue-600 flex items-center justify-center shadow-lg shadow-blue-500/30 border border-blue-400/20 group-hover:scale-105 transition-transform duration-300">
              <Mountain className="h-5 w-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xl font-black tracking-tight text-white bg-clip-text">
                  Terraint<span className="text-blue-400">Trace</span>
                </span>
              </div>
            </div>
          </div>

          {/* Navigation Tabs */}
          <nav className="hidden lg:flex items-center gap-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = currentTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => dispatch(setActiveModule(item.id))}
                  className={`flex items-center gap-2 px-4 py-2 rounded-xl text-[13px] transition-all duration-300 relative font-semibold ${
                    isActive
                      ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-[0_0_15px_rgba(79,70,229,0.5)] border border-blue-400/30'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50 hover:shadow-lg'
                  }`}
                >
                  <Icon className={`h-4 w-4 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                  <span>{item.label}</span>
                  {item.badge > 0 && (
                    <span className="ml-1 px-1.5 py-0.5 bg-red-500 text-white text-[10px] rounded-full font-bold shadow-sm">
                      {item.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>

          {/* Right utility actions */}
          <div className="flex items-center gap-3">
            {/* Language Selector */}
            <div className="relative flex items-center bg-slate-800/50 border border-slate-700/80 rounded-full px-3 py-1.5 text-xs text-slate-200 hover:bg-slate-800 transition-colors">
              <Globe className="h-3.5 w-3.5 text-blue-400 mr-2" />
              <select
                value={currentLang}
                onChange={(e) => setCurrentLang(e.target.value)}
                aria-label="Select Language"
                className="bg-transparent border-none text-slate-200 text-xs font-medium focus:outline-none cursor-pointer pr-1"
              >
                {LANGUAGES.map((lang) => (
                  <option key={lang.code} value={lang.code} className="bg-slate-900 text-slate-100">
                    {lang.native} ({lang.name})
                  </option>
                ))}
              </select>
            </div>

            {/* Offline/Online Sync Badge */}
            <div className="flex items-center gap-2">
              {isOnline ? (
                <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-800/50 border border-slate-700/50 text-emerald-400 text-xs font-medium shadow-sm">
                  <span className="relative flex h-2 w-2">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                  </span>
                  <span className="hidden sm:inline">Cloud Synced</span>
                </div>
              ) : (
                <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-rose-950/40 border border-rose-800/30 text-rose-400 text-xs font-medium animate-pulse">
                  <WifiOff className="h-3.5 w-3.5" />
                  <span>{t.offline_mode}</span>
                </div>
              )}

              {/* Pending Offline Reports Sync Button */}
              {pendingCount > 0 && (
                <button
                  onClick={handleSync}
                  disabled={!isOnline || syncing}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-indigo-500 hover:bg-indigo-600 disabled:opacity-50 text-white text-xs font-bold transition-all shadow-[0_0_10px_rgba(99,102,241,0.4)]"
                  title="Upload reports recorded while offline"
                >
                  <RefreshCw className={`h-3 w-3 ${syncing ? 'animate-spin' : ''}`} />
                  <span>Sync ({pendingCount})</span>
                </button>
              )}
            </div>

            {/* User Profile / Logout */}
            {user && (
              <div className="flex items-center gap-3 pl-3 border-l border-slate-700/50">
                <div className="hidden sm:block text-right">
                  <div className="text-xs font-bold text-slate-200">{user.username || 'Admin'}</div>
                  <div className="text-[10px] text-slate-400 uppercase tracking-wider">{user.role || 'Officer'}</div>
                </div>
                <button
                  onClick={onLogout}
                  className="p-1.5 rounded-lg bg-slate-800/50 hover:bg-red-500/20 text-slate-400 hover:text-red-400 transition-colors border border-transparent hover:border-red-500/30"
                  title="Logout"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                  </svg>
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Mobile Sub-Navigation */}
        <div className="lg:hidden flex items-center justify-between overflow-x-auto py-2 border-t border-slate-800/50 gap-2 text-xs scrollbar-hide">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => dispatch(setActiveModule(item.id))}
                className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl whitespace-nowrap font-medium transition-all ${
                  isActive
                    ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/20'
                    : 'text-slate-400 hover:text-slate-200 bg-slate-800/30'
                }`}
              >
                <Icon className="h-3.5 w-3.5" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </div>
      </div>
    </header>
  );
}
