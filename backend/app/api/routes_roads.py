from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from backend.app.data.ner_geodata import HIGHWAY_CORRIDORS
from backend.app.ml.emergency_engine import emergency_engine

router = APIRouter(prefix="/roads", tags=["Road Connectivity & Emergency Clearance"])

@router.get("/")
def get_all_corridors() -> List[Dict[str, Any]]:
    # Enrich each corridor with priority scores
    results = []
    for c in HIGHWAY_CORRIDORS:
        priority = emergency_engine.calculate_priority_index(
            risk_level=c["risk_level"],
            stranded_vehicles=c["stranded_vehicles_estimate"]
        )
        results.append({
            **c,
            "calculated_priority_score": priority
        })
    # Sort by priority score descending
    results.sort(key=lambda x: x["calculated_priority_score"], reverse=True)
    return results

@router.get("/{corridor_id}")
def get_corridor_details(corridor_id: str) -> Dict[str, Any]:
    res = emergency_engine.get_corridor_recommendations(corridor_id)
    if "error" in res:
        raise HTTPException(status_code=404, detail="Corridor not found")
    return res

@router.post("/{corridor_id}/update-status")
def update_corridor_status(corridor_id: str, new_status: str, eta_hours: Optional[float] = None, remarks: Optional[str] = None) -> Dict[str, Any]:
    target = None
    for c in HIGHWAY_CORRIDORS:
        if c["corridor_id"] == corridor_id:
            target = c
            break
            
    if not target:
        raise HTTPException(status_code=404, detail="Corridor not found")
        
    target["status"] = new_status
    if eta_hours is not None:
        target["clearing_eta_hours"] = eta_hours
    if remarks:
        target["blockage_cause"] = remarks
        
    return {
        "message": f"Corridor {corridor_id} status successfully updated to {new_status}",
        "corridor": target
    }

