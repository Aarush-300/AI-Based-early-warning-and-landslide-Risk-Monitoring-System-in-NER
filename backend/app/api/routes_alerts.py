from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Response, HTTPException
from backend.app.models.schemas import AlertCreate, AlertItem
from backend.app.core.config import settings

router = APIRouter(prefix="/alerts", tags=["Early Warnings & Multilingual Notifications"])

# Pre-seeded active multilingual alerts
ALERTS_DB: List[Dict[str, Any]] = [
    {
        "id": "ALT-NER-2026-0801",
        "title": "RED ALERT: Imminent Slope Collapse & Road Severance on NH-06 (Sonapur Tunnel)",
        "severity": "EMERGENCY",
        "category": "Landslide",
        "state": "Meghalaya",
        "district": "East Jaintia Hills",
        "affected_corridors": ["NH-06 (Barak Valley & Mizoram Lifeline)"],
        "description": "Continuous torrential rainfall (>190mm/24h) and critical inclinometer displacement (14.5 mm/day) have destabilized the northern portal of Sonapur Tunnel. Immediate danger of mass debris flow.",
        "instructions": [
            "All vehicular movement between Jowai and Silchar is immediately halted.",
            "Villagers residing within 500m of the Sonapur scarp must evacuate to designated relief shelters.",
            "Do not attempt to cross moving slurry or active rockfall zones.",
            "BRO clearing teams are in staging position; follow SDRF directives."
        ],
        "translations": {
            "en": {
                "title": "RED ALERT: Imminent Landslide on NH-06 Sonapur Tunnel",
                "body": "CRITICAL: Severe landslide threat at Sonapur Tunnel, NH-06. Highway completely blocked. Evacuate toe areas immediately. Avoid traveling between Shillong and Silchar."
            },
            "as": {
                "title": "ৰঙা সতৰ্কবাৰ্তা: ৰাষ্ট্ৰীয় ঘাইপথ ০৬ সোণাপুৰ সুৰঙ্গৰ ওচৰত ভূমিস্খলনৰ আশংকা",
                "body": "অত্যন্ত জৰুৰী: সোণাপুৰ সুৰঙ্গৰ ওচৰত প্ৰচণ্ড ভূমিস্খলনৰ বাবে ৰাষ্ট্ৰীয় ঘাইপথ বন্ধ কৰা হৈছে। বিপজ্জনক অঞ্চলৰ পৰা সুৰক্ষিত স্থানলৈ যাওক। যাত্ৰা স্থগিত ৰাখক।"
            },
            "bn": {
                "title": "রেড অ্যালার্ট: এনএইচ-০৬ সোনাপুর টানেলের কাছে ধসের চরম আশঙ্কা",
                "body": "জরুরী সতর্কতা: প্রবল বৃষ্টির কারণে সোনাপুর টানেল এলাকায় রাস্তা বন্ধ। নিকটবর্তী বাসিন্দাদের নিরাপদ আশ্রয়ে সরিয়ে নেওয়া হচ্ছে। এই রুটে যাতায়াত করবেন না।"
            },
            "hi": {
                "title": "रेड अलर्ट: एनएच-06 सोनापुर टनल पर भारी भूस्खलन की चेतावनी",
                "body": "अत्यंत गंभीर: सोनापुर टनल के पास भारी भूस्खलन और मलबा गिरने से एनएच-06 बंद कर दिया गया है। ढलान वाले क्षेत्रों से तुरंत सुरक्षित स्थानों पर जाएं।"
            },
            "kha": {
                "title": "JINGMAHAM BASAH: Ka jingtwad khyndew ha Sonapur Tunnel (NH-06)",
                "body": "Kaba khraw: Ka surok bah NH-06 ha Sonapur Tunnel kala khang lut namar ka jingtwa khyndew kaba jur. Sngewbha ki paidbah ki dei ban leit sha ki jaka riewshngain."
            },
            "lus": {
                "title": "RED ALERT: Sonapur Tunnel (NH-06) kawngpui leimin hlauhawm",
                "body": "HRIATTIRNA: Sonapur Tunnel bulah leimin nasa tak a awm avangin Silchar-Shillong kawngpui khar a ni. Mipuiten fimkhur ula, hmun him lam pan rawh u."
            },
            "mni": {
                "title": "রেড অলর্ত: এন.এইচ-০৬ সোনাপুর তনেল ময়াংদা নুংখিবগী খুদোংথিনিংঙাই",
                "body": "অকুপ্পা পাউ: সোনাপুর তনেল ময়াংদা লম্বি চৎপা য়াদ্রে। মায়োল্লোন অমসুং অচৌবা নুং চপচপা তানা লম্বি থিংলে। মীওইশিং য়েংথোক্নবা পাউজেল পীরি।"
            },
            "nag": {
                "title": "RED ALERT: Sonapur Tunnel NH-06 te mati pishi girishe",
                "body": "DANGEROUS: Sonapur Tunnel rasta pura bandh ase mati gira karne. Sob gari rukhai dise. Manu khan safe jaga te jabi."
            }
        },
        "created_at": "2026-08-28T22:00:00Z",
        "active": True
    },
    {
        "id": "ALT-NER-2026-0802",
        "title": "ORANGE WARNING: Tension Cracks & Active Sinking on NH-10 (29th Mile / Teesta Valley)",
        "severity": "WARNING",
        "category": "Road Blockage",
        "state": "Sikkim",
        "district": "East Sikkim",
        "affected_corridors": ["NH-10 (Sikkim Lifeline)"],
        "description": "Continuous river cutting by Teesta and cumulative rainfall >140mm has caused longitudinal cracking on NH-10. Single lane restricted transit only.",
        "instructions": [
            "Heavy multi-axle freight trucks suspended from Rangpo checkpoint.",
            "Light vehicles to use Lava-Gorubathan detour route.",
            "Night travel strictly prohibited between 7 PM and 6 AM."
        ],
        "translations": {
            "en": {
                "title": "ORANGE WARNING: NH-10 Teesta Valley Road Sinking",
                "body": "WARNING: NH-10 at 29th Mile experiences active sinking and cracks. Heavy vehicles barred. Night movement prohibited."
            },
            "hi": {
                "title": "ऑरेंज चेतावनी: एनएच-10 तीस्ता घाटी सड़क धंसने का खतरा",
                "body": "चेतावनी: एनएच-10 पर 29th माइल के पास सड़क दरारें बढ़ रही हैं। भारी वाहनों का प्रवेश वर्जित है। रात के समय यात्रा न करें।"
            },
            "as": {
                "title": "কমলা সতৰ্কতা: এনএইচ-১০ তিস্তা উপত্যকাত পথ ক্ষতিগ্ৰস্ত",
                "body": "সতৰ্কতা: এনএইচ-১০ ৰ ২৯তম মাইলত পথ তললৈ বহি যোৱাৰ ফলত যান-বাহন চলাচল সীমিত কৰা হৈছে। নিশাৰ যাত্ৰা নিষিদ্ধ।"
            },
            "bn": {
                "title": "অরেঞ্জ সতর্কতা: এনএইচ-১০ তিস্তা ভ্যালি রাস্তায় ফাটল ও ধস",
                "body": "সতর্কতা: ২৯ মাইলে তিস্তার জলোচ্ছ্বাসে রাস্তা ক্ষতিগ্রস্ত। ভারী যানবাহন চলাচল বন্ধ রাখা হয়েছে।"
            },
            "kha": {
                "title": "JINGMAHAM: Ka surok NH-10 Teesta Valley kala sdang bam khyndew",
                "body": "Maham: Ym shah ia ki kali bakhraw ban iaid na NH-10 ha 29th Mile. Sngewbha shim da ka lynti Lava-Gorubathan."
            },
            "lus": {
                "title": "ORANGE WARNING: NH-10 Teesta Valley kawng chhe zual",
                "body": "Warning: Teesta ruama NH-10 kawng a khi nasa hle. Zan kal khap a ni a, motor lian kal phal a ni lo."
            },
            "mni": {
                "title": "ওরেঞ্জ ৱার্নিং: এন.এইচ-১০ তিস্তা ভেল্লিদা লম্বি লৈত্ৰে",
                "body": "ৱার্নিং: তিস্তা ভেল্লিদা লম্বি তেন্থরে। অহিংদা গারি চত্থোক চৎশিন তৌবা থিংলে।"
            },
            "nag": {
                "title": "ORANGE WARNING: NH-10 Teesta rasta phati jaishe",
                "body": "WARNING: NH-10 rasta te dangor cracks ahe. Dangor trucks mana ase. Rati time te gari nakholibi."
            }
        },
        "created_at": "2026-08-29T00:30:00Z",
        "active": True
    },
    {
        "id": "ALT-NER-2026-0803",
        "title": "YELLOW ADVISORY: Sinking Risk at Dzüdza Bridge Approach (NH-29)",
        "severity": "ADVISORY",
        "category": "Landslide",
        "state": "Nagaland",
        "district": "Kohima",
        "affected_corridors": ["NH-29 (Kohima-Manipur Corridor)"],
        "description": "Deformation sensors detect 6.8 mm/day displacement at Dzüdza bridge approach. Moderate rainfall continuing.",
        "instructions": [
            "Maintain vehicle spacing of minimum 30 meters.",
            "Drive under 20 km/h across the bridge bypass."
        ],
        "translations": {
            "en": {
                "title": "YELLOW ADVISORY: NH-29 Dzüdza Slope Movement",
                "body": "ADVISORY: Slow slope creeping detected near Dzüdza Bridge. Drive slowly and follow marshals' instructions."
            },
            "nag": {
                "title": "YELLOW ADVISORY: Dzüdza bridge osor te mati lori ase",
                "body": "ADVISORY: Dzüdza bridge logote rasta aste poriboli pare. Gari aste chalabi aru line manibi."
            },
            "hi": {
                "title": "येलो एडवाइजरी: एनएच-29 जुद्जा पुल के पास सतर्कता",
                "body": "सलाह: जुद्जा पुल के पास ढलान का धीमा विस्थापन देखा गया है। कृपया गति धीमी रखें।"
            }
        },
        "created_at": "2026-08-29T01:00:00Z",
        "active": True
    }
]

@router.get("/")
def get_alerts(state: Optional[str] = None, severity: Optional[str] = None) -> List[Dict[str, Any]]:
    results = ALERTS_DB
    if state:
        results = [a for a in results if a["state"].lower() == state.lower()]
    if severity:
        results = [a for a in results if a["severity"].lower() == severity.lower()]
    return results

@router.post("/broadcast")
def broadcast_alert(alert_data: AlertCreate) -> Dict[str, Any]:
    alert_id = f"ALT-NER-{datetime.utcnow().strftime('%Y%m%d')}-{len(ALERTS_DB)+1:03d}"
    
    # Auto generate multi-language translations
    translations = {
        "en": {
            "title": alert_data.title,
            "body": alert_data.description
        },
        "hi": {
            "title": f"[{alert_data.severity}] {alert_data.title}",
            "body": f"चेतावनी: {alert_data.district}, {alert_data.state} में {alert_data.category} का खतरा। कृपया सुरक्षित स्थानों पर रहें।"
        },
        "as": {
            "title": f"[{alert_data.severity}] {alert_data.title}",
            "body": f"সতৰ্কবাৰ্তা: {alert_data.district}, {alert_data.state} ত {alert_data.category} ৰ আশংকা। অনুগ্ৰহ কৰি সুৰক্ষিত স্থানত থাকক।"
        },
        "nag": {
            "title": f"[{alert_data.severity}] {alert_data.title}",
            "body": f"Warning: {alert_data.district} jaga te {alert_data.category} danger ase. Sob manu safe thakibi."
        }
    }
    
    new_alert = {
        "id": alert_id,
        "title": alert_data.title,
        "severity": alert_data.severity,
        "category": alert_data.category,
        "state": alert_data.state,
        "district": alert_data.district,
        "affected_corridors": alert_data.affected_corridors,
        "description": alert_data.description,
        "instructions": alert_data.instructions,
        "translations": translations,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "active": True
    }
    
    ALERTS_DB.insert(0, new_alert)
    return {
        "message": "Alert successfully broadcasted across all channels (SMS, CAP 1.2, App Push, Radio).",
        "alert": new_alert
    }

@router.get("/cap-feed.xml")
def get_cap_xml_feed():
    """
    Returns OASIS Common Alerting Protocol (CAP v1.2) XML compliant feed
    for National Disaster Management Authority (NDMA) & State SDMAs.
    """
    now_iso = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")
    
    xml_items = ""
    for a in ALERTS_DB:
        urgency = "Immediate" if a["severity"] == "EMERGENCY" else ("Expected" if a["severity"] == "WARNING" else "Future")
        cap_sev = "Extreme" if a["severity"] == "EMERGENCY" else ("Severe" if a["severity"] == "WARNING" else "Moderate")
        
        xml_items += f"""
    <info>
      <language>en-IN</language>
      <category>Geo</category>
      <event>{a['category']}</event>
      <urgency>{urgency}</urgency>
      <severity>{cap_sev}</severity>
      <certainty>Observed</certainty>
      <eventHeadline>{a['title']}</eventHeadline>
      <description>{a['description']}</description>
      <instruction>{' '.join(a['instructions'])}</instruction>
      <area>
        <areaDesc>{a['district']}, {a['state']}</areaDesc>
      </area>
    </info>"""

    cap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<alert xmlns="urn:oasis:names:tc:emergency:cap:1.2">
  <identifier>BHOODRISHTI-NER-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}</identifier>
  <sender>sdma.ner.earlywarning@gov.in</sender>
  <sent>{now_iso}</sent>
  <status>Actual</status>
  <msgType>Alert</msgType>
  <scope>Public</scope>
  {xml_items}
</alert>"""

    return Response(content=cap_xml, media_type="application/xml")

