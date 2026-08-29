"""
BhooDrishti-NER (भू-दृष्टि) - Platform Launcher
Launches the FastAPI backend and provides unified access to the AI early warning platform.
"""
import sys
import uvicorn
import webbrowser
import time
import threading

def open_browser():
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    print("=" * 70)
    print("  BhooDrishti-NER: Landslide Early Warning & GIS Platform")
    print("  Serving 8 North Eastern States: Sikkim, Assam, Meghalaya,")
    print("  Arunachal Pradesh, Nagaland, Manipur, Mizoram, Tripura")
    print("=" * 70)
    print(">> Starting FastAPI Production Server on http://127.0.0.1:8000")
    print(">> Interactive GIS Dashboard: http://127.0.0.1:8000")
    print(">> API Documentation (Swagger): http://127.0.0.1:8000/docs")
    print(">> CAP 1.2 XML Early Warning Feed: http://127.0.0.1:8000/api/v1/alerts/cap-feed.xml")
    print("=" * 70)
    
    # Auto-open browser in a separate thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=False)

