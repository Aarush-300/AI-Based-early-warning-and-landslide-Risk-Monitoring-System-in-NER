from fastapi import APIRouter, Response
from typing import Dict, Any, List
import datetime

router = APIRouter(tags=["Alerts & CAP"])

# Dummy CAP 1.2 Feed
@router.get("/cap-feed.xml", response_class=Response)
def get_cap_feed():
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<alert xmlns="urn:oasis:names:tc:emergency:cap:1.2">
  <identifier>BHOO-NER-2026-08-01</identifier>
  <sender>nodal_agency@bhoodrishti.gov.in</sender>
  <sent>{time}</sent>
  <status>Actual</status>
  <msgType>Alert</msgType>
  <scope>Public</scope>
  <info>
    <category>Geo</category>
    <event>Landslide Warning</event>
    <urgency>Expected</urgency>
    <severity>Severe</severity>
    <certainty>Likely</certainty>
    <headline>High risk of landslide in Sonapur Tunnel Zone</headline>
    <description>Heavy rainfall and increased soil moisture detected. Evacuation recommended.</description>
    <area>
      <areaDesc>NH-06 Sonapur Tunnel, Meghalaya</areaDesc>
      <circle>25.1324,92.3682 8.0</circle>
    </area>
  </info>
</alert>
    """.format(time=datetime.datetime.utcnow().isoformat())
    return Response(content=xml_content, media_type="application/xml")

