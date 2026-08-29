import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import Navbar from './components/Navbar';
import GISMap from './components/GISMap';
import RiskAnalytics from './components/RiskAnalytics';
import RoadConnectivity from './components/RoadConnectivity';
import SensorTelemetry from './components/SensorTelemetry';
import FieldReporting from './components/FieldReporting';
import AlertBroadcast from './components/AlertBroadcast';

import { 
  fetchOverview, 
  fetchStates, 
  fetchHighways, 
  fetchSensors, 
  fetchReports, 
  fetchAlerts, 
  fetchRoads,
  fetchEmergencyResources,
  fetchHistoricalLandslides
} from './services/api';

export default function App() {
  const currentTab = useSelector((state) => state.navigation.activeModule);
  const [currentLang, setCurrentLang] = useState('en');

  // Master Data States
  const [overview, setOverview] = useState(null);
  const [states, setStates] = useState([]);
  const [highways, setHighways] = useState([]);
  const [sensors, setSensors] = useState([]);
  const [reports, setReports] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [roads, setRoads] = useState([]);
  const [resources, setResources] = useState([]);
  const [historical, setHistorical] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadAllData = async () => {
    try {
      const [
        ovData,
        stData,
        hwData,
        snData,
        rpData,
        alData,
        rdData,
        rsData,
        hsData
      ] = await Promise.all([
        fetchOverview().catch(() => null),
        fetchStates().catch(() => []),
        fetchHighways().catch(() => []),
        fetchSensors().catch(() => []),
        fetchReports().catch(() => []),
        fetchAlerts().catch(() => []),
        fetchRoads().catch(() => []),
        fetchEmergencyResources().catch(() => []),
        fetchHistoricalLandslides().catch(() => [])
      ]);

      if (ovData) setOverview(ovData);
      setStates(stData || []);
      setHighways(hwData || []);
      setSensors(snData || []);
      setReports(rpData || []);
      setAlerts(alData || []);
      setRoads(rdData || []);
      setResources(rsData || []);
      setHistorical(hsData || []);
    } catch (err) {
      console.error('Failed loading initial master dataset:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAllData();

    // Setup WebSocket connection for live telemetry ticks
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/live`;
    let ws = null;

    try {
      ws = new WebSocket(wsUrl);
      ws.onmessage = (event) => {
        try {
          const payload = JSON.parse(event.data);
          if (payload.event === 'TELEMETRY_TICK' || payload.event === 'INITIAL_SNAPSHOT') {
            if (payload.sensors) {
              setSensors(payload.sensors);
            }
          }
        } catch (e) {
          // ignore parsing error
        }
      };
      ws.onerror = () => {
        // Fallback polling if WS unavailable
      };
    } catch (e) {
      console.warn('WS fallback to polling');
    }

    const interval = setInterval(() => {
      fetchSensors().then(setSensors).catch(() => {});
      fetchRoads().then(setRoads).catch(() => {});
    }, 8000);

    return () => {
      if (ws) ws.close();
      clearInterval(interval);
    };
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-amber-500 selection:text-slate-950">
      {/* Top Universal Navbar */}
      <Navbar
        currentLang={currentLang}
        setCurrentLang={setCurrentLang}
        alerts={alerts}
        overview={overview}
      />

      {/* Main Tab Content */}
      <main className="flex-1 w-full relative">
        {loading ? (
          <div className="flex flex-col items-center justify-center h-[calc(100vh-6rem)] space-y-3">
            <div className="w-12 h-12 border-4 border-amber-500 border-t-transparent rounded-full animate-spin"></div>
            <p className="text-sm font-bold text-amber-400">Loading BhooDrishti-NER Geospatial Engine...</p>
          </div>
        ) : (
          <>
            {currentTab === 'map' && (
              <GISMap
                states={states}
                highways={highways}
                sensors={sensors}
                reports={reports}
                resources={resources}
                historical={historical}
                currentLang={currentLang}
              />
            )}

            {currentTab === 'analytics' && (
              <RiskAnalytics currentLang={currentLang} />
            )}

            {currentTab === 'roads' && (
              <RoadConnectivity
                roads={roads}
                onRefresh={loadAllData}
                currentLang={currentLang}
              />
            )}

            {currentTab === 'sensors' && (
              <SensorTelemetry
                sensors={sensors}
                currentLang={currentLang}
              />
            )}

            {currentTab === 'reports' && (
              <FieldReporting
                reports={reports}
                onReportSubmitted={loadAllData}
                currentLang={currentLang}
              />
            )}

            {currentTab === 'alerts' && (
              <AlertBroadcast
                alerts={alerts}
                onAlertBroadcasted={loadAllData}
                currentLang={currentLang}
              />
            )}
          </>
        )}
      </main>
    </div>
  );
}
