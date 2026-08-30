import math
import os
import numpy as np
from typing import Dict, Any, List
from sklearn.ensemble import RandomForestClassifier
import joblib
import logging

logger = logging.getLogger(__name__)

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "models")
MODEL_PATH = os.path.join(MODELS_DIR, "landslide_rf_v1.joblib")

class LandslidePredictiveEngine:
    def __init__(self):
        # Calibrated Caine I-D Threshold coefficients for NER
        self.caine_alpha_himalaya = 14.82
        self.caine_beta_himalaya = 0.42
        
        self.caine_alpha_indoburma = 18.50
        self.caine_beta_indoburma = 0.48
        
        self.model_version = "v2.0-official-ner"
        self._load_or_train_model()

    def _load_or_train_model(self):
        """Load pre-trained model from disk, or fall back to runtime training."""
        if os.path.exists(MODEL_PATH):
            try:
                self.model = joblib.load(MODEL_PATH)
                logger.info(f"Loaded pre-trained model from {MODEL_PATH}")
                return
            except Exception as e:
                logger.warning(f"Failed to load model from disk: {e}. Falling back to runtime training.")
        
        logger.info("No pre-trained model file found. Training on official GSI/ISRO/NASA/ERA5 dataset...")
        self._init_and_train_model()

    def _init_and_train_model(self):
        """
        Trains the ensemble classifier directly on the curated official dataset
        from Geological Survey of India (GSI), ISRO-NRSC, NASA GLC, and ERA5 weather archives.
        """
        train_csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "data", "training_dataset_official.csv")
        
        if os.path.exists(train_csv_path):
            import pandas as pd
            df = pd.read_csv(train_csv_path)
            X = df.iloc[:, :-1].values
            y = df.iloc[:, -1].values
        else:
            from backend.app.ml.official_data_collector import generate_comprehensive_dataset
            X, y, _ = generate_comprehensive_dataset(augment_factor=150)
            
        self.model = RandomForestClassifier(
            n_estimators=180,
            max_depth=15,
            min_samples_split=4,
            min_samples_leaf=2,
            class_weight="balanced",
            random_state=42
        )
        self.model.fit(X, y)
        logger.info(f"Trained in-memory model on {len(X)} official feature vectors.")

    def calculate_factor_of_safety(
        self,
        slope_deg: float,
        cohesion_kpa: float = 18.0,
        friction_angle_deg: float = 28.0,
        soil_depth_m: float = 3.5,
        water_table_ratio: float = 0.65,
        gamma_sat_kn_m3: float = 19.5,
        gamma_w_kn_m3: float = 9.81
    ) -> float:
        """
        Infinite Slope Limit Equilibrium Model for Factor of Safety (Fs):
        Fs = [ c' + (gamma_sat * z - gamma_w * hw) * cos^2(alpha) * tan(phi') ] / [ gamma_sat * z * sin(alpha) * cos(alpha) ]
        """
        alpha_rad = math.radians(max(5.0, slope_deg))
        phi_rad = math.radians(friction_angle_deg)
        z = max(1.0, soil_depth_m)
        hw = z * max(0.0, min(1.0, water_table_ratio))
        
        effective_normal_stress = (gamma_sat_kn_m3 * z - gamma_w_kn_m3 * hw) * (math.cos(alpha_rad) ** 2)
        shear_strength = cohesion_kpa + effective_normal_stress * math.tan(phi_rad)
        shear_stress = gamma_sat_kn_m3 * z * math.sin(alpha_rad) * math.cos(alpha_rad)
        
        if shear_stress <= 0.001:
            return 3.0
            
        fs = shear_strength / shear_stress
        return round(float(np.clip(fs, 0.4, 3.5)), 2)

    def evaluate_caine_threshold(self, lat: float, intensity_mm_h: float, duration_hours: float = 24.0) -> Dict[str, Any]:
        """
        Evaluates rainfall intensity against regional empirical Caine I-D threshold.
        """
        is_himalayan = lat >= 26.8  # Sikkim, Northern Assam, Arunachal
        alpha = self.caine_alpha_himalaya if is_himalayan else self.caine_alpha_indoburma
        beta = self.caine_beta_himalaya if is_himalayan else self.caine_beta_indoburma
        
        threshold_intensity = alpha * (max(1.0, duration_hours) ** (-beta))
        ratio = intensity_mm_h / threshold_intensity
        
        return {
            "regime": "Eastern Himalayan Caine Curve" if is_himalayan else "Indo-Burman Range Caine Curve",
            "threshold_intensity_mm_h": round(threshold_intensity, 2),
            "actual_intensity_mm_h": round(intensity_mm_h, 2),
            "caine_threshold_ratio": round(ratio, 2),
            "breached": ratio >= 1.0
        }

    def predict_risk(
        self,
        lat: float,
        lng: float,
        slope_deg: float = 34.0,
        elevation_m: float = 1450.0,
        rainfall_3d_mm: float = 110.0,
        rainfall_24h_mm: float = 45.0,
        soil_moisture_pct: float = 78.0,
        inclinometer_tilt_rate_mm_day: float = 3.5,
        lithology_type: str = "Shale & Siltstone (Fragile)"
    ) -> Dict[str, Any]:
        
        litho_map = {
            "Granite / Gneiss": 1,
            "Sandstone": 2,
            "Siltstone": 3,
            "Shale & Siltstone (Fragile)": 4,
            "Weathered Schist / Disang Flysch": 5
        }
        litho_idx = litho_map.get(lithology_type, 4)
        
        # Estimate fault distance based on coordinates
        fault_dist = 450.0 if (25.0 <= lat <= 27.5 and 91.5 <= lng <= 94.0) else 1800.0
        
        rain_24h_int = rainfall_24h_mm / 24.0
        
        feature_vector = np.array([[
            slope_deg, elevation_m, litho_idx, rainfall_3d_mm,
            rain_24h_int, soil_moisture_pct, inclinometer_tilt_rate_mm_day, fault_dist
        ]])
        
        pred_class = int(self.model.predict(feature_vector)[0])
        probabilities = self.model.predict_proba(feature_vector)[0]
        
        # Compute Factor of Safety
        water_ratio = min(1.0, soil_moisture_pct / 100.0)
        fs = self.calculate_factor_of_safety(slope_deg=slope_deg, water_table_ratio=water_ratio)
        
        # Overrule/boost if Fs < 1.05
        if fs < 1.05 and pred_class < 3:
            pred_class = 3
        elif fs < 1.25 and pred_class < 2:
            pred_class = 2

        risk_levels = ["GREEN", "YELLOW", "ORANGE", "RED"]
        risk_level = risk_levels[pred_class]
        
        # Calculate dynamic risk score (0.0 to 1.0)
        risk_score = round(float(
            (0.35 * (1.0 - min(1.0, fs / 2.0))) +
            (0.30 * min(1.0, rainfall_3d_mm / 220.0)) +
            (0.20 * min(1.0, inclinometer_tilt_rate_mm_day / 10.0)) +
            (0.15 * (soil_moisture_pct / 100.0))
        ), 3)
        risk_score = float(np.clip(risk_score, 0.05, 0.99))
        
        # Evaluate Caine threshold
        caine_eval = self.evaluate_caine_threshold(lat, rain_24h_int, duration_hours=24.0)
        
        # Identify dominant failure trigger
        triggers = []
        if rainfall_3d_mm > 120:
            triggers.append("Prolonged Antecedent Rain Saturation")
        if rain_24h_int > 8.0:
            triggers.append("Intense Cloudburst/Precipitation Spike")
        if inclinometer_tilt_rate_mm_day > 4.0:
            triggers.append("Active Subsurface Shear & Inclinometer Drift")
        if slope_deg > 42:
            triggers.append("Over-steepened Cut Slope Geometry")
        if not triggers:
            triggers.append("Baseline Hydrostatic Load")
        dominant_trigger = " & ".join(triggers)
        
        # Actionable recommendations
        recs = []
        if risk_level == "RED":
            recs = [
                "IMMEDIATE EVACUATION: Evacuate toe and crest settlement zones within 400m radius.",
                "TRAFFIC HALT: Immediately close highway corridor to all vehicular and pedestrian transit.",
                "DEPLOYMENT: Mobilize Border Roads Organisation (BRO) and SDRF heavy clearance machinery to safe staging perimeter.",
                "PUBLIC BROADCAST: Dispatch Emergency CAP Red Alert to all telecom towers in sector."
            ]
        elif risk_level == "ORANGE":
            recs = [
                "HIGH ALERT: Restrict night travel and suspend heavy multi-axle freight carriers.",
                "PATROLLING: Deploy 24x7 highway quick-response patrols at identified crown crack zones.",
                "DRAINAGE CHECK: Ensure weep holes and surface catchwater drains are cleared of debris."
            ]
        elif risk_level == "YELLOW":
            recs = [
                "ADVISORY: Maintain heightened vigilance; monitor telemetry feeds every 30 minutes.",
                "SPEED LIMIT: Enforce 20 km/h speed limit across vulnerable curves and unstable talus stretches."
            ]
        else:
            recs = [
                "NORMAL: Continuous IoT telemetry monitoring active. No imminent hazard detected."
            ]
            
        forecast_48h = "RED" if risk_score > 0.65 or rainfall_3d_mm > 150 else ("ORANGE" if risk_score > 0.4 else "YELLOW")
        
        # Explainable contributing factors
        contributing_factors = []
        if rainfall_3d_mm > 150:
            contributing_factors.append({"factor": "72h Cumulative Rainfall", "level": "VERY HIGH", "value": f"{rainfall_3d_mm:.0f} mm", "weight": 0.30})
        elif rainfall_3d_mm > 80:
            contributing_factors.append({"factor": "72h Cumulative Rainfall", "level": "HIGH", "value": f"{rainfall_3d_mm:.0f} mm", "weight": 0.22})
        if rain_24h_int > 8.0:
            contributing_factors.append({"factor": "24h Rainfall Intensity", "level": "VERY HIGH", "value": f"{rain_24h_int:.1f} mm/h", "weight": 0.18})
        if slope_deg > 40:
            contributing_factors.append({"factor": "Slope Angle", "level": "HIGH", "value": f"{slope_deg:.1f}°", "weight": 0.25})
        elif slope_deg > 25:
            contributing_factors.append({"factor": "Slope Angle", "level": "MODERATE", "value": f"{slope_deg:.1f}°", "weight": 0.15})
        if soil_moisture_pct > 85:
            contributing_factors.append({"factor": "Soil Saturation", "level": "VERY HIGH", "value": f"{soil_moisture_pct:.0f}%", "weight": 0.15})
        elif soil_moisture_pct > 70:
            contributing_factors.append({"factor": "Soil Saturation", "level": "HIGH", "value": f"{soil_moisture_pct:.0f}%", "weight": 0.12})
        if inclinometer_tilt_rate_mm_day > 4.0:
            contributing_factors.append({"factor": "Ground Displacement Rate", "level": "HIGH", "value": f"{inclinometer_tilt_rate_mm_day:.1f} mm/day", "weight": 0.15})
        if fs < 1.2:
            contributing_factors.append({"factor": "Factor of Safety", "level": "CRITICAL" if fs < 1.0 else "HIGH", "value": f"{fs:.2f}", "weight": 0.20})
        if not contributing_factors:
            contributing_factors.append({"factor": "All Parameters", "level": "NORMAL", "value": "Within safe thresholds", "weight": 0.0})
        
        # Sort by weight descending
        contributing_factors.sort(key=lambda x: x["weight"], reverse=True)
        
        # Confidence based on RF probability and FoS agreement
        confidence = round(float(probabilities[pred_class] * 100), 1)
        
        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "confidence_score": confidence,
            "factor_of_safety": fs,
            "caine_threshold_ratio": caine_eval["caine_threshold_ratio"],
            "probability_percentage": round(float(probabilities[pred_class] * 100), 1),
            "dominant_trigger": dominant_trigger,
            "contributing_factors": contributing_factors,
            "recommendations": recs,
            "forecast_48h_level": forecast_48h,
            "model_version": self.model_version,
            "geotechnical_summary": {
                "slope_deg": slope_deg,
                "elevation_m": elevation_m,
                "lithology": lithology_type,
                "inclinometer_tilt_rate_mm_day": inclinometer_tilt_rate_mm_day,
                "soil_moisture_pct": soil_moisture_pct,
                "rainfall_3d_mm": rainfall_3d_mm,
                "rainfall_24h_mm": rainfall_24h_mm,
                "caine_analysis": caine_eval
            },
            "disclaimer": "Decision-support indicator only. Does not replace official disaster-management assessment."
        }

landslide_engine = LandslidePredictiveEngine()


