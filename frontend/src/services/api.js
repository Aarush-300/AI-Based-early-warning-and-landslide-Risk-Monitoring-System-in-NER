// API Service & IndexedDB Offline Queue Manager for TerrainTrace

const API_BASE = '/api/v1';

export function getAuthToken() {
  return localStorage.getItem('terraintrace_token') || localStorage.getItem('bhoodrishti_token');
}

export function setAuthToken(token) {
  if (token) {
    localStorage.setItem('terraintrace_token', token);
  } else {
    localStorage.removeItem('terraintrace_token');
    localStorage.removeItem('bhoodrishti_token');
  }
}

export function getCurrentUser() {
  const user = localStorage.getItem('terraintrace_user') || localStorage.getItem('bhoodrishti_user');
  return user ? JSON.parse(user) : null;
}

export function setCurrentUser(user) {
  if (user) {
    localStorage.setItem('terraintrace_user', JSON.stringify(user));
  } else {
    localStorage.removeItem('terraintrace_user');
    localStorage.removeItem('bhoodrishti_user');
  }
}

async function authFetch(url, options = {}) {
  const token = getAuthToken();
  const headers = {
    ...options.headers
  };
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  const response = await fetch(url, { ...options, headers });
  if (response.status === 401) {
    // Handle unauthorized
    setAuthToken(null);
    setCurrentUser(null);
    window.location.hash = '#login'; // Simple client-side routing
  }
  return response;
}

export async function login(username, password) {
  const formData = new URLSearchParams();
  formData.append('username', username);
  formData.append('password', password);
  
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: formData.toString()
  });
  
  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || 'Login failed');
  }
  
  const data = await res.json();
  setAuthToken(data.access_token);
  setCurrentUser(data.user);
  return data.user;
}

export async function registerAccount(account) {
  const res = await fetch(`${API_BASE}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(account)
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({}));
    throw new Error(error.detail || 'Unable to create your account');
  }

  const data = await res.json();
  setAuthToken(data.access_token);
  setCurrentUser(data.user);
  return data.user;
}

export function logout() {
  setAuthToken(null);
  setCurrentUser(null);
}

// ---------------- IndexedDB Offline Vault ----------------
const DB_NAME = 'terraintrace_offline_vault';
const DB_VERSION = 1;
const STORE_REPORTS = 'pending_field_reports';

function openOfflineDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, DB_VERSION);
    request.onupgradeneeded = (e) => {
      const db = e.target.result;
      if (!db.objectStoreNames.contains(STORE_REPORTS)) {
        db.createObjectStore(STORE_REPORTS, { keyPath: 'local_id', autoIncrement: true });
      }
    };
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

export const OfflineVault = {
  async saveReport(report) {
    const db = await openOfflineDB();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(STORE_REPORTS, 'readwrite');
      const store = tx.objectStore(STORE_REPORTS);
      const record = {
        ...report,
        offline_created_at: new Date().toISOString()
      };
      const req = store.add(record);
      req.onsuccess = () => resolve(req.result);
      req.onerror = () => reject(req.error);
    });
  },

  async getAllPendingReports() {
    const db = await openOfflineDB();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(STORE_REPORTS, 'readonly');
      const store = tx.objectStore(STORE_REPORTS);
      const req = store.getAll();
      req.onsuccess = () => resolve(req.result || []);
      req.onerror = () => reject(req.error);
    });
  },

  async clearPendingReports() {
    const db = await openOfflineDB();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(STORE_REPORTS, 'readwrite');
      const store = tx.objectStore(STORE_REPORTS);
      const req = store.clear();
      req.onsuccess = () => resolve(true);
      req.onerror = () => reject(req.error);
    });
  }
};

// ---------------- API Calls ----------------
export async function fetchOverview() {
  const res = await fetch(`${API_BASE}/predict/overview`);
  if (!res.ok) throw new Error('Failed to fetch regional overview');
  return res.json();
}

export async function fetchStates() {
  const res = await fetch(`${API_BASE}/gis/states`);
  if (!res.ok) throw new Error('Failed to fetch NER states');
  return res.json();
}

export async function fetchHighways() {
  const res = await authFetch(`${API_BASE}/gis/highways`);
  if (!res.ok) throw new Error('Failed to fetch highways');
  return res.json();
}

export async function fetchSensors() {
  const res = await authFetch(`${API_BASE}/gis/sensors`);
  if (!res.ok) throw new Error('Failed to fetch sensors');
  return res.json();
}

export async function fetchHeatmap() {
  const res = await authFetch(`${API_BASE}/gis/risk-heatmap`);
  if (!res.ok) throw new Error('Failed to fetch heatmap points');
  return res.json();
}

export async function fetchHistoricalLandslides() {
  const res = await authFetch(`${API_BASE}/gis/historical`);
  if (!res.ok) throw new Error('Failed to fetch historical landslides');
  return res.json();
}

export async function fetchEmergencyResources() {
  const res = await authFetch(`${API_BASE}/gis/resources`);
  if (!res.ok) throw new Error('Failed to fetch emergency resources');
  return res.json();
}

export async function predictRisk(params) {
  const res = await authFetch(`${API_BASE}/predict/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params)
  });
  if (!res.ok) throw new Error('Failed to predict risk');
  return res.json();
}

export async function fetchWeatherForecast(lat, lng, locationName) {
  const res = await authFetch(`${API_BASE}/predict/weather-forecast?lat=${lat}&lng=${lng}&location_name=${encodeURIComponent(locationName || '')}`);
  if (!res.ok) throw new Error('Failed to fetch weather forecast');
  return res.json();
}

export async function fetchReports(filters = {}) {
  const query = new URLSearchParams(filters).toString();
  const res = await authFetch(`${API_BASE}/reports/${query ? `?${query}` : ''}`);
  if (!res.ok) throw new Error('Failed to fetch field reports');
  return res.json();
}

export async function submitFieldReport(reportData) {
  try {
    const res = await authFetch(`${API_BASE}/reports/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(reportData)
    });
    if (!res.ok) throw new Error('Server returned error');
    return await res.json();
  } catch (err) {
    // If network fails, save to offline IndexedDB
    console.warn('Network unavailable, caching report locally to IndexedDB:', err);
    await OfflineVault.saveReport(reportData);
    return {
      id: `LOCAL-OFFLINE-${Date.now()}`,
      offline_cached: true,
      hazard_type: reportData.hazard_type,
      landmark: reportData.landmark,
      status: 'OFFLINE_PENDING_SYNC',
      ai_analysis: {
        hazard_detected: true,
        hazard_classification: reportData.hazard_type,
        severity_level: 'HIGH',
        confidence_score: 0.85,
        detected_features: ['Saved in offline queue', 'Will be analyzed by Cloud AI upon reconnection'],
        estimated_crack_width_mm: 25.0,
        debris_volume_estimate: 'Pending cloud verification',
        action_priority: 'OFFLINE_CACHED',
        ai_remarks: 'Your report and photo have been safely recorded in your device memory. They will automatically sync when network is restored.'
      }
    };
  }
}

export async function syncPendingOfflineReports() {
  const pending = await OfflineVault.getAllPendingReports();
  if (pending.length === 0) return { synced_count: 0 };
  
  const res = await authFetch(`${API_BASE}/reports/sync-offline`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(pending)
  });
  if (res.ok) {
    await OfflineVault.clearPendingReports();
    return res.json();
  }
  throw new Error('Failed to synchronize offline reports');
}

export async function fetchAlerts(filters = {}) {
  const query = new URLSearchParams(filters).toString();
  const res = await authFetch(`${API_BASE}/alerts/${query ? `?${query}` : ''}`);
  if (!res.ok) throw new Error('Failed to fetch alerts');
  return res.json();
}

export async function broadcastAlert(alertData) {
  const res = await authFetch(`${API_BASE}/alerts/broadcast`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(alertData)
  });
  if (!res.ok) throw new Error('Failed to broadcast alert');
  return res.json();
}

export async function fetchRoads() {
  const res = await authFetch(`${API_BASE}/roads/`);
  if (!res.ok) throw new Error('Failed to fetch roads');
  return res.json();
}

export async function updateRoadStatus(corridorId, newStatus, etaHours, remarks) {
  const res = await authFetch(`${API_BASE}/roads/${corridorId}/update-status?new_status=${newStatus}&eta_hours=${etaHours || ''}&remarks=${encodeURIComponent(remarks || '')}`, {
    method: 'POST'
  });
  if (!res.ok) throw new Error('Failed to update road status');
  return res.json();
}
