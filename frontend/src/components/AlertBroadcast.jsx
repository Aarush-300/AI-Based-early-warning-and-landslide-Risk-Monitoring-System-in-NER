import React, { useState } from 'react';
import { 
  Bell, 
  Volume2, 
  VolumeX, 
  Globe, 
  Radio, 
  FileCode, 
  Send, 
  CheckCircle, 
  ShieldAlert, 
  ExternalLink 
} from 'lucide-react';
import { broadcastAlert } from '../services/api';
import { LANGUAGES, TRANSLATIONS } from '../services/i18n';

export default function AlertBroadcast({ 
  alerts = [], 
  onAlertBroadcasted = () => {},
  currentLang = 'en' 
}) {
  const t = TRANSLATIONS[currentLang] || TRANSLATIONS.en;

  const [activeAlertLang, setActiveAlertLang] = useState(currentLang);
  const [playingAudioId, setPlayingAudioId] = useState(null);

  // Broadcast Form state
  const [title, setTitle] = useState('');
  const [severity, setSeverity] = useState('EMERGENCY');
  const [category, setCategory] = useState('Landslide');
  const [state, setState] = useState('Meghalaya');
  const [district, setDistrict] = useState('East Jaintia Hills');
  const [corridor, setCorridor] = useState('NH-06 (Sonapur Tunnel)');
  const [description, setDescription] = useState('');
  const [instructions, setInstructions] = useState('');
  const [broadcasting, setBroadcasting] = useState(false);
  const [broadcastSuccess, setBroadcastSuccess] = useState(null);

  const handleSpeakAlert = (alert) => {
    if (!window.speechSynthesis) {
      alert('Speech synthesis not supported on this browser.');
      return;
    }

    if (playingAudioId === alert.id) {
      window.speechSynthesis.cancel();
      setPlayingAudioId(null);
      return;
    }

    window.speechSynthesis.cancel();
    const trans = alert.translations?.[activeAlertLang] || { title: alert.title, body: alert.description };
    const textToSpeak = `${trans.title}. ${trans.body}`;

    const utterance = new SpeechSynthesisUtterance(textToSpeak);
    // Select language voice code
    const langVoiceMap = {
      en: 'en-IN',
      hi: 'hi-IN',
      bn: 'bn-IN',
      as: 'as-IN'
    };
    utterance.lang = langVoiceMap[activeAlertLang] || 'en-IN';
    utterance.rate = 0.95;

    utterance.onend = () => setPlayingAudioId(null);
    utterance.onerror = () => setPlayingAudioId(null);

    setPlayingAudioId(alert.id);
    window.speechSynthesis.speak(utterance);
  };

  const handleBroadcast = async (e) => {
    e.preventDefault();
    setBroadcasting(true);
    setBroadcastSuccess(null);

    const instrList = instructions
      ? instructions.split('\n').filter(i => i.trim())
      : ['Evacuate immediate slope toe zones.', 'Follow SDMA police directives.'];

    try {
      const res = await broadcastAlert({
        title,
        severity,
        category,
        state,
        district,
        affected_corridors: [corridor],
        description,
        instructions: instrList
      });
      setBroadcastSuccess(res.message);
      onAlertBroadcasted();
      setTitle('');
      setDescription('');
      setInstructions('');
    } catch (err) {
      console.error(err);
    } finally {
      setBroadcasting(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-6 space-y-6">
      {/* Header */}
      <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-red-400 text-xs font-bold uppercase tracking-widest mb-1">
            <Bell className="h-4 w-4 animate-bounce" />
            National Emergency Early Warning & Alert Broadcasting Center
          </div>
          <h1 className="text-2xl font-black text-white">
            Multilingual Early Warnings & Common Alerting Protocol (CAP 1.2)
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Real-time public warnings with text-to-speech audio in 8 North Eastern dialects, SMS gateway integration, and OASIS CAP feeds.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <a
            href="/api/v1/alerts/cap-feed.xml"
            target="_blank"
            rel="noreferrer"
            className="flex items-center gap-1.5 px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-amber-300 text-xs font-bold rounded-xl border border-slate-700 transition-all shadow-md"
          >
            <FileCode className="h-4 w-4" />
            <span>OASIS CAP 1.2 XML Feed</span>
            <ExternalLink className="h-3 w-3 ml-1 opacity-70" />
          </a>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left 7 Columns: Active Alerts Feed & Multilingual Player */}
        <div className="lg:col-span-7 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <ShieldAlert className="h-5 w-5 text-red-500" />
              Active Early Warnings ({alerts.length})
            </h2>

            {/* Language Switcher for Alerts */}
            <div className="flex items-center gap-1.5 bg-slate-900 px-2.5 py-1 rounded-lg border border-slate-800 text-xs text-slate-300">
              <Globe className="h-3.5 w-3.5 text-amber-400" />
              <span className="text-[11px] text-slate-400 font-medium">Dialect:</span>
              <select
                value={activeAlertLang}
                onChange={(e) => setActiveAlertLang(e.target.value)}
                aria-label="Select Alert Dialect"
                className="bg-transparent border-none text-amber-300 font-semibold focus:outline-none cursor-pointer"
              >
                {LANGUAGES.map(l => (
                  <option key={l.code} value={l.code} className="bg-slate-900 text-white">
                    {l.native}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="space-y-4">
            {alerts.map((alert) => {
              const trans = alert.translations?.[activeAlertLang] || { title: alert.title, body: alert.description };
              const isPlaying = playingAudioId === alert.id;

              return (
                <div
                  key={alert.id}
                  className={`p-5 rounded-2xl border ${
                    alert.severity === 'EMERGENCY'
                      ? 'bg-red-950/30 border-red-800/80 shadow-lg shadow-red-900/20'
                      : alert.severity === 'WARNING'
                      ? 'bg-orange-950/30 border-orange-800/80 shadow-lg shadow-orange-900/20'
                      : 'bg-amber-950/30 border-amber-800/80'
                  } space-y-3`}
                >
                  <div className="flex items-center justify-between gap-2">
                    <span className={`px-2.5 py-0.5 text-xs font-black rounded ${
                      alert.severity === 'EMERGENCY' ? 'bg-red-600 text-white animate-pulse' :
                      alert.severity === 'WARNING' ? 'bg-orange-600 text-white' : 'bg-amber-500 text-slate-950 font-bold'
                    }`}>
                      {alert.severity} ALERT
                    </span>
                    <span className="text-[11px] text-slate-400 font-mono">
                      {alert.district}, {alert.state}
                    </span>
                  </div>

                  <div>
                    <h3 className="text-base font-bold text-white leading-snug">
                      {trans.title}
                    </h3>
                    <p className="text-xs text-slate-300 mt-1 leading-relaxed">
                      {trans.body}
                    </p>
                  </div>

                  {/* Directives list */}
                  {alert.instructions && alert.instructions.length > 0 && (
                    <div className="bg-black/30 p-3 rounded-xl border border-slate-800 text-xs space-y-1">
                      <span className="font-bold text-amber-300">Public Safety Directives:</span>
                      <ul className="list-disc list-inside space-y-0.5 text-slate-300">
                        {alert.instructions.map((ins, idx) => (
                          <li key={idx}>{ins}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  <div className="flex items-center justify-between pt-2 border-t border-slate-800 text-xs">
                    <span className="text-slate-400 text-[11px]">
                      Dispatched: {new Date(alert.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>

                    {/* Speech Synthesis Audio Button */}
                    <button
                      onClick={() => handleSpeakAlert(alert)}
                      className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                        isPlaying
                          ? 'bg-red-600 text-white animate-pulse'
                          : 'bg-slate-800 hover:bg-slate-700 text-amber-300 border border-slate-700'
                      }`}
                    >
                      {isPlaying ? <VolumeX className="h-3.5 w-3.5" /> : <Volume2 className="h-3.5 w-3.5" />}
                      <span>{isPlaying ? 'Stop Audio' : t.listen_audio}</span>
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right 5 Columns: Authority Alert Broadcasting Terminal */}
        <div className="lg:col-span-5 bg-slate-900/90 border border-slate-800 p-6 rounded-2xl shadow-xl space-y-5">
          <div className="border-b border-slate-800 pb-3">
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <Radio className="h-5 w-5 text-amber-400" />
              {t.broadcast_alert}
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">
              Authorized for SDMA, BRO & District Disaster Authorities.
            </p>
          </div>

          {broadcastSuccess && (
            <div className="p-3 rounded-xl bg-emerald-950/60 border border-emerald-800 text-emerald-300 text-xs font-semibold flex items-center gap-2">
              <CheckCircle className="h-4 w-4" />
              <span>{broadcastSuccess}</span>
            </div>
          )}

          <form onSubmit={handleBroadcast} className="space-y-4 text-xs">
            <div>
              <label className="text-slate-300 font-semibold mb-1 block">Alert Headline:</label>
              <input
                type="text"
                placeholder="e.g. FLASH FLOOD & ROCKFALL HAZARD ON NH-10"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
                className="w-full bg-slate-950 border border-slate-700 text-white rounded-lg p-2 font-medium"
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-slate-300 font-semibold mb-1 block">Severity Level:</label>
                <select
                  value={severity}
                  onChange={(e) => setSeverity(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-700 text-white rounded-lg p-2 font-medium"
                >
                  <option value="EMERGENCY">EMERGENCY (Red)</option>
                  <option value="WARNING">WARNING (Orange)</option>
                  <option value="ADVISORY">ADVISORY (Yellow)</option>
                </select>
              </div>

              <div>
                <label className="text-slate-300 font-semibold mb-1 block">Category:</label>
                <select
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-700 text-white rounded-lg p-2 font-medium"
                >
                  <option value="Landslide">Landslide & Slope Collapse</option>
                  <option value="Mudflow">Debris / Mudflow</option>
                  <option value="Road Blockage">Highway Blockage</option>
                  <option value="Flash Flood">Flash Flood & River Swell</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
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

              <div>
                <label className="text-slate-300 font-semibold mb-1 block">District:</label>
                <input
                  type="text"
                  placeholder="e.g. East Khasi Hills"
                  value={district}
                  onChange={(e) => setDistrict(e.target.value)}
                  required
                  className="w-full bg-slate-950 border border-slate-700 text-white rounded-lg p-2 font-medium"
                />
              </div>
            </div>

            <div>
              <label className="text-slate-300 font-semibold mb-1 block">Affected Strategic Highway Corridor:</label>
              <input
                type="text"
                placeholder="e.g. NH-06 Shillong-Silchar"
                value={corridor}
                onChange={(e) => setCorridor(e.target.value)}
                className="w-full bg-slate-950 border border-slate-700 text-white rounded-lg p-2 font-medium"
              />
            </div>

            <div>
              <label className="text-slate-300 font-semibold mb-1 block">Alert Description & Meteorological Context:</label>
              <textarea
                rows="2"
                placeholder="Details on rainfall intensity, slope movement, and imminent danger..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                required
                className="w-full bg-slate-950 border border-slate-700 text-white rounded-lg p-2 font-medium"
              ></textarea>
            </div>

            <div>
              <label className="text-slate-300 font-semibold mb-1 block">Instructions & Evacuation Directives (1 per line):</label>
              <textarea
                rows="2"
                placeholder="1. Halt all vehicle movement&#10;2. Evacuate 400m from slope toe"
                value={instructions}
                onChange={(e) => setInstructions(e.target.value)}
                className="w-full bg-slate-950 border border-slate-700 text-white rounded-lg p-2 font-medium"
              ></textarea>
            </div>

            <button
              type="submit"
              disabled={broadcasting}
              className="w-full py-3 bg-gradient-to-r from-red-600 via-rose-600 to-red-700 hover:brightness-110 disabled:opacity-50 text-white font-black text-sm rounded-xl shadow-xl transition-all flex items-center justify-center gap-2"
            >
              <Send className="h-4 w-4" />
              {broadcasting ? 'Transmitting CAP & Multilingual Alerts...' : 'Broadcast Multi-Channel Emergency Warning'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
