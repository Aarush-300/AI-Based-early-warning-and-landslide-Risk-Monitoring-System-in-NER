"""
TerrainTrace-NER - Platform Launcher
Automatically boots the FastAPI server + Serves the React GIS SPA
and launches your default browser.
"""
import os
import sys
import time
import webbrowser
import threading
import uvicorn

def open_browser():
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    print("=" * 70)
    print("  TerrainTrace-NER: Landslide Early Warning & GIS Platform")
    print("  Smart India Hackathon 2026 Prototype")
    print("=" * 70)
    print("  Starting unified backend & dashboard on http://127.0.0.1:8000")
    print("  CAP 1.2 Feed available at: http://127.0.0.1:8000/api/v1/alerts/cap-feed.xml")
    print("=" * 70)
    print(">> Starting FastAPI Production Server on http://127.0.0.1:8000")
    print(">> Interactive GIS Dashboard: http://127.0.0.1:8000")
    print(">> API Documentation (Swagger): http://127.0.0.1:8000/docs")
    print(">> CAP 1.2 XML Early Warning Feed: http://127.0.0.1:8000/api/v1/alerts/cap-feed.xml")
    print("=" * 70)
    
    # Auto-open browser in a separate thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=False)

