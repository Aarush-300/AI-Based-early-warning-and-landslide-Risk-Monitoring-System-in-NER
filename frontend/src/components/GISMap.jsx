import React, { useState, useEffect } from 'react';
import { 
  MapContainer, 
  TileLayer, 
  Marker, 
  Popup, 
  Polyline, 
  Circle, 
  useMap, 
  useMapEvents 
} from 'react-leaflet';
import L from 'leaflet';
import { 
  Radio, 
  AlertTriangle, 
  ShieldCheck, 
  Truck, 
  Building, 
  Compass, 
  Zap, 
  Eye, 
  Droplet, 
  Layers, 
  Info,
  Maximize2
} from 'lucide-react';
import { predictRisk } from '../services/api';
import { TRANSLATIONS } from '../services/i18n';

// Fix standard Leaflet icon paths
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

// Custom Icon Creators
const createSensorIcon = (status) => {
  const color = status === 'CRITICAL' ? '#ef4444' : (status === 'WARNING' ? '#f97316' : (status === 'WATCH' ? '#eab308' : '#10b981'));
  const pulseClass = status === 'CRITICAL' ? 'pulse-red' : '';
  return L.divIcon({
    className: 'custom-sensor-marker',
    html: `<div style="background-color: ${color}; width: 22px; height: 22px; border-radius: 50%; border: 3px solid #ffffff; box-shadow: 0 0 10px ${color}; display: flex; align-items: center; justify-content: center;" class="${pulseClass}">
      <span style="width: 6px; height: 6px; background: white; border-radius: 50%;"></span>
    </div>`,
    iconSize: [22, 22],
    iconAnchor: [11, 11]
  });
};

const createReportIcon = (severity) => {
  const color = severity === 'CRITICAL' ? '#dc2626' : (severity === 'HIGH' ? '#ea580c' : '#ca8a04');
  return L.divIcon({
    className: 'custom-report-marker',
    html: `<div style="background-color: ${color}; width: 26px; height: 26px; border-radius: 6px; border: 2px solid #ffffff; display: flex; align-items: center; justify-content: center; transform: rotate(45deg);">
      <span style="transform: rotate(-45deg); font-weight: bold; font-size: 13px; color: white;">!</span>
    </div>`,
    iconSize: [26, 26],
    iconAnchor: [13, 13]
  });
};

const createResourceIcon = (type) => {
  const isHospital = type === 'HOSPITAL';
  const color = isHospital ? '#38bdf8' : '#8b5cf6';
  return L.divIcon({
    className: 'custom-resource-marker',
    html: `<div style="background-color: ${color}; width: 24px; height: 24px; border-radius: 50%; border: 2px solid white; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: bold; color: white;">
      ${isHospital ? 'H' : 'R'}
    </div>`,
    iconSize: [24, 24],
    iconAnchor: [12, 12]
  });
};

// Map View Controller component
function MapViewController({ center, zoom }) {
  const map = useMap();
  useEffect(() => {
    if (center) {
      map.flyTo(center, zoom || 8, { duration: 1.5 });
    }
  }, [center, zoom, map]);
  return null;
}

// Map Click Inspector component for Terrain AI Risk Probe
function MapInspector({ onLocationClick }) {
  useMapEvents({
    click(e) {
      onLocationClick(e.latlng);
    }
  });
  return null;
}

export default function GISMap({ 
  states = [], 
  highways = [], 
  sensors = [], 
  reports = [], 
  resources = [], 
  historical = [],
  currentLang = 'en'
}) {
  const t = TRANSLATIONS[currentLang] || TRANSLATIONS.en;

  const [mapCenter, setMapCenter] = useState([26.2006, 92.9376]); // Center of North East India
  const [zoomLevel, setZoomLevel] = useState(7);
  const [selectedState, setSelectedState] = useState(null);

  // Layer Toggles
  const [showHeatmap, setShowHeatmap] = useState(true);
  const [showHighways, setShowHighways] = useState(true);
  const [showSensors, setShowSensors] = useState(true);
  const [showReports, setShowReports] = useState(true);
  const [showResources, setShowResources] = useState(true);
  const [showHistorical, setShowHistorical] = useState(true);

  // Probe state
  const [probeLocation, setProbeLocation] = useState(null);
  const [probeLoading, setProbeLoading] = useState(false);
  const [probeResult, setProbeResult] = useState(null);

  const handleStateClick = (state) => {
    setSelectedState(state.name);
    setMapCenter(state.center);
    setZoomLevel(9);
  };

  const handleMapProbe = async (latlng) => {
    setProbeLocation(latlng);
    setProbeLoading(true);
    setProbeResult(null);
    try {
      const res = await predictRisk({
        lat: latlng.lat,
        lng: latlng.lng,
        slope_deg: 36.0,
        elevation_m: 1600.0,
        rainfall_3d_mm: 140.0,
        rainfall_24h_mm: 55.0,
        soil_moisture_pct: 82.0,
        inclinometer_tilt_rate_mm_day: 4.2
      });
      setProbeResult(res);
    } catch (err) {
      console.error('Probe error:', err);
    } finally {
      setProbeLoading(false);
    }
  };

  const getHighwayColor = (riskLevel) => {
    switch (riskLevel) {
      case 'RED': return '#ef4444';
      case 'ORANGE': return '#f97316';
      case 'YELLOW': return '#eab308';
      default: return '#10b981';
    }
  };

  return (
    <div className="relative w-full h-[calc(100vh-6rem)] bg-slate-950 flex flex-col overflow-hidden">
      {/* Top Floating State Selector Bar */}
      <div className="absolute top-3 left-3 right-3 z-[1000] flex flex-wrap items-center gap-1.5 p-2 bg-slate-900/90 backdrop-blur-md rounded-xl border border-slate-800 shadow-2xl">
        <span className="text-[11px] font-bold text-amber-400 uppercase tracking-wider px-2 flex items-center gap-1">
          <Compass className="h-3.5 w-3.5" />
          {t.quick_states}:
        </span>
        <button
          onClick={() => {
            setSelectedState(null);
            setMapCenter([26.2006, 92.9376]);
            setZoomLevel(7);
          }}
          className={`px-2.5 py-1 text-xs font-semibold rounded-lg transition-all ${
            !selectedState 
              ? 'bg-amber-500 text-slate-950 shadow-md font-bold' 
              : 'text-slate-300 hover:bg-slate-800'
          }`}
        >
          All NER (Overview)
        </button>
        {states.map((st) => (
          <button
            key={st.name}
            onClick={() => handleStateClick(st)}
            className={`px-2.5 py-1 text-xs font-semibold rounded-lg transition-all ${
              selectedState === st.name 
                ? 'bg-gradient-to-r from-orange-500 to-amber-500 text-white shadow-md font-bold' 
                : 'text-slate-300 hover:bg-slate-800'
            }`}
          >
            {st.name}
          </button>
        ))}
      </div>

      {/* Main Leaflet Map View */}
      <div className="flex-1 w-full h-full relative">
        <MapContainer
          center={mapCenter}
          zoom={zoomLevel}
          scrollWheelZoom={true}
          className="w-full h-full"
        >
          <MapViewController center={mapCenter} zoom={zoomLevel} />
          <MapInspector onLocationClick={handleMapProbe} />

          {/* CartoDB Dark Matter Base Tiles */}
          <TileLayer
            attribution='&copy; <a href="https://carto.com/">CARTO</a> &copy; OpenStreetMap contributors'
            url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
          />

          {/* 1. Landslide Risk Heatmap & Hazard Buffers */}
          {showHeatmap && (
            <>
              {/* High risk zones */}
              <Circle
                center={[25.1324, 92.3682]} // Sonapur Tunnel zone
                radius={8000}
                pathOptions={{ color: '#ef4444', fillColor: '#ef4444', fillOpacity: 0.35, weight: 2 }}
              />
              <Circle
                center={[27.0620, 88.4325]} // Teesta Valley 29th mile
                radius={7500}
                pathOptions={{ color: '#ef4444', fillColor: '#ef4444', fillOpacity: 0.32, weight: 2 }}
              />
              <Circle
                center={[25.7225, 93.9230]} // Dzüdza Bridge Nagaland
                radius={6000}
                pathOptions={{ color: '#f97316', fillColor: '#f97316', fillOpacity: 0.28, weight: 2 }}
              />
              <Circle
                center={[25.1215, 92.9820]} // Dima Hasao Jatinga
                radius={6500}
                pathOptions={{ color: '#f97316', fillColor: '#f97316', fillOpacity: 0.28, weight: 2 }}
              />
            </>
          )}

          {/* 2. Highway Corridors */}
          {showHighways && highways.map((hw) => {
            const color = getHighwayColor(hw.risk_level);
            return (
              <React.Fragment key={hw.corridor_id}>
                <Polyline
                  positions={hw.coordinates}
                  pathOptions={{
                    color: color,
                    weight: hw.risk_level === 'RED' ? 6 : 4,
                    dashArray: hw.status.includes('BLOCKED') ? '8, 8' : undefined,
                    opacity: 0.95
                  }}
                >
                  <Popup>
                    <div className="p-2 max-w-xs text-slate-100">
                      <div className="flex items-center justify-between gap-2 mb-1">
                        <span className="font-bold text-sm text-white">{hw.highway_name}</span>
                        <span className={`px-2 py-0.5 text-[10px] font-bold rounded ${
                          hw.risk_level === 'RED' ? 'bg-red-500/20 text-red-400 border border-red-500/30' :
                          hw.risk_level === 'ORANGE' ? 'bg-orange-500/20 text-orange-400 border border-orange-500/30' :
                          'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                        }`}>
                          {hw.risk_level}
                        </span>
                      </div>
                      <p className="text-xs text-slate-300 font-medium mb-1.5">{hw.stretch_name}</p>
                      <div className="bg-slate-900/80 p-2 rounded border border-slate-700 text-xs space-y-1 mb-2">
                        <div className="flex justify-between">
                          <span className="text-slate-400">Status:</span>
                          <span className="font-semibold text-amber-300">{hw.status.replace(/_/g, ' ')}</span>
                        </div>
                        {hw.clearing_eta_hours > 0 && (
                          <div className="flex justify-between">
                            <span className="text-slate-400">{t.clearance_eta}:</span>
                            <span className="font-semibold text-white">{hw.clearing_eta_hours} Hours</span>
                          </div>
                        )}
                        <div className="flex justify-between">
                          <span className="text-slate-400">{t.stranded_vehicles}:</span>
                          <span className="font-semibold text-rose-400">{hw.stranded_vehicles_estimate}</span>
                        </div>
                      </div>
                      {hw.blockage_cause && (
                        <p className="text-[11px] text-rose-300 mb-2 italic">
                          "{hw.blockage_cause}"
                        </p>
                      )}
                      {hw.alternate_route && (
                        <div className="text-[11px] bg-amber-950/40 border border-amber-800/40 p-1.5 rounded text-amber-200">
                          <span className="font-bold text-amber-400">{t.alternate_route}:</span> {hw.alternate_route}
                        </div>
                      )}
                    </div>
                  </Popup>
                </Polyline>
              </React.Fragment>
            );
          })}

          {/* 3. Real-Time IoT Sensor Nodes */}
          {showSensors && sensors.map((s) => (
            <Marker
              key={s.sensor_id}
              position={[s.lat, s.lng]}
              icon={createSensorIcon(s.status)}
            >
              <Popup>
                <div className="p-2 max-w-sm text-slate-100">
                  <div className="flex items-center justify-between gap-2 mb-1">
                    <span className="font-bold text-sm text-white flex items-center gap-1.5">
                      <Radio className="h-4 w-4 text-amber-400 animate-pulse" />
                      {s.name}
                    </span>
                    <span className={`px-2 py-0.5 text-[10px] font-bold rounded ${
                      s.status === 'CRITICAL' ? 'bg-red-600 text-white' :
                      s.status === 'WARNING' ? 'bg-orange-600 text-white' : 'bg-emerald-600 text-white'
                    }`}>
                      {s.status}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 mb-2">{s.location_name}, {s.state}</p>
                  <div className="grid grid-cols-2 gap-2 text-xs bg-slate-900/90 p-2.5 rounded-lg border border-slate-700/80 mb-2">
                    <div className="bg-slate-800/60 p-1.5 rounded">
                      <div className="text-[10px] text-slate-400">Pore Water Press.</div>
                      <div className="font-bold text-cyan-300 text-sm">{s.pore_water_pressure_kpa} kPa</div>
                    </div>
                    <div className="bg-slate-800/60 p-1.5 rounded">
                      <div className="text-[10px] text-slate-400">Soil Moisture</div>
                      <div className="font-bold text-blue-400 text-sm">{s.soil_moisture_pct}%</div>
                    </div>
                    <div className="bg-slate-800/60 p-1.5 rounded">
                      <div className="text-[10px] text-slate-400">Inclinometer Tilt</div>
                      <div className="font-bold text-amber-400 text-sm">{s.inclinometer_tilt_deg}°</div>
                    </div>
                    <div className="bg-slate-800/60 p-1.5 rounded">
                      <div className="text-[10px] text-slate-400">Displacement Rate</div>
                      <div className="font-bold text-rose-400 text-sm">{s.displacement_rate_mm_day} mm/d</div>
                    </div>
                  </div>
                  <div className="flex items-center justify-between text-[11px] text-slate-400">
                    <span>Rainfall: <strong className="text-white">{s.current_rainfall_mm_h} mm/h</strong></span>
                    <span>Battery: <strong className="text-emerald-400">{s.battery_pct}%</strong></span>
                  </div>
                </div>
              </Popup>
            </Marker>
          ))}

          {/* 4. Verified Field Reports */}
          {showReports && reports.map((r) => (
            <Marker
              key={r.id}
              position={[r.lat, r.lng]}
              icon={createReportIcon(r.ai_analysis?.severity_level || 'HIGH')}
            >
              <Popup>
                <div className="p-2 max-w-xs text-slate-100">
                  <div className="flex items-center justify-between gap-1 mb-1">
                    <span className="font-bold text-xs text-amber-400">{r.hazard_type}</span>
                    <span className="px-1.5 py-0.5 text-[9px] bg-slate-800 text-slate-300 rounded border border-slate-700">
                      {r.reporter_role}
                    </span>
                  </div>
                  <p className="text-xs text-slate-300 mb-1 font-semibold">{r.landmark}</p>
                  <p className="text-[11px] text-slate-400 mb-2 italic">"{r.description}"</p>
                  {r.ai_analysis && (
                    <div className="bg-slate-900/90 border border-slate-700/80 p-2 rounded text-[11px] space-y-1">
                      <div className="font-bold text-cyan-300 flex items-center gap-1">
                        <Eye className="h-3 w-3" />
                        AI Diagnosis: {r.ai_analysis.hazard_classification}
                      </div>
                      <div className="text-slate-300">
                        Severity: <strong className="text-rose-400">{r.ai_analysis.severity_level}</strong> (Conf: {Math.round(r.ai_analysis.confidence_score * 100)}%)
                      </div>
                      {r.ai_analysis.estimated_crack_width_mm && (
                        <div className="text-slate-400">
                          {t.crack_width}: <span className="text-amber-300 font-bold">{r.ai_analysis.estimated_crack_width_mm} mm</span>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </Popup>
            </Marker>
          ))}

          {/* 5. Emergency Shelters & Hospitals */}
          {showResources && resources.map((res) => (
            <Marker
              key={res.id}
              position={[res.lat, res.lng]}
              icon={createResourceIcon(res.type)}
            >
              <Popup>
                <div className="p-2 max-w-xs text-slate-100">
                  <div className="font-bold text-sm text-purple-300 mb-1">{res.name}</div>
                  <p className="text-xs text-slate-400 mb-2">{res.type.replace('_', ' ')} • {res.district}, {res.state}</p>
                  <div className="bg-slate-900 p-2 rounded text-xs space-y-1 border border-slate-700">
                    <div>Capacity: <strong className="text-white">{res.capacity_persons} Persons</strong></div>
                    <div>Emergency Hotline: <strong className="text-emerald-400">{res.contact}</strong></div>
                    {res.heavy_equipment && (
                      <div className="pt-1 text-[11px] text-slate-300">
                        <span className="text-slate-400">Deployment Assets:</span>
                        <ul className="list-disc list-inside mt-0.5 text-slate-200">
                          {res.heavy_equipment.map((eq, idx) => (
                            <li key={idx}>{eq}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </div>
              </Popup>
            </Marker>
          ))}

          {/* Interactive Map Probe Result Popup */}
          {probeLocation && (
            <Popup position={[probeLocation.lat, probeLocation.lng]}>
              <div className="p-2 max-w-xs text-slate-100">
                <div className="flex items-center gap-1.5 mb-1 font-bold text-sm text-amber-400">
                  <Zap className="h-4 w-4" />
                  Terrain AI Slope Risk Probe
                </div>
                <div className="text-[11px] text-slate-400 mb-2">
                  Lat: {probeLocation.lat.toFixed(4)}, Lng: {probeLocation.lng.toFixed(4)}
                </div>
                {probeLoading ? (
                  <div className="py-4 text-center text-xs text-slate-300 animate-pulse">
                    Analyzing Digital Elevation & Geotech Infiltration Models...
                  </div>
                ) : probeResult ? (
                  <div className="space-y-2">
                    <div className="flex items-center justify-between bg-slate-900 p-2 rounded border border-slate-700">
                      <span className="text-xs text-slate-300">{t.risk_score}:</span>
                      <span className={`px-2 py-0.5 text-xs font-bold rounded ${
                        probeResult.risk_level === 'RED' ? 'bg-red-500 text-white' :
                        probeResult.risk_level === 'ORANGE' ? 'bg-orange-500 text-white' : 'bg-emerald-500 text-white'
                      }`}>
                        {probeResult.risk_level} ({Math.round(probeResult.risk_score * 100)}%)
                      </span>
                    </div>
                    <div className="grid grid-cols-2 gap-1 text-[11px] bg-slate-900/80 p-2 rounded">
                      <div>Fs Factor: <strong className="text-white">{probeResult.factor_of_safety}</strong></div>
                      <div>I-D Ratio: <strong className="text-amber-400">{probeResult.caine_threshold_ratio}x</strong></div>
                    </div>
                    <div className="text-[11px] text-slate-300 bg-slate-900/50 p-1.5 rounded border border-slate-800">
                      <span className="text-slate-400 font-bold">Dominant Trigger:</span> {probeResult.dominant_trigger}
                    </div>
                  </div>
                ) : null}
              </div>
            </Popup>
          )}
        </MapContainer>

        {/* Floating Layer Toggle Panel */}
        <div className="absolute bottom-4 left-4 z-[1000] bg-slate-900/90 backdrop-blur-md p-3 rounded-xl border border-slate-800 shadow-2xl text-xs space-y-2 max-w-xs">
          <div className="flex items-center gap-1.5 font-bold text-slate-200 border-b border-slate-800 pb-1.5">
            <Layers className="h-4 w-4 text-amber-400" />
            <span>GIS Map Layer Controls</span>
          </div>
          <div className="space-y-1.5 text-slate-300">
            <label className="flex items-center gap-2 cursor-pointer hover:text-white">
              <input type="checkbox" checked={showHeatmap} onChange={(e) => setShowHeatmap(e.target.checked)} className="rounded text-amber-500 focus:ring-0" />
              <span>Susceptibility Heatmap Buffers</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer hover:text-white">
              <input type="checkbox" checked={showHighways} onChange={(e) => setShowHighways(e.target.checked)} className="rounded text-amber-500 focus:ring-0" />
              <span>Highway Corridors (NH-10, NH-29, NH-06)</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer hover:text-white">
              <input type="checkbox" checked={showSensors} onChange={(e) => setShowSensors(e.target.checked)} className="rounded text-amber-500 focus:ring-0" />
              <span>Live Geotech IoT Sensor Nodes</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer hover:text-white">
              <input type="checkbox" checked={showReports} onChange={(e) => setShowReports(e.target.checked)} className="rounded text-amber-500 focus:ring-0" />
              <span>Citizen/Field Reports & Cracks</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer hover:text-white">
              <input type="checkbox" checked={showResources} onChange={(e) => setShowResources(e.target.checked)} className="rounded text-amber-500 focus:ring-0" />
              <span>Hospitals & NDRF Emergency Bases</span>
            </label>
          </div>
          <div className="text-[10px] text-amber-400/80 pt-1 border-t border-slate-800 flex items-center gap-1">
            <Info className="h-3 w-3" />
            <span>Tip: Click anywhere on terrain to probe AI slope risk</span>
          </div>
        </div>

        {/* Legend Panel */}
        <div className="absolute bottom-4 right-4 z-[1000] bg-slate-900/90 backdrop-blur-md p-3 rounded-xl border border-slate-800 shadow-2xl text-xs space-y-1.5 hidden md:block">
          <div className="font-bold text-slate-200 mb-1">Risk Severity Legend</div>
          <div className="flex items-center gap-2">
            <span className="w-3 h-3 rounded-full bg-red-500"></span>
            <span className="text-slate-300">Red: Imminent Failure / Blocked</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-3 h-3 rounded-full bg-orange-500"></span>
            <span className="text-slate-300">Orange: High Warning / Cracks</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-3 h-3 rounded-full bg-yellow-500"></span>
            <span className="text-slate-300">Yellow: Advisory / Vigilance</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-3 h-3 rounded-full bg-emerald-500"></span>
            <span className="text-slate-300">Green: Baseline Normal</span>
          </div>
        </div>
      </div>
    </div>
  );
}

