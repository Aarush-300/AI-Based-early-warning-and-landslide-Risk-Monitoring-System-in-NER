import React, { useState } from 'react';
import { 
  Camera, 
  Upload, 
  MapPin, 
  AlertTriangle, 
  CheckCircle, 
  Eye, 
  Layers, 
  WifiOff, 
  ShieldCheck, 
  Send, 
  FileText, 
  RefreshCw 
} from 'lucide-react';
import { submitFieldReport } from '../services/api';
import { TRANSLATIONS } from '../services/i18n';

export default function FieldReporting({ 
  reports = [], 
  onReportSubmitted = () => {},
  currentLang = 'en' 
}) {
  const t = TRANSLATIONS[currentLang] || TRANSLATIONS.en;

  const [reporterName, setReporterName] = useState('');
  const [reporterRole, setReporterRole] = useState('Citizen');
  const [hazardType, setHazardType] = useState('Tension Cracks');
  const [state, setState] = useState('Meghalaya');
  const [district, setDistrict] = useState('East Jaintia Hills');
  const [landmark, setLandmark] = useState('');
  const [description, setDescription] = useState('');
  const [roadPassable, setRoadPassable] = useState(false);
  const [lat, setLat] = useState(25.1324);
  const [lng, setLng] = useState(92.3682);
  const [imageBase64, setImageBase64] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [submitResult, setSubmitResult] = useState(null);

  const handleGetLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          setLat(pos.coords.latitude);
          setLng(pos.coords.longitude);
        },
        (err) => {
          console.warn('Geolocation denied or unavailable, using fallback coordinates');
        }
      );
    }
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImageBase64(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setSubmitResult(null);

    const payload = {
      reporter_name: reporterName || 'Anonymous Citizen',
      reporter_role: reporterRole,
      hazard_type: hazardType,
      state: state,
      district: district,
      landmark: landmark || `${hazardType} near highway marker`,
      description: description || 'Citizen reported slope hazard.',
      road_passable: roadPassable,
      lat: Number(lat),
      lng: Number(lng),
      image_base64: imageBase64
    };

    try {
      const result = await submitFieldReport(payload);
      setSubmitResult(result);
      onReportSubmitted();
      // Reset optional inputs
      setDescription('');
      setLandmark('');
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-6 space-y-6">
      {/* Header */}
      <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl shadow-xl">
        <div className="flex items-center gap-2 text-amber-400 text-xs font-bold uppercase tracking-widest mb-1">
          <FileText className="h-4 w-4" />
          Citizen & Field Officer Crowdsourced Reporting (Offline-Capable)
        </div>
        <h1 className="text-2xl font-black text-white">
          Geo-Tagged Hazard Reporting & AI Crack Analyzer
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Capture photos of rockfalls, road fractures, or mudslides. Works completely offline in remote hill tracks with local caching.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left 6 Columns: Submission Form */}
        <div className="lg:col-span-6 bg-slate-900/90 border border-slate-800 p-6 rounded-2xl shadow-xl space-y-5">
          <h2 className="text-base font-bold text-white flex items-center gap-2 border-b border-slate-800 pb-3">
            <Camera className="h-5 w-5 text-amber-400" />
            {t.submit_report}
          </h2>

          {submitResult && (
            <div className={`p-4 rounded-xl border ${
              submitResult.offline_cached 
                ? 'bg-amber-950/40 border-amber-800 text-amber-200' 
                : 'bg-emerald-950/40 border-emerald-800 text-emerald-200'
            } text-xs space-y-2`}>
              <div className="flex items-center justify-between font-bold">
                <span className="flex items-center gap-1.5">
                  {submitResult.offline_cached ? <WifiOff className="h-4 w-4 text-amber-400" /> : <CheckCircle className="h-4 w-4 text-emerald-400" />}
                  {submitResult.offline_cached ? 'Saved Locally (Offline Queue)' : 'Report Successfully Logged & Verified!'}
                </span>
                <span className="text-[10px] bg-slate-900 px-2 py-0.5 rounded border border-slate-700">
                  ID: {submitResult.id}
                </span>
              </div>

              {submitResult.ai_analysis && (
                <div className="bg-slate-950/90 p-3 rounded-lg border border-slate-800 space-y-1.5 mt-2">
                  <div className="text-amber-400 font-bold flex items-center gap-1.5">
                    <Eye className="h-3.5 w-3.5" />
                    {t.ai_vision_analysis}: {submitResult.ai_analysis.hazard_classification}
                  </div>
                  <div className="text-slate-300">
                    Severity: <strong className="text-rose-400">{submitResult.ai_analysis.severity_level}</strong> (Confidence: {Math.round(submitResult.ai_analysis.confidence_score * 100)}%)
                  </div>
                  {submitResult.ai_analysis.estimated_crack_width_mm && (
                    <div className="text-slate-400">
                      {t.crack_width}: <strong className="text-amber-300">{submitResult.ai_analysis.estimated_crack_width_mm} mm</strong> • {t.debris_volume}: <strong className="text-cyan-300">{submitResult.ai_analysis.debris_volume_estimate}</strong>
                    </div>
                  )}
                  <p className="text-[11px] text-slate-300 italic pt-1 border-t border-slate-800">
                    "{submitResult.ai_analysis.ai_remarks}"
                  </p>
                </div>
              )}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4 text-xs">
            {/* Reporter info */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="text-slate-300 font-semibold mb-1 block">Your Name / Call-sign:</label>
                <input
                  type="text"
                  placeholder="e.g. John Khasi / Officer Das"
                  value={reporterName}
                  onChange={(e) => setReporterName(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-700 text-white rounded-lg p-2 font-medium"
                />
              </div>

              <div>
                <label className="text-slate-300 font-semibold mb-1 block">Reporter Role:</label>
                <select
                  value={reporterRole}
                  onChange={(e) => setReporterRole(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-700 text-white rounded-lg p-2 font-medium"
                >
                  <option value="Citizen">Citizen Commuter</option>
                  <option value="Field Official">SDMA Field Official</option>
                  <option value="BRO Engineer">Border Roads (BRO) Engineer</option>
                  <option value="Traffic Police">Traffic Police Highway Marshal</option>
                </select>
              </div>
            </div>

            {/* Hazard Type & State */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="text-slate-300 font-semibold mb-1 block">Observed Hazard Type:</label>
                <select
                  value={hazardType}
                  onChange={(e) => setHazardType(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-700 text-white rounded-lg p-2 font-medium"
                >
                  <option value="Tension Cracks">Tension Cracks / Pavement Fissures</option>
                  <option value="Mudslide">Active Mudslide / Debris Flow</option>
                  <option value="Active Rockfall">Active Rockfall / Boulder Detachment</option>
                  <option value="Road Sinking">Road Sinking / Retaining Wall Tilt</option>
                  <option value="Total Road Blockage">Total Road Blockage / Submersion</option>
                </select>
              </div>

              <div>
                <label className="text-slate-300 font-semibold mb-1 block">State:</label>
                <select
                  value={state}
                  onChange={(e) => setState(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-700 text-white rounded-lg p-2 font-medium"
                >
                  <option value="Meghalaya">Meghalaya</option>
                  <option value="Sikkim">Sikkim</option>
                  <option value="Assam">Assam</option>
                  <option value="Nagaland">Nagaland</option>
                  <option value="Arunachal Pradesh">Arunachal Pradesh</option>
                  <option value="Manipur">Manipur</option>
                  <option value="Mizoram">Mizoram</option>
                  <option value="Tripura">Tripura</option>
                </select>
              </div>
            </div>

            {/* Landmark & Coordinates */}
            <div>
              <label className="text-slate-300 font-semibold mb-1 block">Landmark / Highway Stretch / Kilometer Stone:</label>
              <input
                type="text"
                placeholder="e.g. 500m before Sonapur Tunnel, near river bend"
                value={landmark}
                onChange={(e) => setLandmark(e.target.value)}
                required
                className="w-full bg-slate-950 border border-slate-700 text-white rounded-lg p-2 font-medium"
              />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 items-end">
              <div>
                <label className="text-slate-400 text-[11px] mb-1 block">Latitude:</label>
                <input
                  type="number"
                  step="0.0001"
                  value={lat}
                  onChange={(e) => setLat(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-700 text-white rounded-lg p-2"
                />
              </div>
              <div>
                <label className="text-slate-400 text-[11px] mb-1 block">Longitude:</label>
                <input
                  type="number"
                  step="0.0001"
                  value={lng}
                  onChange={(e) => setLng(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-700 text-white rounded-lg p-2"
                />
              </div>
              <button
                type="button"
                onClick={handleGetLocation}
                className="p-2 bg-slate-800 hover:bg-slate-700 text-amber-300 font-semibold rounded-lg border border-slate-700 flex items-center justify-center gap-1 text-[11px]"
              >
                <MapPin className="h-3.5 w-3.5" />
                Auto-GPS
              </button>
            </div>

            {/* Photo Capture & Base64 upload */}
            <div>
              <label className="text-slate-300 font-semibold mb-1 block">Upload Hazard Photo / Live Camera Capture:</label>
              <div className="flex items-center gap-3">
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleImageChange}
                  className="text-xs text-slate-400 file:mr-3 file:py-2 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-amber-500 file:text-slate-950 hover:file:bg-amber-600 cursor-pointer"
                />
              </div>
              {imageBase64 && (
                <div className="mt-2 relative w-full h-40 rounded-lg overflow-hidden border border-slate-700 bg-black">
                  <img src={imageBase64} alt="Upload preview" className="w-full h-full object-cover" />
                  <span className="absolute bottom-2 left-2 bg-black/70 px-2 py-0.5 rounded text-[10px] text-amber-300 font-mono">
                    AI Edge Ready
                  </span>
                </div>
              )}
            </div>

            {/* Road Passable Checkbox */}
            <label className="flex items-center gap-2 cursor-pointer bg-slate-950 p-2.5 rounded-lg border border-slate-800">
              <input
                type="checkbox"
                checked={roadPassable}
                onChange={(e) => setRoadPassable(e.target.checked)}
                className="rounded text-amber-500 focus:ring-0"
              />
              <span className="text-slate-300">Vehicles can still pass through with caution</span>
            </label>

            {/* Description */}
            <div>
              <label className="text-slate-300 font-semibold mb-1 block">Field Description & Observations:</label>
              <textarea
                rows="2"
                placeholder="Describe crack length, falling debris rate, stranded vehicles, or water seepage..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="w-full bg-slate-950 border border-slate-700 text-white rounded-lg p-2 font-medium"
              ></textarea>
            </div>

            <button
              type="submit"
              disabled={submitting}
              className="w-full py-3 bg-gradient-to-r from-amber-500 via-orange-500 to-red-600 hover:brightness-110 disabled:opacity-50 text-slate-950 font-black text-sm rounded-xl shadow-xl transition-all flex items-center justify-center gap-2"
            >
              <Send className="h-4 w-4" />
              {submitting ? 'Transmitting Field Telemetry...' : 'Submit Field Report to Disaster Network'}
            </button>
          </form>
        </div>

        {/* Right 6 Columns: Recent Verified Field Feed */}
        <div className="lg:col-span-6 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <Layers className="h-5 w-5 text-cyan-400" />
              Recent Field Incidents ({reports.length})
            </h2>
            <span className="text-xs text-slate-400">Live Crowdsourced Stream</span>
          </div>

          <div className="space-y-3 max-h-[calc(100vh-16rem)] overflow-y-auto pr-1">
            {reports.map((r) => (
              <div key={r.id} className="bg-slate-900/80 border border-slate-800 p-4 rounded-xl space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-sm text-white">{r.hazard_type}</span>
                    <span className="px-2 py-0.5 text-[10px] bg-slate-800 text-amber-300 rounded font-semibold border border-slate-700">
                      {r.reporter_role}
                    </span>
                  </div>
                  <span className={`px-2 py-0.5 text-[10px] font-bold rounded ${
                    r.status === 'VERIFIED' ? 'bg-emerald-600 text-white' : 'bg-amber-600 text-white'
                  }`}>
                    {r.status}
                  </span>
                </div>

                <div className="text-xs text-slate-300">
                  <span className="font-semibold text-amber-400">{r.landmark}</span> ({r.district}, {r.state})
                </div>

                <p className="text-xs text-slate-400 italic bg-slate-950/60 p-2.5 rounded-lg border border-slate-800">
                  "{r.description}"
                </p>

                {r.ai_analysis && (
                  <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800 text-xs space-y-1">
                    <div className="flex items-center justify-between text-cyan-300 font-bold">
                      <span className="flex items-center gap-1">
                        <Eye className="h-3 w-3" />
                        AI Diagnosis: {r.ai_analysis.hazard_classification}
                      </span>
                      <span className="text-rose-400 font-bold">{r.ai_analysis.severity_level}</span>
                    </div>
                    {r.ai_analysis.estimated_crack_width_mm && (
                      <div className="text-[11px] text-slate-400">
                        Aperture: <strong className="text-white">{r.ai_analysis.estimated_crack_width_mm} mm</strong> • Debris Vol: <strong className="text-amber-400">{r.ai_analysis.debris_volume_estimate}</strong>
                      </div>
                    )}
                  </div>
                )}

                <div className="flex items-center justify-between text-[11px] text-slate-500 pt-2 border-t border-slate-800">
                  <span>Reported by: <strong className="text-slate-300">{r.reporter_name}</strong></span>
                  <span>{new Date(r.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

