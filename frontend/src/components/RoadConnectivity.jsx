import React, { useState } from 'react';
import { 
  Truck, 
  AlertTriangle, 
  Clock, 
  MapPin, 
  Navigation, 
  CheckCircle, 
  Wrench, 
  ShieldAlert, 
  Compass, 
  ChevronRight, 
  RefreshCw 
} from 'lucide-react';
import { updateRoadStatus } from '../services/api';
import { TRANSLATIONS } from '../services/i18n';

export default function RoadConnectivity({ 
  roads = [], 
  onRefresh = () => {},
  currentLang = 'en' 
}) {
  const t = TRANSLATIONS[currentLang] || TRANSLATIONS.en;

  const [selectedRoad, setSelectedRoad] = useState(roads[0] || null);
  const [updating, setUpdating] = useState(false);
  const [newStatus, setNewStatus] = useState('PARTIALLY_BLOCKED');
  const [etaHours, setEtaHours] = useState(4.0);
  const [remarks, setRemarks] = useState('');
  const [updateMessage, setUpdateMessage] = useState(null);

  const activeRoad = selectedRoad || roads[0];

  const handleUpdateStatus = async (e) => {
    e.preventDefault();
    if (!activeRoad) return;
    setUpdating(true);
    setUpdateMessage(null);
    try {
      await updateRoadStatus(activeRoad.corridor_id, newStatus, etaHours, remarks);
      setUpdateMessage('Road status updated successfully! Broadcast synced with GIS.');
      onRefresh();
    } catch (err) {
      console.error(err);
      setUpdateMessage('Failed to update road status.');
    } finally {
      setUpdating(false);
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'FULLY_BLOCKED':
        return <span className="px-2.5 py-1 text-xs font-bold rounded bg-red-600 text-white animate-pulse">FULLY BLOCKED</span>;
      case 'PARTIALLY_BLOCKED':
        return <span className="px-2.5 py-1 text-xs font-bold rounded bg-orange-600 text-white">PARTIALLY BLOCKED</span>;
      case 'HIGH_RISK_ADVISORY':
        return <span className="px-2.5 py-1 text-xs font-bold rounded bg-amber-500 text-slate-950 font-bold">HIGH RISK ADVISORY</span>;
      default:
        return <span className="px-2.5 py-1 text-xs font-bold rounded bg-emerald-600 text-white">OPERATIONAL</span>;
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-6 space-y-6">
      {/* Header */}
      <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-amber-400 text-xs font-bold uppercase tracking-widest mb-1">
            <Truck className="h-4 w-4" />
            North Eastern Strategic Highway Connectivity Matrix
          </div>
          <h1 className="text-2xl font-black text-white">
            Highway Corridor Status & Emergency Detour Routing
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Real-time monitoring of NH-10, NH-29, NH-06, NH-102, NH-13, NH-54, and NH-27 corridors with multi-agency clearance response.
          </p>
        </div>

        <button
          onClick={onRefresh}
          className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold rounded-xl border border-slate-700 transition-all self-start md:self-auto"
        >
          <RefreshCw className="h-4 w-4 text-amber-400" />
          Refresh Corridors
        </button>
      </div>

      {/* Grid of Highway Cards + Detail/Update Section */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left 5 Columns: Highway Corridor List */}
        <div className="lg:col-span-5 space-y-3">
          <div className="text-xs font-bold text-slate-400 uppercase tracking-wider px-1">
            Monitored Lifeline Corridors ({roads.length})
          </div>
          <div className="space-y-2.5 max-h-[calc(100vh-18rem)] overflow-y-auto pr-1">
            {roads.map((road) => {
              const isSelected = activeRoad?.corridor_id === road.corridor_id;
              return (
                <div
                  key={road.corridor_id}
                  onClick={() => setSelectedRoad(road)}
                  className={`p-4 rounded-xl border cursor-pointer transition-all ${
                    isSelected
                      ? 'bg-slate-800 border-amber-500/80 shadow-lg shadow-amber-500/10'
                      : 'bg-slate-900/80 border-slate-800 hover:bg-slate-800/60'
                  }`}
                >
                  <div className="flex items-center justify-between gap-2 mb-1.5">
                    <span className="font-bold text-sm text-white">{road.highway_name}</span>
                    {getStatusBadge(road.status)}
                  </div>
                  <p className="text-xs text-slate-300 font-medium mb-2">{road.stretch_name}</p>
                  
                  <div className="flex items-center justify-between text-xs text-slate-400 pt-2 border-t border-slate-800">
                    <div className="flex items-center gap-1">
                      <span className="text-slate-500">{road.state}</span>
                    </div>
                    {road.stranded_vehicles_estimate > 0 && (
                      <div className="text-rose-400 font-semibold">
                        {road.stranded_vehicles_estimate} {t.stranded_vehicles}
                      </div>
                    )}
                    <div className="text-amber-400 font-bold">
                      Priority: {road.response_priority_score || road.calculated_priority_score}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right 7 Columns: Selected Corridor Details, Detour Map, & Clearing Controls */}
        <div className="lg:col-span-7 space-y-6">
          {activeRoad ? (
            <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl shadow-xl space-y-6">
              {/* Top Banner */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-4">
                <div>
                  <div className="flex items-center gap-2">
                    <h2 className="text-xl font-bold text-white">{activeRoad.highway_name}</h2>
                    {getStatusBadge(activeRoad.status)}
                  </div>
                  <p className="text-xs text-slate-400 mt-0.5">{activeRoad.stretch_name} ({activeRoad.state})</p>
                </div>
                <div className="bg-slate-950 px-3 py-1.5 rounded-xl border border-slate-800 text-right">
                  <div className="text-[10px] text-slate-400 font-bold uppercase">Response Priority Score</div>
                  <div className="text-lg font-black text-amber-400">
                    {activeRoad.response_priority_score || activeRoad.calculated_priority_score} / 100
                  </div>
                </div>
              </div>

              {/* Blockage Cause & Metrics */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
                <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                  <div className="text-[10px] text-slate-400 font-bold uppercase">{t.clearance_eta}</div>
                  <div className="text-base font-bold text-cyan-400 mt-1 flex items-center gap-1.5">
                    <Clock className="h-4 w-4" />
                    {activeRoad.clearing_eta_hours > 0 ? `${activeRoad.clearing_eta_hours} Hours` : 'Clear'}
                  </div>
                </div>

                <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                  <div className="text-[10px] text-slate-400 font-bold uppercase">{t.stranded_vehicles}</div>
                  <div className="text-base font-bold text-rose-400 mt-1 flex items-center gap-1.5">
                    <Truck className="h-4 w-4" />
                    {activeRoad.stranded_vehicles_estimate}
                  </div>
                </div>

                <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                  <div className="text-[10px] text-slate-400 font-bold uppercase">Corridor Risk Level</div>
                  <div className="text-base font-bold text-amber-400 mt-1 flex items-center gap-1.5">
                    <ShieldAlert className="h-4 w-4" />
                    {activeRoad.risk_level}
                  </div>
                </div>
              </div>

              {/* Specific Blockage Cause Remarks */}
              {activeRoad.blockage_cause && (
                <div className="bg-rose-950/30 border border-rose-800/40 p-4 rounded-xl text-xs space-y-1">
                  <span className="font-bold text-rose-300 flex items-center gap-1.5">
                    <AlertTriangle className="h-4 w-4 text-rose-400" />
                    Field Incident Intelligence:
                  </span>
                  <p className="text-slate-200 pl-5 leading-relaxed">{activeRoad.blockage_cause}</p>
                </div>
              )}

              {/* Alternate Detour Route Card */}
              {activeRoad.alternate_route && (
                <div className="bg-amber-950/20 border border-amber-800/40 p-4 rounded-xl text-xs space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-amber-300 flex items-center gap-1.5">
                      <Navigation className="h-4 w-4 text-amber-400" />
                      {t.alternate_route} Guidance:
                    </span>
                    <span className="text-[11px] font-bold text-amber-400 bg-amber-500/20 px-2 py-0.5 rounded">
                      +{activeRoad.alternate_route_extra_km} km / +{activeRoad.alternate_route_extra_hours} hrs
                    </span>
                  </div>
                  <p className="text-slate-200 pl-5 leading-relaxed">{activeRoad.alternate_route}</p>
                </div>
              )}

              {/* Status Update Form for Authorized Engineers & Field Marshals */}
              <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-4">
                <div className="font-bold text-xs text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                  <Wrench className="h-4 w-4 text-amber-400" />
                  Field Marshal / BRO Corridor Status Dispatch
                </div>

                {updateMessage && (
                  <div className="p-2.5 rounded bg-emerald-950/60 border border-emerald-800 text-emerald-300 text-xs font-semibold">
                    {updateMessage}
                  </div>
                )}

                <form onSubmit={handleUpdateStatus} className="space-y-3 text-xs">
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    <div>
                      <label className="text-slate-400 font-semibold mb-1 block">New Operational Status:</label>
                      <select
                        value={newStatus}
                        onChange={(e) => setNewStatus(e.target.value)}
                        className="w-full bg-slate-900 border border-slate-700 text-white rounded-lg p-2 font-medium"
                      >
                        <option value="CLEAR">CLEAR / OPERATIONAL</option>
                        <option value="HIGH_RISK_ADVISORY">HIGH RISK ADVISORY</option>
                        <option value="PARTIALLY_BLOCKED">PARTIALLY BLOCKED (Single Lane)</option>
                        <option value="FULLY_BLOCKED">FULLY BLOCKED (Impassable)</option>
                      </select>
                    </div>

                    <div>
                      <label className="text-slate-400 font-semibold mb-1 block">Clearing ETA (Hours):</label>
                      <input
                        type="number"
                        step="0.5"
                        min="0"
                        max="48"
                        value={etaHours}
                        onChange={(e) => setEtaHours(e.target.value)}
                        className="w-full bg-slate-900 border border-slate-700 text-white rounded-lg p-2 font-medium"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="text-slate-400 font-semibold mb-1 block">Field Remarks / Clearance Machinery Notes:</label>
                    <input
                      type="text"
                      placeholder="e.g. 2 heavy excavators deployed near mile marker 29, clearing lower bench..."
                      value={remarks}
                      onChange={(e) => setRemarks(e.target.value)}
                      className="w-full bg-slate-900 border border-slate-700 text-white rounded-lg p-2 font-medium"
                    />
                  </div>

                  <button
                    type="submit"
                    disabled={updating}
                    className="w-full py-2.5 bg-gradient-to-r from-amber-500 to-orange-600 hover:brightness-110 disabled:opacity-50 text-slate-950 font-bold text-xs rounded-xl shadow-lg transition-all"
                  >
                    {updating ? 'Transmitting to Central Command...' : 'Update & Broadcast Status to GIS'}
                  </button>
                </form>
              </div>
            </div>
          ) : (
            <div className="p-8 text-center text-slate-500">Select a corridor to view detailed logistics.</div>
          )}
        </div>
      </div>
    </div>
  );
}

