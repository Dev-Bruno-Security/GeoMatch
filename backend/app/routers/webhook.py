from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import Address, ProviderResult, AuditLog
from ..providers import get_providers
from ..config import API_PROVIDERS
from ..services.matching import normalize_address, classify_score

router = APIRouter()


@router.post("/webhook/process")
def webhook_process(payload: dict, db: Session = Depends(get_db)):
    """Webhook para ser chamado pelo n8n: espera {"addresses": ["..."]}"""
    addrs: List[str] = payload.get("addresses", [])
    if not isinstance(addrs, list):
        raise HTTPException(status_code=400, detail="O campo 'addresses' deve ser uma lista")

    providers = get_providers(API_PROVIDERS)
    processed = 0

    for raw in addrs:
        norm = normalize_address(str(raw))
        addr = Address(raw_address=str(raw), normalized_address=norm)
        db.add(addr)
        db.commit()
        db.refresh(addr)

        best_score = 0.0
        for p in providers:
            try:
                r = p.validate(raw)
                pr = ProviderResult(
                    address_id=addr.id,
                    provider_name=p.name,
                    matched_address=r["matched_address"],
                    score=r["score"],
                    metadata=r.get("metadata"),
                )
                db.add(pr)
                db.commit()
                if pr.score and pr.score >= best_score:
                    best_score = pr.score
            except Exception as ex:
                db.add(AuditLog(event="provider_error", details=f"{p.name}: {ex}"))
                db.commit()
                continue
        addr.status = classify_score(best_score)
        db.commit()
        processed += 1

    db.add(AuditLog(event="webhook_process", details=f"rows={processed}"))
    db.commit()

    return {"processed": processed}
