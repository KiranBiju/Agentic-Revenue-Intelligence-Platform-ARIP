from dotenv import load_dotenv
import os

load_dotenv()

APP_ENV = os.getenv("APP_ENV", "dev")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./arip.db")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
MAX_OUTREACH = int(os.getenv("MAX_OUTREACH", 60))