"""
BhooDrishti-NER SQLAlchemy ORM Models
All persistent entities for the landslide early warning platform.
"""
import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, Text, DateTime,
    ForeignKey, Index, Enum as SAEnum
)
from sqlalchemy.orm import relationship
from backend.app.database import Base


# ─────────────────────────────────────────────
# Users & Authentication
# ─────────────────────────────────────────────
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), default="")
    role = Column(String(50), default="citizen")  # admin, officer, field_officer, citizen
    state = Column(String(100), default="")
    district = Column(String(100), default="")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))

    reports = relationship("FieldReport", back_populates="reporter")
    audit_logs = relationship("AuditLog", back_populates="user")


# ─────────────────────────────────────────────
# Geographic Entities
# ─────────────────────────────────────────────
class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    location_type = Column(String(50))  # state, district, village, highway_point
    state = Column(String(100), index=True)
    district = Column(String(100))
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    elevation_m = Column(Float)
    slope_deg = Column(Float)
    geology = Column(String(255))
    historical_landslide_density = Column(Float, default=0.0)
    population = Column(Integer, default=0)

    __table_args__ = (
        Index("idx_location_coords", "lat", "lng"),
    )


class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    sensor_type = Column(String(50))  # piezometer, inclinometer, rain_gauge, soil_moisture
    location_name = Column(String(255))
    state = Column(String(100), index=True)
    district = Column(String(100))
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    elevation_m = Column(Float)
    status = Column(String(20), default="NORMAL")  # NORMAL, WATCH, WARNING, CRITICAL
    battery_pct = Column(Float, default=100.0)
    last_reading_at = Column(DateTime)
    installed_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))

    readings = relationship("SensorReading", back_populates="sensor")


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    sensor_db_id = Column(Integer, ForeignKey("sensors.id"), nullable=False, index=True)
    pore_water_pressure_kpa = Column(Float)
    soil_moisture_pct = Column(Float)
    inclinometer_tilt_deg = Column(Float)
    displacement_rate_mm_day = Column(Float)
    rainfall_mm_h = Column(Float)
    acoustic_emission_db = Column(Float)
    temperature_c = Column(Float)
    recorded_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), index=True)

    sensor = relationship("Sensor", back_populates="readings")

    __table_args__ = (
        Index("idx_reading_time", "sensor_db_id", "recorded_at"),
    )


# ─────────────────────────────────────────────
# Field Reports (Crowdsourced)
# ─────────────────────────────────────────────
class FieldReport(Base):
    __tablename__ = "field_reports"

    id = Column(Integer, primary_key=True, index=True)
    reporter_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    reporter_name = Column(String(255), default="Anonymous")
    reporter_role = Column(String(50), default="Citizen")
    hazard_type = Column(String(100), nullable=False)
    state = Column(String(100), index=True)
    district = Column(String(100))
    landmark = Column(String(500))
    description = Column(Text)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    road_passable = Column(Boolean, default=True)
    image_path = Column(String(500))
    status = Column(String(30), default="PENDING")  # PENDING, VERIFIED, DISMISSED
    severity = Column(String(20), default="MODERATE")

    # AI analysis results
    ai_hazard_classification = Column(String(100))
    ai_severity_level = Column(String(20))
    ai_confidence_score = Column(Float)
    ai_crack_width_mm = Column(Float)
    ai_debris_volume = Column(String(50))
    ai_remarks = Column(Text)

    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), index=True)
    verified_at = Column(DateTime)

    reporter = relationship("User", back_populates="reports")

    __table_args__ = (
        Index("idx_report_coords", "lat", "lng"),
    )


# ─────────────────────────────────────────────
# Alerts & Warnings
# ─────────────────────────────────────────────
class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    severity = Column(String(20), nullable=False)  # WATCH, WARNING, EMERGENCY
    category = Column(String(50), default="Landslide")
    location_name = Column(String(255))
    state = Column(String(100), index=True)
    district = Column(String(100))
    lat = Column(Float)
    lng = Column(Float)
    risk_score = Column(Float)
    reason = Column(Text)
    recommended_action = Column(Text)
    source = Column(String(100), default="AI Risk Engine")
    status = Column(String(20), default="ACTIVE")  # ACTIVE, ACKNOWLEDGED, RESOLVED
    
    # Multilingual translations stored as JSON-compatible text
    translations_json = Column(Text)

    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), index=True)
    acknowledged_at = Column(DateTime)
    resolved_at = Column(DateTime)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)


# ─────────────────────────────────────────────
# Roads & Infrastructure
# ─────────────────────────────────────────────
class Road(Base):
    __tablename__ = "roads"

    id = Column(Integer, primary_key=True, index=True)
    corridor_id = Column(String(50), unique=True, nullable=False, index=True)
    highway_name = Column(String(100), nullable=False)
    stretch_name = Column(String(255))
    state = Column(String(100), index=True)
    risk_level = Column(String(20), default="GREEN")  # GREEN, YELLOW, ORANGE, RED
    status = Column(String(50), default="OPEN")
    blockage_cause = Column(Text)
    clearing_eta_hours = Column(Integer, default=0)
    stranded_vehicles_estimate = Column(Integer, default=0)
    alternate_route = Column(Text)
    priority_score = Column(Float, default=0.0)
    last_updated = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_by = Column(String(255))


class Shelter(Base):
    __tablename__ = "shelters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    shelter_type = Column(String(50))  # HOSPITAL, SHELTER, NDRF_BASE, SDRF_BASE
    state = Column(String(100), index=True)
    district = Column(String(100))
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    capacity_persons = Column(Integer, default=0)
    contact = Column(String(100))
    is_operational = Column(Boolean, default=True)


# ─────────────────────────────────────────────
# ML Model Predictions (Audit Trail)
# ─────────────────────────────────────────────
class ModelPrediction(Base):
    __tablename__ = "model_predictions"

    id = Column(Integer, primary_key=True, index=True)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String(20), nullable=False)
    confidence = Column(Float)
    factor_of_safety = Column(Float)
    caine_threshold_ratio = Column(Float)
    dominant_trigger = Column(String(255))
    contributing_factors_json = Column(Text)
    model_version = Column(String(50), default="v1.0")
    computed_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), index=True)


# ─────────────────────────────────────────────
# Audit Log
# ─────────────────────────────────────────────
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)
    entity_type = Column(String(50))
    entity_id = Column(Integer)
    details = Column(Text)
    ip_address = Column(String(45))
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), index=True)

    user = relationship("User", back_populates="audit_logs")
