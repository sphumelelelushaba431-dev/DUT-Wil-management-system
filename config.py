import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'DUT-WIL-TechTitans-Group15-2026-XkQ9#mPz')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///wil.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    
