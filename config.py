# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # File Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'temp'
    
    # Evaluation Weights
    CORRECTNESS_WEIGHT = 0.3
    QUALITY_WEIGHT = 0.25
    EFFICIENCY_WEIGHT = 0.2
    READABILITY_WEIGHT = 0.15
    EDGE_CASES_WEIGHT = 0.1
    
    # Scoring Thresholds
    EXCELLENT_THRESHOLD = 90
    GOOD_THRESHOLD = 75
    FAIR_THRESHOLD = 60
