import React, { useState, useEffect } from 'react';
import { 
  ShieldAlert, 
  Wifi, 
  WifiOff, 
  RefreshCw, 
  Globe, 
  Volume2, 
  VolumeX, 
  Layers, 
  Activity, 
  Radio, 
  Truck, 
  FileText, 
  Bell
} from 'lucide-react';
import { LANGUAGES, TRANSLATIONS } from '../services/i18n';
import { OfflineVault, syncPendingOfflineReports } from '../services/api';

export default function Navbar({ 
  currentTab, 
  setCurrentTab, 
  currentLang, 
  setCurrentLang, 
  alerts = [],
  overview = null
}) {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [pendingCount, setPendingCount] = useState(0);
  const [syncing, setSyncing] = useState(false);
  const [soundEnabled, setSoundEnabled] = useState(true);

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
    <header className="sticky top-0 z-50 bg-slate-900/95 backdrop-blur-md border-b border-slate-800 shadow-xl">
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
            onClick={() => setCurrentTab('alerts')}
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
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => setCurrentTab('map')}>
            <div className="h-11 w-11 rounded-xl bg-gradient-to-br from-amber-500 via-orange-600 to-red-600 flex items-center justify-center shadow-lg shadow-orange-500/20 border border-orange-400/30">
              <ShieldAlert className="h-6 w-6 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xl font-black tracking-tight text-white bg-clip-text">
                  BhooDrishti<span className="text-amber-400">-NER</span>
                </span>
                <span className="hidden md:inline-block px-1.5 py-0.5 text-[10px] uppercase font-bold tracking-wider rounded bg-amber-500/10 text-amber-300 border border-amber-500/20">
                  भू-दृष्टि AI
                </span>
              </div>
              <p className="text-[11px] text-slate-400 font-medium hidden sm:block">
                {t.app_subtitle}
              </p>
            </div>
          </div>

          {/* Navigation Tabs */}
          <nav className="hidden lg:flex items-center gap-1 bg-slate-950/60 p-1.5 rounded-xl border border-slate-800">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = currentTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setCurrentTab(item.id)}
                  className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all duration-200 relative ${
                    isActive
                      ? 'bg-gradient-to-r from-amber-500 to-orange-600 text-white shadow-md shadow-orange-500/20 font-bold'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                  }`}
                >
                  <Icon className={`h-4 w-4 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                  <span>{item.label}</span>
                  {item.badge > 0 && (
                    <span className="ml-1 px-1.5 py-0.2 bg-red-500 text-white text-[10px] rounded-full font-bold">
                      {item.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>

          {/* Right utility actions */}
          <div className="flex items-center gap-2.5">
            {/* Language Selector */}
            <div className="relative flex items-center bg-slate-800/80 border border-slate-700 rounded-lg px-2.5 py-1 text-xs text-slate-200">
              <Globe className="h-3.5 w-3.5 text-amber-400 mr-1.5" />
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
            <div className="flex items-center gap-1.5">
              {isOnline ? (
                <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-emerald-950/60 border border-emerald-800/50 text-emerald-400 text-xs font-medium">
                  <Wifi className="h-3.5 w-3.5" />
                  <span className="hidden sm:inline">{t.online_synced}</span>
                </div>
              ) : (
                <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-rose-950/70 border border-rose-800/60 text-rose-300 text-xs font-medium animate-pulse">
                  <WifiOff className="h-3.5 w-3.5" />
                  <span>{t.offline_mode}</span>
                </div>
              )}

              {/* Pending Offline Reports Sync Button */}
              {pendingCount > 0 && (
                <button
                  onClick={handleSync}
                  disabled={!isOnline || syncing}
                  className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-amber-500 hover:bg-amber-600 disabled:opacity-50 text-slate-950 text-xs font-bold transition-all shadow-md"
                  title="Upload reports recorded while offline in remote mountain areas"
                >
                  <RefreshCw className={`h-3 w-3 ${syncing ? 'animate-spin' : ''}`} />
                  <span>Sync ({pendingCount})</span>
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Mobile Sub-Navigation */}
        <div className="lg:hidden flex items-center justify-between overflow-x-auto py-2 border-t border-slate-800/80 gap-1 text-xs">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setCurrentTab(item.id)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg whitespace-nowrap font-medium ${
                  isActive
                    ? 'bg-orange-500 text-white font-bold'
                    : 'text-slate-400 hover:text-slate-200'
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

