from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class Coordinates(BaseModel):
    lat: float
    lng: float

class LandslideRiskPredictionRequest(BaseModel):
    lat: float
    lng: float
    slope_deg: Optional[float] = None
    elevation_m: Optional[float] = None
    rainfall_3d_mm: Optional[float] = None
    rainfall_24h_mm: Optional[float] = None
    soil_moisture_pct: Optional[float] = None
    inclinometer_tilt_rate_mm_day: Optional[float] = None
    lithology: Optional[str] = "Shale & Siltstone (Fragile)"

class LandslideRiskPredictionResponse(BaseModel):
    risk_score: float = Field(..., description="0.0 to 1.0 risk score")
    risk_level: str = Field(..., description="GREEN, YELLOW, ORANGE, RED")
    factor_of_safety: float
    caine_threshold_ratio: float = Field(..., description="Actual intensity / I-D threshold")
    probability_percentage: float
    dominant_trigger: str
    recommendations: List[str]
    forecast_48h_level: str
    geotechnical_summary: Dict[str, Any]

class SensorTelemetryItem(BaseModel):
    sensor_id: str
    name: str
    location_name: str
    state: str
    district: str
    lat: float
    lng: float
    highway_corridor: Optional[str] = None
    pore_water_pressure_kpa: float
    soil_moisture_pct: float
    inclinometer_tilt_deg: float
    displacement_rate_mm_day: float
    acoustic_emission_db: float
    current_rainfall_mm_h: float
    cumulative_24h_rainfall_mm: float
    status: str  # NORMAL, WATCH, WARNING, CRITICAL
    battery_pct: int
    last_updated: datetime

class FieldReportCreate(BaseModel):
    reporter_name: Optional[str] = "Anonymous Citizen"
    reporter_phone: Optional[str] = None
    reporter_role: str = "Citizen"  # Citizen, Field Official, BRO Engineer, Traffic Police
    lat: float
    lng: float
    landmark: str
    state: str
    district: str
    hazard_type: str  # Tension Cracks, Active Rockfall, Mudslide, Road Sinking, Blockage
    estimated_length_m: Optional[float] = None
    road_passable: bool = False
    description: str
    image_base64: Optional[str] = None
    offline_created_at: Optional[datetime] = None

class VisionAnalysisResult(BaseModel):
    hazard_detected: bool
    hazard_classification: str
    severity_level: str  # LOW, MODERATE, HIGH, CRITICAL
    confidence_score: float
    detected_features: List[str]
    estimated_crack_width_mm: Optional[float] = None
    debris_volume_estimate: Optional[str] = None
    action_priority: str
    ai_remarks: str

class FieldReportResponse(BaseModel):
    id: str
    reporter_name: str
    reporter_role: str
    lat: float
    lng: float
    landmark: str
    state: str
    district: str
    hazard_type: str
    road_passable: bool
    description: str
    image_url: Optional[str] = None
    ai_analysis: Optional[VisionAnalysisResult] = None
    status: str  # VERIFIED, INVESTIGATING, RESOLVED, REJECTED
    created_at: datetime

class RoadBlockageItem(BaseModel):
    corridor_id: str
    highway_name: str
    stretch_name: str
    state: str
    start_point: str
    end_point: str
    status: str  # CLEAR, PARTIALLY_BLOCKED, FULLY_BLOCKED, HIGH_RISK_ADVISORY
    risk_level: str  # GREEN, YELLOW, ORANGE, RED
    blockage_cause: Optional[str] = None
    clearing_eta_hours: Optional[float] = None
    stranded_vehicles_estimate: int = 0
    alternate_route: Optional[str] = None
    alternate_route_extra_km: Optional[float] = None
    alternate_route_extra_hours: Optional[float] = None
    response_priority_score: float  # 0 to 100
    coordinates: List[List[float]]

class AlertCreate(BaseModel):
    title: str
    severity: str
    category: Optional[str] = "Landslide"
    location_name: Optional[str] = None
    state: str
    district: str
    lat: Optional[float] = None
    lng: Optional[float] = None
    risk_score: Optional[float] = None
    reason: Optional[str] = None
    recommended_action: Optional[str] = None
    source: Optional[str] = None
    translations: Optional[Dict[str, Any]] = None
    affected_corridors: Optional[List[str]] = None
    description: Optional[str] = None
    instructions: Optional[List[str]] = None
    expires_at: Optional[datetime] = None

class AlertItem(BaseModel):
    id: str
    title: str
    severity: str
    category: str
    state: str
    district: str
    affected_corridors: List[str]
    description: str
    instructions: List[str]
    translations: Dict[str, Dict[str, str]]
    created_at: datetime
    active: bool = True

class WeatherForecastItem(BaseModel):
    time: str
    rainfall_mm: float
    rainfall_intensity_mm_h: float
    soil_saturation_forecast_pct: float
    predicted_risk_level: str
    wind_speed_kmh: float

