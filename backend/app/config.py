import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./geomatch.db")
API_PROVIDERS = os.getenv("API_PROVIDERS", "local,dummy").split(",")

# Credenciais de provedores de exemplo (definir no arquivo .env)
PROVIDER_A_KEY = os.getenv("PROVIDER_A_KEY")
PROVIDER_B_KEY = os.getenv("PROVIDER_B_KEY")
