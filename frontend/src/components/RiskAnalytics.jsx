import React, { useState, useEffect } from 'react';
import { 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer, 
  LineChart, 
  Line, 
  Legend 
} from 'recharts';
import { 
  Activity, 
  CloudRain, 
  Sliders, 
  ShieldAlert, 
  CheckCircle, 
  AlertOctagon, 
  TrendingUp, 
  Zap, 
  Layers 
} from 'lucide-react';
import { predictRisk, fetchWeatherForecast } from '../services/api';
import { TRANSLATIONS } from '../services/i18n';

export default function RiskAnalytics({ currentLang = 'en' }) {
  const t = TRANSLATIONS[currentLang] || TRANSLATIONS.en;

  // Simulator state
  const [slopeDeg, setSlopeDeg] = useState(38);
  const [rain3d, setRain3d] = useState(160);
  const [rain24h, setRain24h] = useState(65);
  const [soilMoisture, setSoilMoisture] = useState(84);
  const [tiltRate, setTiltRate] = useState(6.5);
  const [lithology, setLithology] = useState('Shale & Siltstone (Fragile)');

  // Prediction result state
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  // Weather forecast state
  const [forecastData, setForecastData] = useState([]);
  const [currentWx, setCurrentWx] = useState(null);
  const [selectedStation, setSelectedStation] = useState({ name: 'Shillong / Sonapur (Meghalaya)', lat: 25.1324, lng: 92.3682 });

  const runSimulation = async () => {
    setLoading(true);
    try {
      const res = await predictRisk({
        lat: selectedStation.lat,
        lng: selectedStation.lng,
        slope_deg: Number(slopeDeg),
        elevation_m: 1450,
        rainfall_3d_mm: Number(rain3d),
        rainfall_24h_mm: Number(rain24h),
        soil_moisture_pct: Number(soilMoisture),
        inclinometer_tilt_rate_mm_day: Number(tiltRate),
        lithology: lithology
      });
      setPrediction(res);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const loadForecast = async () => {
    try {
      const data = await fetchWeatherForecast(selectedStation.lat, selectedStation.lng, selectedStation.name);
      setCurrentWx(data.current);
      setForecastData(data.forecast_72h || []);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadForecast();
  }, [selectedStation]);

  useEffect(() => {
    const timer = setTimeout(() => {
      runSimulation();
    }, 500);
    return () => clearTimeout(timer);
  }, [slopeDeg, rain3d, rain24h, soilMoisture, tiltRate, lithology, selectedStation]);

  // Caine I-D theoretical curve points
  const caineCurveData = [
    { duration_h: 1, threshold: 14.8, actual: rain24h > 40 ? 18.2 : 8.5 },
    { duration_h: 3, threshold: 9.3, actual: rain24h > 40 ? 12.4 : 6.1 },
    { duration_h: 6, threshold: 7.0, actual: rain24h > 40 ? 9.8 : 4.5 },
    { duration_h: 12, threshold: 5.2, actual: rain24h > 40 ? 7.6 : 3.2 },
    { duration_h: 24, threshold: 3.9, actual: (rain24h / 24).toFixed(1) },
    { duration_h: 48, threshold: 2.9, actual: (rain3d / 48).toFixed(1) },
    { duration_h: 72, threshold: 2.5, actual: (rain3d / 72).toFixed(1) }
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-6 space-y-6">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/90 border border-slate-800 p-6 rounded-2xl shadow-xl">
        <div>
          <div className="flex items-center gap-2 text-amber-400 text-xs font-bold uppercase tracking-widest mb-1">
            <Activity className="h-4 w-4" />
            AI Landslide Predictive Modeling Engine
          </div>
          <h1 className="text-2xl font-black text-white">
            Hydro-Meteorological & Geotechnical Failure Analytics
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Combines Random Forest susceptibility models, Caine Intensity-Duration (I-D) thresholds, and Infinite Slope Factor of Safety ($F_s$) equilibrium models.
          </p>
        </div>

        {/* Station Selector */}
        <div className="flex items-center gap-2 bg-slate-950 p-2 rounded-xl border border-slate-800">
          <span className="text-xs text-slate-400 font-semibold pl-2">Region Sector:</span>
          <select
            value={selectedStation.name}
            onChange={(e) => {
              const options = [
                { name: 'Shillong / Sonapur (Meghalaya)', lat: 25.1324, lng: 92.3682 },
                { name: 'Teesta Valley / Rangpo (Sikkim)', lat: 27.0620, lng: 88.4325 },
                { name: 'Dzüdza / Kohima (Nagaland)', lat: 25.7225, lng: 93.9230 },
                { name: 'Dima Hasao / Haflong (Assam)', lat: 25.1215, lng: 92.9820 },
                { name: 'Sela Pass / Bomdila (Arunachal)', lat: 27.5020, lng: 92.1050 }
              ];
              const match = options.find(o => o.name === e.target.value);
              if (match) setSelectedStation(match);
            }}
            className="bg-slate-900 text-white text-xs font-semibold px-3 py-1.5 rounded-lg border border-slate-700 focus:outline-none cursor-pointer"
          >
            <option value="Shillong / Sonapur (Meghalaya)">Shillong / Sonapur (Meghalaya)</option>
            <option value="Teesta Valley / Rangpo (Sikkim)">Teesta Valley / Rangpo (Sikkim)</option>
            <option value="Dzüdza / Kohima (Nagaland)">Dzüdza / Kohima (Nagaland)</option>
            <option value="Dima Hasao / Haflong (Assam)">Dima Hasao / Haflong (Assam)</option>
            <option value="Sela Pass / Bomdila (Arunachal)">Sela Pass / Bomdila (Arunachal)</option>
          </select>
        </div>
      </div>

      {/* Top Metrics Cards */}
      {currentWx && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div className="bg-slate-900/80 border border-slate-800 p-4 rounded-xl">
            <div className="text-xs text-slate-400 font-medium">Current Rain Rate</div>
            <div className="text-xl font-bold text-cyan-400 mt-1 flex items-baseline gap-1">
              {currentWx.current_rainfall_rate_mm_h} <span className="text-xs text-slate-400 font-normal">mm/h</span>
            </div>
            <div className="text-[11px] text-slate-500 mt-1">{currentWx.weather_condition}</div>
          </div>

          <div className="bg-slate-900/80 border border-slate-800 p-4 rounded-xl">
            <div className="text-xs text-slate-400 font-medium">Antecedent Index (API-30)</div>
            <div className="text-xl font-bold text-amber-400 mt-1 flex items-baseline gap-1">
              {currentWx.api_30_mm} <span className="text-xs text-slate-400 font-normal">mm</span>
            </div>
            <div className="text-[11px] text-amber-400/80 mt-1">High Subsurface Retention</div>
          </div>

          <div className="bg-slate-900/80 border border-slate-800 p-4 rounded-xl">
            <div className="text-xs text-slate-400 font-medium">24h Cumulative Rain</div>
            <div className="text-xl font-bold text-blue-400 mt-1 flex items-baseline gap-1">
              {currentWx.rainfall_24h_mm} <span className="text-xs text-slate-400 font-normal">mm</span>
            </div>
            <div className="text-[11px] text-slate-500 mt-1">3-Day Total: {currentWx.rainfall_3d_mm} mm</div>
          </div>

          <div className="bg-slate-900/80 border border-slate-800 p-4 rounded-xl">
            <div className="text-xs text-slate-400 font-medium">IMD Warning Level</div>
            <div className="text-xl font-bold text-rose-400 mt-1 flex items-center gap-1.5">
              <span className={`h-3 w-3 rounded-full ${
                currentWx.imd_warning_level === 'RED' ? 'bg-red-500 animate-ping' :
                currentWx.imd_warning_level === 'ORANGE' ? 'bg-orange-500' : 'bg-emerald-500'
              }`}></span>
              {currentWx.imd_warning_level}
            </div>
            <div className="text-[11px] text-slate-500 mt-1">Precipitation Alert active</div>
          </div>
        </div>
      )}

      {/* Main Analysis Section: Charts + What-If Simulator */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left 7 Columns: Predictive Timeline & Caine Curves */}
        <div className="lg:col-span-7 space-y-6">
          {/* 72-Hour Predictive Hydro-Meteorological Forecast */}
          <div className="bg-slate-900/90 border border-slate-800 p-5 rounded-2xl shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="font-bold text-sm text-white flex items-center gap-2">
                  <CloudRain className="h-4 w-4 text-cyan-400" />
                  72-Hour Predictive Rainfall & Soil Saturation Forecast
                </h3>
                <p className="text-xs text-slate-400">
                  Predicted precipitation bursts vs cumulative soil pore pressure saturation.
                </p>
              </div>
            </div>
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={forecastData}>
                  <defs>
                    <linearGradient id="rainGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.8}/>
                      <stop offset="95%" stopColor="#06b6d4" stopOpacity={0}/>
                    </linearGradient>
                    <linearGradient id="satGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#f97316" stopOpacity={0.8}/>
                      <stop offset="95%" stopColor="#f97316" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis dataKey="time" stroke="#64748b" tick={{ fontSize: 10 }} />
                  <YAxis yAxisId="left" stroke="#06b6d4" tick={{ fontSize: 10 }} />
                  <YAxis yAxisId="right" orientation="right" stroke="#f97316" tick={{ fontSize: 10 }} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '0.5rem' }}
                    labelStyle={{ color: '#94a3b8', fontSize: '11px' }}
                  />
                  <Area yAxisId="left" type="monotone" dataKey="rainfall_intensity_mm_h" name="Rain Intensity (mm/h)" stroke="#06b6d4" fillOpacity={1} fill="url(#rainGrad)" />
                  <Area yAxisId="right" type="monotone" dataKey="soil_saturation_forecast_pct" name="Soil Saturation (%)" stroke="#f97316" fillOpacity={1} fill="url(#satGrad)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Caine Intensity-Duration (I-D) Threshold Model */}
          <div className="bg-slate-900/90 border border-slate-800 p-5 rounded-2xl shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="font-bold text-sm text-white flex items-center gap-2">
                  <TrendingUp className="h-4 w-4 text-amber-400" />
                  Empirical Caine Intensity-Duration (I-D) Failure Threshold
                </h3>
                <p className="text-xs text-slate-400">
                  Calculated using \(I = 14.82 \cdot D^{'{'}-0.42{'}'}\) calibrated for Eastern Himalayas. Points above red line breach trigger threshold.
                </p>
              </div>
            </div>
            <div className="h-56 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={caineCurveData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis dataKey="duration_h" stroke="#64748b" label={{ value: 'Duration (Hours)', position: 'insideBottom', offset: -5, fill: '#64748b', fontSize: 10 }} tick={{ fontSize: 10 }} />
                  <YAxis stroke="#64748b" label={{ value: 'Intensity (mm/h)', angle: -90, position: 'insideLeft', fill: '#64748b', fontSize: 10 }} tick={{ fontSize: 10 }} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '0.5rem' }}
                  />
                  <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                  <Line type="monotone" dataKey="threshold" name="Caine Threshold (Failure Boundary)" stroke="#ef4444" strokeWidth={2.5} strokeDasharray="4 4" dot={false} />
                  <Line type="monotone" dataKey="actual" name="Actual Recorded Cloudburst Pulse" stroke="#38bdf8" strokeWidth={2.5} dot={{ r: 4, fill: '#38bdf8' }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Right 5 Columns: Interactive AI Parameter Simulator */}
        <div className="lg:col-span-5 space-y-6">
          <div className="bg-slate-900/90 border border-slate-800 p-5 rounded-2xl shadow-xl space-y-5">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div>
                <h3 className="font-bold text-sm text-white flex items-center gap-2">
                  <Sliders className="h-4 w-4 text-orange-400" />
                  Interactive AI Parameter Simulator
                </h3>
                <p className="text-[11px] text-slate-400">
                  Simulate what-if slope failure scenarios in real time.
                </p>
              </div>
              <button
                onClick={runSimulation}
                className="px-3 py-1 bg-gradient-to-r from-amber-500 to-orange-600 text-slate-950 font-bold text-xs rounded-lg hover:brightness-110 transition-all flex items-center gap-1 shadow-md"
              >
                <Zap className="h-3 w-3" />
                Recalculate
              </button>
            </div>

            {/* Parameter Sliders */}
            <div className="space-y-4 text-xs">
              {/* Slope Angle */}
              <div>
                <div className="flex justify-between font-semibold mb-1">
                  <span className="text-slate-300">Slope Gradient (\(\alpha\)):</span>
                  <span className="text-amber-400 font-bold">{slopeDeg}°</span>
                </div>
                <input
                  type="range"
                  min="10"
                  max="65"
                  value={slopeDeg}
                  onChange={(e) => { setSlopeDeg(e.target.value); }}
                  className="w-full accent-amber-500"
                />
              </div>

              {/* 3-Day Cumulative Rainfall */}
              <div>
                <div className="flex justify-between font-semibold mb-1">
                  <span className="text-slate-300">3-Day Cumulative Rainfall:</span>
                  <span className="text-cyan-400 font-bold">{rain3d} mm</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="450"
                  value={rain3d}
                  onChange={(e) => { setRain3d(e.target.value); }}
                  className="w-full accent-cyan-500"
                />
              </div>

              {/* 24h Peak Rain */}
              <div>
                <div className="flex justify-between font-semibold mb-1">
                  <span className="text-slate-300">24-Hour Peak Rain Volume:</span>
                  <span className="text-blue-400 font-bold">{rain24h} mm</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="200"
                  value={rain24h}
                  onChange={(e) => { setRain24h(e.target.value); }}
                  className="w-full accent-blue-500"
                />
              </div>

              {/* Soil Moisture Saturation */}
              <div>
                <div className="flex justify-between font-semibold mb-1">
                  <span className="text-slate-300">In-situ Soil Saturation:</span>
                  <span className="text-orange-400 font-bold">{soilMoisture}%</span>
                </div>
                <input
                  type="range"
                  min="20"
                  max="100"
                  value={soilMoisture}
                  onChange={(e) => { setSoilMoisture(e.target.value); }}
                  className="w-full accent-orange-500"
                />
              </div>

              {/* Inclinometer Drift Rate */}
              <div>
                <div className="flex justify-between font-semibold mb-1">
                  <span className="text-slate-300">Inclinometer Shear Rate:</span>
                  <span className="text-rose-400 font-bold">{tiltRate} mm/day</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="20"
                  step="0.5"
                  value={tiltRate}
                  onChange={(e) => { setTiltRate(e.target.value); }}
                  className="w-full accent-rose-500"
                />
              </div>

              {/* Lithology */}
              <div>
                <div className="text-slate-300 font-semibold mb-1">Lithology / Rock Type:</div>
                <select
                  value={lithology}
                  onChange={(e) => { setLithology(e.target.value); }}
                  className="w-full bg-slate-950 border border-slate-700 text-white rounded-lg p-2 font-medium"
                >
                  <option value="Shale & Siltstone (Fragile)">Shale & Siltstone (Fragile Disang Group)</option>
                  <option value="Weathered Schist / Disang Flysch">Weathered Schist / Daling Group</option>
                  <option value="Sandstone">Tertiary Sandstone (Tipam Formation)</option>
                  <option value="Granite / Gneiss">Granite / Gneiss Complex</option>
                </select>
              </div>
            </div>

            {/* Instant AI Evaluation Card */}
            {prediction && (
              <div className={`p-4 rounded-xl border ${
                prediction.risk_level === 'RED' ? 'bg-red-950/40 border-red-800/80 text-red-200' :
                prediction.risk_level === 'ORANGE' ? 'bg-orange-950/40 border-orange-800/80 text-orange-200' :
                prediction.risk_level === 'YELLOW' ? 'bg-amber-950/40 border-amber-800/80 text-amber-200' :
                'bg-emerald-950/40 border-emerald-800/80 text-emerald-200'
              } space-y-3`}>
                <div className="flex items-center justify-between">
                  <span className="font-bold text-xs uppercase tracking-wider text-slate-300">Predicted Risk Output</span>
                  <span className={`px-2.5 py-1 text-xs font-black rounded ${
                    prediction.risk_level === 'RED' ? 'bg-red-600 text-white animate-pulse' :
                    prediction.risk_level === 'ORANGE' ? 'bg-orange-600 text-white' : 'bg-emerald-600 text-white'
                  }`}>
                    {prediction.risk_level} ALERT
                  </span>
                </div>

                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div className="bg-slate-900/80 p-2 rounded border border-slate-800">
                    <div className="text-[10px] text-slate-400">Risk Score</div>
                    <div className="font-black text-base text-white">{Math.round(prediction.risk_score * 100)}%</div>
                  </div>
                  <div className="bg-slate-900/80 p-2 rounded border border-slate-800">
                    <div className="text-[10px] text-slate-400">Factor of Safety (\(F_s\))</div>
                    <div className={`font-black text-base ${prediction.factor_of_safety < 1.0 ? 'text-red-400' : 'text-emerald-400'}`}>
                      {prediction.factor_of_safety}
                    </div>
                  </div>
                  <div className="bg-slate-900/80 p-2 rounded border border-slate-800">
                    <div className="text-[10px] text-slate-400">I-D Threshold Ratio</div>
                    <div className="font-black text-base text-amber-300">{prediction.caine_threshold_ratio}x</div>
                  </div>
                  <div className="bg-slate-900/80 p-2 rounded border border-slate-800">
                    <div className="text-[10px] text-slate-400">48h Risk Outlook</div>
                    <div className="font-black text-base text-purple-300">{prediction.forecast_48h_level}</div>
                  </div>
                </div>

                <div className="text-[11px] bg-black/40 p-2 rounded border border-slate-800">
                  <span className="font-bold text-slate-200">Dominant Failure Trigger:</span>
                  <div className="text-slate-300 mt-0.5">{prediction.dominant_trigger}</div>
                </div>

                <div className="text-[11px] space-y-1">
                  <span className="font-bold text-slate-200">{t.recommendations}:</span>
                  <ul className="list-disc list-inside space-y-0.5 text-slate-300">
                    {prediction.recommendations.map((r, i) => (
                      <li key={i}>{r}</li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

