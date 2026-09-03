import React, { useState, useEffect, useCallback, useRef } from 'react';
import { 
  MapContainer, 
  TileLayer, 
  Marker, 
  Popup, 
  Polyline, 
  Circle, 
  CircleMarker,
  useMap, 
  useMapEvents,
  ZoomControl
} from 'react-leaflet';
import L from 'leaflet';
import { 
  Radio, 
  Zap, 
  Eye, 
  Layers, 
  Info,
  AlertTriangle,
  ShieldAlert
} from 'lucide-react';
import { predictRisk } from '../services/api';
import { TRANSLATIONS } from '../services/i18n';

const DEFAULT_MAP_CENTER = [26.2006, 92.9376];

const isFiniteCoordinate = (value) => typeof value === 'number' && Number.isFinite(value);

const isValidLatLng = (lat, lng) => (
  isFiniteCoordinate(lat)
  && isFiniteCoordinate(lng)
  && lat >= -90
  && lat <= 90
  && lng >= -180
  && lng <= 180
);

const isValidPosition = (position) => (
  Array.isArray(position)
  && position.length >= 2
  && isValidLatLng(position[0], position[1])
);

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
    if (isValidPosition(center)) {
      map.flyTo(center, zoom || 8, { duration: 1.5 });
    }
  }, [center, zoom, map]);
  return null;
}

// Map Click Inspector component for Terrain AI Risk Probe
function MapInspector({ onLocationClick }) {
  useMapEvents({
    click(e) {
      // Leaflet can bubble one physical interaction through nested map layers.
      // The parent callback deduplicates it before requesting a prediction.
      onLocationClick(e.latlng);
    }
  });
  return null;
}

import { useSelector } from 'react-redux';
import SubNav from './SubNav';

export default function GISMap({ 
  states = [], 
  highways = [], 
  sensors = [], 
  reports = [], 
  resources = [], 
  predictedRiskLocations = [],
  currentLang = 'en'
}) {
  const t = TRANSLATIONS[currentLang] || TRANSLATIONS.en;
  const activeRegion = useSelector((state) => state.navigation.activeRegion);

  // The map position is derived from the selected region, so it cannot become
  // stale when the available state data changes.
  const safeStates = Array.isArray(states) ? states : [];
  const safeHighways = Array.isArray(highways) ? highways : [];
  const safeSensors = Array.isArray(sensors) ? sensors : [];
  const safeReports = Array.isArray(reports) ? reports : [];
  const safeResources = Array.isArray(resources) ? resources : [];
  const safePredictedRiskLocations = Array.isArray(predictedRiskLocations)
    ? predictedRiskLocations
    : [];
  const selectedState = safeStates.find((state) => state?.name === activeRegion);
  const mapCenter = isValidPosition(selectedState?.center)
    ? selectedState.center
    : DEFAULT_MAP_CENTER;
  const zoomLevel = selectedState ? 9 : 7;

  // Layer Toggles
  const [showHeatmap, setShowHeatmap] = useState(true);
  const [showHighways, setShowHighways] = useState(true);
  const [showSensors, setShowSensors] = useState(true);
  const [showReports, setShowReports] = useState(true);
  const [showResources, setShowResources] = useState(true);
  const [showPredictedRisk, setShowPredictedRisk] = useState(true);

  // Probe state
  const [probeLocation, setProbeLocation] = useState(null);
  const [probeLoading, setProbeLoading] = useState(false);
  const [probeResult, setProbeResult] = useState(null);
  const activeProbeKey = useRef(null);
  const probeRequestId = useRef(0);

  const handleMapProbe = useCallback(async (latlng) => {
    if (!isValidLatLng(latlng?.lat, latlng?.lng)) return;

    const probeKey = `${latlng.lat.toFixed(5)},${latlng.lng.toFixed(5)}`;
    if (activeProbeKey.current === probeKey) return;

    activeProbeKey.current = probeKey;
    const requestId = ++probeRequestId.current;
    setProbeLocation(latlng);
    setProbeLoading(true);
    setProbeResult(null);
    try {
      const res = await predictRisk({
        lat: latlng.lat,
        lng: latlng.lng
      });
      if (requestId === probeRequestId.current) setProbeResult(res);
    } catch (err) {
      if (requestId === probeRequestId.current) console.error('Probe error:', err);
    } finally {
      if (requestId === probeRequestId.current) setProbeLoading(false);
    }
  }, []);

  const getHighwayColor = (riskLevel) => {
    switch (riskLevel) {
      case 'RED': return '#ef4444';
      case 'ORANGE': return '#f97316';
      case 'YELLOW': return '#eab308';
      default: return '#10b981';
    }
  };

  // Map model risk levels (GREEN/YELLOW/ORANGE/RED) to marker colors
  const getRiskColor = (level) => {
    switch (level) {
      case 'RED': return '#ef4444';
      case 'ORANGE': return '#f97316';
      case 'YELLOW': return '#eab308';
      case 'GREEN': default: return '#10b981';
    }
  };

  const getRiskRadius = (level) => {
    switch (level) {
      case 'RED': return 10;
      case 'ORANGE': return 9;
      case 'YELLOW': return 8;
      default: return 7;
    }
  };

  const getRiskBadgeClasses = (level) => {
    switch (level) {
      case 'RED': return 'bg-red-500 text-white';
      case 'ORANGE': return 'bg-orange-500 text-white';
      case 'YELLOW': return 'bg-yellow-500 text-slate-900';
      case 'GREEN': default: return 'bg-emerald-500 text-white';
    }
  };

  return (
    <div className="relative w-full h-[calc(100vh-6rem)] bg-slate-950 flex flex-col overflow-hidden">
      
      {/* Floating Glassmorphic SubNav for Regions */}
      <SubNav states={safeStates} />

      {/* Main Leaflet Map View */}
      <div className="relative min-h-0 flex-1 w-full">
        <MapContainer
          center={mapCenter}
          zoom={zoomLevel}
          scrollWheelZoom={true}
          zoomControl={false}
          className="absolute inset-0"
        >
          <ZoomControl position="bottomright" />
          <MapViewController center={mapCenter} zoom={zoomLevel} />
          <MapInspector onLocationClick={handleMapProbe} />

          {/* OpenStreetMap base tiles — public tiles with no API key required. */}
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
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
          {showHighways && safeHighways.filter((hw) => (
            Array.isArray(hw?.coordinates)
            && hw.coordinates.length >= 2
            && hw.coordinates.every(isValidPosition)
          )).map((hw) => {
            const color = getHighwayColor(hw.risk_level);
            return (
              <React.Fragment key={hw.corridor_id}>
                <Polyline
                  positions={hw.coordinates}
                  pathOptions={{
                    color: color,
                    weight: hw.risk_level === 'RED' ? 6 : 4,
                    dashArray: hw.status?.includes('BLOCKED') ? '8, 8' : undefined,
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
          {showSensors && safeSensors.filter((sensor) => isValidLatLng(sensor?.lat, sensor?.lng)).map((s) => (
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
          {showReports && safeReports.filter((report) => isValidLatLng(report?.lat, report?.lng)).map((r) => (
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
          {showResources && safeResources.filter((resource) => isValidLatLng(resource?.lat, resource?.lng)).map((res) => (
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

          {/* 6. ML Predicted Risk Locations — powered by LandslidePredictiveEngine.predict_risk() */}
          {showPredictedRisk && safePredictedRiskLocations.filter((feature) => {
            const coordinates = feature?.geometry?.coordinates;
            return Array.isArray(coordinates) && isValidLatLng(coordinates[1], coordinates[0]);
          }).map((feature, idx) => {
            const coords = feature.geometry.coordinates; // [lng, lat]
            const p = feature.properties || {};
            const color = getRiskColor(p.risk_level);
            const radius = getRiskRadius(p.risk_level);
            return (
              <CircleMarker
                key={`prl-${idx}`}
                center={[coords[1], coords[0]]}
                radius={radius}
                pathOptions={{
                  fillColor: color,
                  color: '#ffffff',
                  weight: 2,
                  opacity: 1,
                  fillOpacity: 0.85,
                }}
              >
                <Popup>
                  <div className="p-2 max-w-sm text-slate-100">
                    {/* Header */}
                    <div className="flex items-center justify-between gap-2 mb-1">
                      <span className="font-bold text-sm text-white flex items-center gap-1.5">
                        <ShieldAlert className="h-4 w-4 text-amber-400" />
                        {p.location_name}
                      </span>
                      <span className={`px-2 py-0.5 text-[10px] font-bold rounded ${getRiskBadgeClasses(p.risk_level)}`}>
                        {p.risk_level}
                      </span>
                    </div>
                    <p className="text-xs text-slate-400 mb-2">{p.state} • Risk Score: {Math.round(p.risk_score * 100)}%</p>

                    {/* Coordinates & Key Metrics */}
                    <div className="grid grid-cols-2 gap-2 text-xs bg-slate-900/90 p-2.5 rounded-lg border border-slate-700/80 mb-2">
                      <div className="bg-slate-800/60 p-1.5 rounded">
                        <div className="text-[10px] text-slate-400">Latitude</div>
                        <div className="font-bold text-white text-sm">{coords[1].toFixed(4)}</div>
                      </div>
                      <div className="bg-slate-800/60 p-1.5 rounded">
                        <div className="text-[10px] text-slate-400">Longitude</div>
                        <div className="font-bold text-white text-sm">{coords[0].toFixed(4)}</div>
                      </div>
                      <div className="bg-slate-800/60 p-1.5 rounded">
                        <div className="text-[10px] text-slate-400">Factor of Safety</div>
                        <div className={`font-bold text-sm ${p.factor_of_safety < 1.2 ? 'text-rose-400' : 'text-emerald-400'}`}>{p.factor_of_safety}</div>
                      </div>
                      <div className="bg-slate-800/60 p-1.5 rounded">
                        <div className="text-[10px] text-slate-400">Caine I-D Ratio</div>
                        <div className={`font-bold text-sm ${p.caine_threshold_ratio >= 1.0 ? 'text-rose-400' : 'text-amber-400'}`}>{p.caine_threshold_ratio}x</div>
                      </div>
                    </div>

                    {/* Environmental Inputs */}
                    <div className="grid grid-cols-2 gap-1.5 text-[11px] bg-slate-900/80 p-2 rounded border border-slate-700/60 mb-2">
                      <div><span className="text-slate-400">Slope:</span> <strong className="text-white">{p.slope_deg}°</strong></div>
                      <div><span className="text-slate-400">Elevation:</span> <strong className="text-white">{p.elevation_m}m</strong></div>
                      <div><span className="text-slate-400">Rain (3d):</span> <strong className="text-cyan-300">{p.rainfall_3d_mm}mm</strong></div>
                      <div><span className="text-slate-400">Rain (24h):</span> <strong className="text-cyan-300">{p.rainfall_24h_mm}mm</strong></div>
                      <div><span className="text-slate-400">Soil Moist:</span> <strong className="text-blue-400">{p.soil_moisture_pct}%</strong></div>
                      <div><span className="text-slate-400">Tilt Rate:</span> <strong className="text-amber-400">{p.inclinometer_tilt_rate_mm_day} mm/d</strong></div>
                      <div className="col-span-2"><span className="text-slate-400">Lithology:</span> <strong className="text-slate-200">{p.lithology_type}</strong></div>
                    </div>

                    {/* Contributing Factors */}
                    {Array.isArray(p.contributing_factors) && p.contributing_factors.length > 0 && (
                      <div className="text-[11px] bg-slate-900/50 p-1.5 rounded border border-slate-800 mb-2">
                        <span className="text-slate-400 font-bold">Contributing Factors:</span>
                        <ul className="mt-1 space-y-0.5">
                          {p.contributing_factors.map((cf, i) => (
                            <li key={i} className="text-slate-300">
                              <span className={`font-semibold ${cf.level === 'VERY HIGH' || cf.level === 'CRITICAL' ? 'text-rose-400' : cf.level === 'HIGH' ? 'text-orange-400' : 'text-amber-300'}`}>
                                {cf.level}
                              </span>
                              {' '}{cf.factor}: {cf.value}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* Dominant Trigger */}
                    {p.dominant_trigger && (
                      <div className="text-[11px] text-slate-300 bg-slate-900/50 p-1.5 rounded border border-slate-800 mb-2">
                        <span className="text-slate-400 font-bold">Dominant Trigger:</span> {p.dominant_trigger}
                      </div>
                    )}

                    {/* Disclaimer */}
                    <div className="text-[9px] text-amber-400/70 flex items-center gap-1 pt-1 border-t border-slate-800">
                      <AlertTriangle className="h-3 w-3 flex-shrink-0" />
                      Simulated demo inputs • Model v{p.model_version}
                    </div>
                  </div>
                </Popup>
              </CircleMarker>
            );
          })}

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
            <label className="flex items-center gap-2 cursor-pointer hover:text-white">
              <input type="checkbox" checked={showPredictedRisk} onChange={(e) => setShowPredictedRisk(e.target.checked)} className="rounded text-amber-500 focus:ring-0" />
              <span>ML Predicted Risk Locations ({safePredictedRiskLocations.length})</span>
            </label>
          </div>
          <div className="text-[10px] text-amber-400/80 pt-1 border-t border-slate-800 flex items-center gap-1">
            <Info className="h-3 w-3" />
            <span>Tip: Click anywhere on terrain to probe AI slope risk</span>
          </div>
          <div className="text-[9px] text-amber-400/60 flex items-center gap-1 mt-1">
            <AlertTriangle className="h-3 w-3 flex-shrink-0" />
            <span>Environmental/sensor values in ML Risk layer are simulated for prototype demo</span>
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
