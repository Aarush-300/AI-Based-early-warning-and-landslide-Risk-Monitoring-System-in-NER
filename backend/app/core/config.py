import os
from pydantic import BaseModel

class Settings(BaseModel):
    APP_NAME: str = "BhooDrishti-NER"
    APP_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True
    UPLOAD_DIR: str = os.path.join(os.getcwd(), "uploads")
    DB_PATH: str = os.path.join(os.getcwd(), "bhoodrishti.db")
    
    # Supported North Eastern Region States
    NER_STATES: list[str] = [
        "Sikkim",
        "Assam",
        "Meghalaya",
        "Arunachal Pradesh",
        "Nagaland",
        "Manipur",
        "Mizoram",
        "Tripura"
    ]
    
    # Supported Alert Languages
    LANGUAGES: list[dict] = [
        {"code": "en", "name": "English", "native": "English"},
        {"code": "as", "name": "Assamese", "native": "অসমীয়া"},
        {"code": "bn", "name": "Bengali", "native": "বাংলা"},
        {"code": "hi", "name": "Hindi", "native": "हिन्दी"},
        {"code": "kha", "name": "Khasi", "native": "Ka Ktien Khasi"},
        {"code": "lus", "name": "Mizo", "native": "Mizo tawng"},
        {"code": "mni", "name": "Manipuri", "native": "মৈতৈলোন্"},
        {"code": "nag", "name": "Nagamese", "native": "Nagamese"}
    ]

settings = Settings()
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

