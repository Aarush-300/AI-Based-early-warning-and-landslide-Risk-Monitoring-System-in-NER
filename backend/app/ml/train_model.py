"""
BhooDrishti-NER ML Training Pipeline
Trains a Random Forest classifier on synthetic geotechnical data
and serializes it for production inference.

Usage:
    python -m backend.app.ml.train_model
"""
import os
import json
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score, f1_score
)
import joblib

# Output directory
MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "models")
MODEL_PATH = os.path.join(MODELS_DIR, "landslide_rf_v1.joblib")
METRICS_PATH = os.path.join(MODELS_DIR, "training_metrics.json")


def generate_synthetic_training_data(n_samples: int = 5000, seed: int = 42):
    """
    Generate synthetic but physically calibrated training data for NER landslide prediction.
    
    Feature vector:
        0: Slope angle (degrees) [5-70]
        1: Elevation (meters) [100-4500]
        2: Lithology index [1: Granite/Gneiss, 2: Sandstone, 3: Siltstone, 4: Shale, 5: Weathered Schist]
        3: 3-day cumulative rainfall (mm) [0-500]
        4: 24h peak intensity (mm/h) [0-60]
        5: Soil moisture saturation (%) [20-100]
        6: Inclinometer displacement rate (mm/day) [0-25]
        7: Distance to tectonic fault line (m) [50-5000]
    
    Labels:
        0: GREEN (Safe)
        1: YELLOW (Advisory)
        2: ORANGE (Warning)
        3: RED (Imminent)
    """
    rng = np.random.RandomState(seed)
    
    slopes = rng.uniform(10, 65, n_samples)
    elevations = rng.uniform(200, 3800, n_samples)
    litho = rng.randint(1, 6, n_samples)
    rain_3d = rng.exponential(scale=90, size=n_samples)
    rain_24h_int = rng.exponential(scale=12, size=n_samples)
    soil_moisture = np.clip(rng.normal(65, 18, n_samples), 20, 100)
    disp_rate = rng.exponential(scale=3.5, size=n_samples)
    fault_dist = rng.uniform(50, 4000, n_samples)
    
    X = np.column_stack([
        slopes, elevations, litho, rain_3d, rain_24h_int, 
        soil_moisture, disp_rate, fault_dist
    ])
    
    # Physics-derived failure probability for ground truth
    y = np.zeros(n_samples, dtype=int)
    for i in range(n_samples):
        score = (
            0.25 * (slopes[i] / 50.0) +
            0.15 * (litho[i] / 5.0) +
            0.22 * min(1.0, rain_3d[i] / 250.0) +
            0.18 * min(1.0, rain_24h_int[i] / 35.0) +
            0.12 * (soil_moisture[i] / 100.0) +
            0.15 * min(1.0, disp_rate[i] / 12.0) -
            0.07 * min(1.0, fault_dist[i] / 3000.0)
        )
        
        if score >= 0.72 or disp_rate[i] > 10.0 or (slopes[i] > 40 and rain_3d[i] > 180):
            y[i] = 3  # RED
        elif score >= 0.52 or disp_rate[i] > 5.0 or rain_3d[i] > 120:
            y[i] = 2  # ORANGE
        elif score >= 0.35 or rain_3d[i] > 60:
            y[i] = 1  # YELLOW
        else:
            y[i] = 0  # GREEN
    
    return X, y


def train_and_evaluate():
    """Train, evaluate, and serialize the landslide risk model."""
    print("=" * 60)
    print("BhooDrishti-NER ML Training Pipeline")
    print("=" * 60)
    
    # Generate data
    print("\n[1/5] Generating synthetic training data (5000 samples)...")
    X, y = generate_synthetic_training_data(n_samples=5000)
    
    # Split
    print("[2/5] Splitting train/test (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"  Train: {len(X_train)}, Test: {len(X_test)}")
    print(f"  Class distribution: {dict(zip(*np.unique(y_train, return_counts=True)))}")
    
    # Train
    print("[3/5] Training RandomForestClassifier (150 trees, max_depth=14)...")
    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=14,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    print("[4/5] Evaluating model performance...")
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)
    
    class_names = ["GREEN", "YELLOW", "ORANGE", "RED"]
    report = classification_report(y_test, y_pred, target_names=class_names, output_dict=True)
    cm = confusion_matrix(y_test, y_pred)
    
    # Calculate macro metrics
    f1_macro = f1_score(y_test, y_pred, average='macro')
    try:
        roc_auc = roc_auc_score(y_test, y_proba, multi_class='ovr', average='macro')
    except ValueError:
        roc_auc = 0.0
    
    print(f"\n  Macro F1 Score:  {f1_macro:.4f}")
    print(f"  Macro ROC-AUC:  {roc_auc:.4f}")
    print(f"\n  Confusion Matrix:")
    print(f"  {cm}")
    print(f"\n  Classification Report:")
    print(classification_report(y_test, y_pred, target_names=class_names))
    
    # Feature importance
    feature_names = [
        "slope_deg", "elevation_m", "lithology_idx", "rainfall_3d_mm",
        "rainfall_24h_intensity", "soil_moisture_pct", "displacement_rate", "fault_distance_m"
    ]
    importances = model.feature_importances_
    sorted_idx = np.argsort(importances)[::-1]
    print("  Feature Importance Ranking:")
    for i, idx in enumerate(sorted_idx):
        print(f"    {i+1}. {feature_names[idx]}: {importances[idx]:.4f}")
    
    # Serialize
    print(f"\n[5/5] Saving model to {MODEL_PATH}...")
    os.makedirs(MODELS_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    
    # Save metrics
    metrics = {
        "model_version": "v1.0",
        "algorithm": "RandomForestClassifier",
        "n_estimators": 150,
        "max_depth": 14,
        "training_samples": len(X_train),
        "test_samples": len(X_test),
        "macro_f1": round(f1_macro, 4),
        "macro_roc_auc": round(roc_auc, 4),
        "per_class": {
            name: {
                "precision": round(report[name]["precision"], 4),
                "recall": round(report[name]["recall"], 4),
                "f1": round(report[name]["f1-score"], 4),
                "support": int(report[name]["support"])
            }
            for name in class_names
        },
        "feature_importance": {
            feature_names[idx]: round(float(importances[idx]), 4)
            for idx in sorted_idx
        },
        "disclaimer": "Model trained on synthetic data calibrated to NER geotechnical parameters. Not a substitute for field assessment."
    }
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)
    
    print(f"  Metrics saved to {METRICS_PATH}")
    print(f"\n{'=' * 60}")
    print(f"Training complete. Model saved at: {MODEL_PATH}")
    print(f"{'=' * 60}")
    
    return model, metrics


if __name__ == "__main__":
    train_and_evaluate()
