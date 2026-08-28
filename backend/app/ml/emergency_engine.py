from typing import List, Dict, Any
from backend.app.data.ner_geodata import HIGHWAY_CORRIDORS, EMERGENCY_RESOURCES

class EmergencyResponseEngine:
    def __init__(self):
        pass

    def calculate_priority_index(
        self,
        risk_level: str,
        stranded_vehicles: int,
        isolated_settlement_pop: int = 15000,
        is_strategic_lifeline: bool = True,
        hospitals_cut_off: int = 1
    ) -> float:
        """
        Computes multi-criteria Vulnerability & Emergency Response Priority Score (0 - 100).
        """
        sev_weights = {"RED": 40.0, "ORANGE": 25.0, "YELLOW": 12.0, "GREEN": 2.0}
        w_sev = sev_weights.get(risk_level, 10.0)
        
        # Stranded traffic component (up to 20 pts)
        w_traffic = min(20.0, (stranded_vehicles / 200.0) * 20.0)
        
        # Isolated population component (up to 20 pts)
        w_pop = min(20.0, (isolated_settlement_pop / 50000.0) * 20.0)
        
        # Lifeline & hospital cutoff component (up to 20 pts)
        w_infra = (10.0 if is_strategic_lifeline else 2.0) + min(10.0, hospitals_cut_off * 5.0)
        
        total_score = round(min(100.0, w_sev + w_traffic + w_pop + w_infra), 1)
        return total_score

    def get_corridor_recommendations(self, corridor_id: str) -> Dict[str, Any]:
        target = None
        for c in HIGHWAY_CORRIDORS:
            if c["corridor_id"] == corridor_id:
                target = c
                break
                
        if not target:
            return {"error": "Corridor not found"}
            
        priority_score = self.calculate_priority_index(
            risk_level=target["risk_level"],
            stranded_vehicles=target["stranded_vehicles_estimate"],
            is_strategic_lifeline=True
        )
        
        # Determine machinery allocation
        machinery = []
        if target["risk_level"] in ["RED", "ORANGE"]:
            machinery = [
                {"equipment": "Heavy Tracked Excavator (20-Ton)", "quantity": 2, "source_depot": "BRO Taskforce HQ"},
                {"equipment": "Hydraulic Rock Breaker Unit", "quantity": 1, "source_depot": "PWD Mechanical Division"},
                {"equipment": "Wheel Loader / Dozer", "quantity": 2, "source_depot": "NHAI Road Maintenance Unit"},
                {"equipment": "Mobile High-Mast Floodlights & Genset", "quantity": 3, "source_depot": "District Disaster Cell"}
            ]
        else:
            machinery = [
                {"equipment": "Tractor Dozer / Backhoe Loader", "quantity": 1, "source_depot": "Local PWD Sub-division"}
            ]
            
        return {
            "corridor": target,
            "response_priority_score": priority_score,
            "dispatch_urgency": "IMMEDIATE (Tier-1)" if priority_score > 85 else ("HIGH (Tier-2)" if priority_score > 70 else "ROUTINE"),
            "allocated_machinery": machinery,
            "detour_advice": {
                "alternate_route_name": target["alternate_route"],
                "extra_distance_km": target["alternate_route_extra_km"],
                "extra_travel_time_hours": target["alternate_route_extra_hours"],
                "recommended_for": "Light Motor Vehicles & Emergency Ambulances Only" if target["risk_level"] == "RED" else "All Traffic"
            }
        }

emergency_engine = EmergencyResponseEngine()

