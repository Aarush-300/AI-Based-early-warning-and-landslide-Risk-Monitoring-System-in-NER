"""
TerrainTrace Physical Hardware Datalogger Telemetry Client
Simulates or connects real IoT hardware field stations (Raspberry Pi, ESP32, 4G Cellular Datalogger)
to stream physical in-situ sensor packets directly into TerrainTrace.

Usage:
    python scripts/send_physical_sensor_packet.py --station-id SONAPUR-HW-01 --pwp 135.5 --tilt 4.2
"""
import sys
import argparse
import urllib.request
import json

DEFAULT_SERVER_URL = "http://127.0.0.1:8000/api/v1/sensors/ingest"

def send_sensor_packet(
    station_id: str,
    pwp_kpa: float,
    tilt_deg: float,
    soil_moisture: float,
    rain_rate: float,
    server_url: str = DEFAULT_SERVER_URL
):
    payload = {
        "sensor_id": station_id,
        "pore_water_pressure_kpa": pwp_kpa,
        "inclinometer_tilt_deg": tilt_deg,
        "soil_moisture_pct": soil_moisture,
        "current_rainfall_mm_h": rain_rate,
        "displacement_rate_mm_day": round(tilt_deg * 2.8, 2),
        "acoustic_emission_db": 28.5,
        "battery_pct": 98,
        "temperature_c": 21.5
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        server_url,
        data=data,
        headers={"Content-Type": "application/json", "User-Agent": "TerrainTrace-HardwareLogger/1.0"}
    )
    
    print(f">> Transmitting physical sensor packet for station '{station_id}' to {server_url}...")
    print(f"   • Piezometer Pore Water Pressure : {pwp_kpa} kPa")
    print(f"   • Biaxial Inclinometer Tilt      : {tilt_deg} deg")
    print(f"   • Soil Moisture Saturation       : {soil_moisture}%")
    print(f"   • Rain Gauge Intensity           : {rain_rate} mm/h")
    
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            resp_body = json.loads(response.read().decode("utf-8"))
            print(f"\n[OK] Response from TerrainTrace Server: HTTP {response.status}")
            print(f"     Status: {resp_body.get('status')}")
            print(f"     Evaluated Hazard Level: {resp_body.get('evaluated_status')}")
            print(f"     Data Mode: {resp_body.get('data_mode')}")
            print(">> Telemetry is now live on dashboard and streaming via WebSocket (/ws/live)!")
    except Exception as exc:
        print(f"\n[ERROR] Failed to connect to TerrainTrace gateway: {exc}")
        print("Make sure 'python start_platform.py' is running.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send physical hardware sensor telemetry to TerrainTrace")
    parser.add_argument("--station-id", default="SONAPUR-HW-01", help="Hardware Sensor ID")
    parser.add_argument("--pwp", type=float, default=138.0, help="Pore Water Pressure (kPa)")
    parser.add_argument("--tilt", type=float, default=4.5, help="Inclinometer Tilt (degrees)")
    parser.add_argument("--soil", type=float, default=92.0, help="Soil Moisture Saturation (%)")
    parser.add_argument("--rain", type=float, default=24.0, help="Rainfall Rate (mm/h)")
    parser.add_argument("--url", default=DEFAULT_SERVER_URL, help="TerrainTrace API Endpoint")
    
    args = parser.parse_args()
    send_sensor_packet(
        station_id=args.station_id,
        pwp_kpa=args.pwp,
        tilt_deg=args.tilt,
        soil_moisture=args.soil,
        rain_rate=args.rain,
        server_url=args.url
    )

