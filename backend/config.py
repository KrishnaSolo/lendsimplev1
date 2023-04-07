import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "my-secret-key"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Plooto API credentials
    PLOOTO_API_KEY = os.environ.get("PLOOTO_API_KEY")
    PLOOTO_API_SECRET = os.environ.get("PLOOTO_API_SECRET")
    PLOOTO_API_URL = "https://api.plooto.com/api/v2/"

    # Flinks API credentials
    FLINKS_CLIENT_ID = os.environ.get("FLINKS_CLIENT_ID")
    FLINKS_CLIENT_SECRET = os.environ.get("FLINKS_CLIENT_SECRET")
    FLINKS_BASE_URL = "https://sandbox.flinks.io/api/v4/"

    # Google Cloud credentials
    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    CORS_HEADERS = "Content-Type"

    # Other config settings...
