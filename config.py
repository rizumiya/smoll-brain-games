# Base Configuration 
from pydantic import BaseModel

class PlayerConfig(BaseModel):
    player_name: str = "Anonymous"
    player_score: int = 0
    player_level: int = 1

class GameHistoryConfig(BaseModel):
    games_played: int = 0
    games_won: int = 0
    games_lost: int = 0
    last_played: str = None  # ISO format date string

class GameSettingsConfig(BaseModel):
    sound_enabled: bool = True
    notifications_enabled: bool = True
    difficulty_level: str = "Medium"  # Options: Easy, Medium, Hard

import os

# Cek file .env untuk konfigurasi yang mungkin ada
ENV_PATH = os.getenv('ENV_PATH', '.env')
if os.path.exists(ENV_PATH):
    from dotenv import load_dotenv
    load_dotenv(ENV_PATH)
else:
    print(f"File .env tidak ditemukan di lokasi: {ENV_PATH}")