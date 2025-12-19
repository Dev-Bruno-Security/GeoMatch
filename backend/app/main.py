from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import upload, export, webhook, addresses
from .logging_config import setup_logging

setup_logging()

app = FastAPI(title="GeoMatch Backend", version="0.1.0")

# CORS para frontend local (porta padrão do Vite: 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ajustar para origens específicas em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(export.router, prefix="/api", tags=["export"])
app.include_router(webhook.router, prefix="/api", tags=["webhook"]) 
app.include_router(addresses.router, prefix="/api", tags=["addresses"]) 


@app.get("/api/health")
async def health():
    return {"status": "ok"}
