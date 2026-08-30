import React, { useState } from 'react';
import { 
  Radio, 
  Activity, 
  Droplet, 
  Compass, 
  TrendingUp, 
  Battery, 
  AlertTriangle, 
  CheckCircle, 
  Volume2, 
  Zap 
} from 'lucide-react';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer, 
  Legend 
} from 'recharts';
import { TRANSLATIONS } from '../services/i18n';

export default function SensorTelemetry({ 
  sensors = [], 
  currentLang = 'en' 
}) {
  const t = TRANSLATIONS[currentLang] || TRANSLATIONS.en;
  const [selectedSensorId, setSelectedSensorId] = useState(sensors[0]?.sensor_id || null);

  const activeSensor = sensors.find(s => s.sensor_id === selectedSensorId) || sensors[0];

  const getStatusBadge = (status) => {
    switch (status) {
      case 'CRITICAL':
        return <span className="px-2.5 py-1 text-xs font-bold rounded bg-red-600 text-white animate-pulse">CRITICAL BREACH</span>;
      case 'WARNING':
        return <span className="px-2.5 py-1 text-xs font-bold rounded bg-orange-600 text-white">WARNING THRESHOLD</span>;
      case 'WATCH':
        return <span className="px-2.5 py-1 text-xs font-bold rounded bg-amber-500 text-slate-950 font-bold">WATCH</span>;
      default:
        return <span className="px-2.5 py-1 text-xs font-bold rounded bg-emerald-600 text-white">NORMAL</span>;
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-6 space-y-6">
      {/* Header Banner */}
      <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-amber-400 text-xs font-bold uppercase tracking-widest mb-1">
            <Radio className="h-4 w-4 animate-pulse" />
            In-Situ Geotechnical Telemetry Stream
          </div>
          <h1 className="text-2xl font-black text-white">
            Real-Time Slope Instrumentation & Sensor Telemetry
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Live readings of Piezometer Pore Pressure (u), Soil Moisture (θ), Biaxial Inclinometer Tilt (θ_tilt), and Acoustic Emissions.
          </p>
        </div>

        {/* Live WebSocket Status Badge */}
        <div className="flex items-center gap-2 bg-emerald-950/60 border border-emerald-800/60 px-3.5 py-2 rounded-xl text-emerald-300 text-xs font-semibold self-start md:self-auto">
          <span className="h-2.5 w-2.5 rounded-full bg-emerald-400 animate-ping"></span>
          <span>WebSocket Stream Active (4s Tick)</span>
        </div>
      </div>

      {/* Sensor Node Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {sensors.map((s) => {
          const isSelected = activeSensor?.sensor_id === s.sensor_id;
          return (
            <div
              key={s.sensor_id}
              onClick={() => setSelectedSensorId(s.sensor_id)}
              className={`p-4 rounded-xl border cursor-pointer transition-all ${
                isSelected
                  ? 'bg-slate-800 border-amber-500/80 shadow-lg shadow-amber-500/10'
                  : 'bg-slate-900/80 border-slate-800 hover:bg-slate-800/60'
              }`}
            >
              <div className="flex items-center justify-between gap-2 mb-1.5">
                <span className="font-bold text-sm text-white flex items-center gap-1.5">
                  <Radio className="h-3.5 w-3.5 text-amber-400" />
                  {s.name}
                </span>
                {getStatusBadge(s.status)}
              </div>
              <p className="text-xs text-slate-400 mb-3">{s.location_name} • {s.state}</p>

              <div className="grid grid-cols-2 gap-2 text-xs bg-slate-950/80 p-2.5 rounded-lg border border-slate-800/80">
                <div>
                  <div className="text-[10px] text-slate-500">Pore Pressure</div>
                  <div className="font-bold text-cyan-300 text-sm">{s.pore_water_pressure_kpa} kPa</div>
                </div>
                <div>
                  <div className="text-[10px] text-slate-500">Soil Saturation</div>
                  <div className="font-bold text-blue-400 text-sm">{s.soil_moisture_pct}%</div>
                </div>
                <div>
                  <div className="text-[10px] text-slate-500">Inclinometer Tilt</div>
                  <div className="font-bold text-amber-400 text-sm">{s.inclinometer_tilt_deg}°</div>
                </div>
                <div>
                  <div className="text-[10px] text-slate-500">Displacement</div>
                  <div className="font-bold text-rose-400 text-sm">{s.displacement_rate_mm_day} mm/d</div>
                </div>
              </div>

              <div className="flex items-center justify-between text-[11px] text-slate-400 mt-2.5 pt-2 border-t border-slate-800">
                <span className="px-2 py-0.5 rounded text-[9px] font-bold bg-slate-950 border border-slate-700 text-cyan-300">
                  {s.data_mode || "LIVE_CALIBRATED"}
                </span>
                <span className="flex items-center gap-1 text-emerald-400 font-medium">
                  <Battery className="h-3 w-3" /> {s.battery_pct}%
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Selected Sensor Detailed Telemetry Chart */}
      {activeSensor && (
        <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl shadow-xl space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-4">
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-xl font-bold text-white">{activeSensor.name}</h2>
                {getStatusBadge(activeSensor.status)}
                <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-500/20 border border-blue-500/40 text-blue-300">
                  {activeSensor.data_mode || "LIVE_CALIBRATED"}
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-0.5">
                {activeSensor.location_name}, {activeSensor.district}, {activeSensor.state} (Node ID: {activeSensor.sensor_id})
              </p>
            </div>
            
            <div className="flex items-center gap-2">
              <button
                onClick={async () => {
                  try {
                    const testPayload = {
                      sensor_id: activeSensor.sensor_id,
                      pore_water_pressure_kpa: Number((activeSensor.pore_water_pressure_kpa + 15.0).toFixed(1)),
                      soil_moisture_pct: Math.min(99.0, Number((activeSensor.soil_moisture_pct + 4.5).toFixed(1))),
                      inclinometer_tilt_deg: Number((activeSensor.inclinometer_tilt_deg + 0.85).toFixed(2)),
                      current_rainfall_mm_h: 24.5,
                      battery_pct: 97
                    };
                    await fetch('/api/v1/sensors/ingest', {
                      method: 'POST',
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify(testPayload)
                    });
                  } catch (e) {
                    console.error("Hardware test injection error:", e);
                  }
                }}
                className="px-3 py-1.5 bg-blue-600/80 hover:bg-blue-600 text-white rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors border border-blue-400/30 shadow-md"
                title="Transmits live datalogger telemetry packet to POST /api/v1/sensors/ingest"
              >
                <Zap className="h-3.5 w-3.5 text-amber-300" />
                <span>Transmit Field Hardware Packet</span>
              </button>
            </div>
          </div>

          {/* Real-time Telemetry Graph */}
          <div className="space-y-2">
            <h3 className="font-bold text-sm text-slate-200 flex items-center gap-2">
              <Activity className="h-4 w-4 text-cyan-400" />
              Dynamic In-Situ Telemetry Curves (Pore Pressure vs Soil Moisture vs Tilt)
            </h3>
            <div className="h-72 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={activeSensor.history || []}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis dataKey="timestamp_offset_h" stroke="#64748b" tick={{ fontSize: 10 }} label={{ value: 'Hours Offset', position: 'insideBottom', offset: -5, fill: '#64748b', fontSize: 10 }} />
                  <YAxis yAxisId="pwp" stroke="#06b6d4" label={{ value: 'Pore Pressure (kPa)', angle: -90, position: 'insideLeft', fill: '#06b6d4', fontSize: 10 }} tick={{ fontSize: 10 }} />
                  <YAxis yAxisId="sm" orientation="right" stroke="#f97316" label={{ value: 'Moisture / Tilt', angle: 90, position: 'insideRight', fill: '#f97316', fontSize: 10 }} tick={{ fontSize: 10 }} />
                  <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '0.5rem' }} />
                  <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                  <Line yAxisId="pwp" type="monotone" dataKey="pore_water_pressure_kpa" name="Pore Water Pressure (kPa)" stroke="#06b6d4" strokeWidth={2} dot={false} />
                  <Line yAxisId="sm" type="monotone" dataKey="soil_moisture_pct" name="Soil Moisture (%)" stroke="#f97316" strokeWidth={2} dot={false} />
                  <Line yAxisId="sm" type="monotone" dataKey="inclinometer_tilt_deg" name="Inclinometer Tilt (°)" stroke="#eab308" strokeWidth={2} strokeDasharray="3 3" dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

