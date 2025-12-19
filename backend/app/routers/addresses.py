from fastapi import APIRouter, Depends, HTTPException # type: ignore
from sqlalchemy.orm import Session # type: ignore
from typing import List

from ..database import get_db
from ..models import Address
from ..schemas import AddressOut, ProviderResultOut

from ..services.matching import classify_score

router = APIRouter()


@router.get("/addresses", response_model=List[AddressOut])
async def list_addresses(db: Session = Depends(get_db)):
    addrs = db.query(Address).order_by(Address.id.desc()).all()
    out: List[AddressOut] = []
    for a in addrs:
        # determina o melhor resultado
        best = None
        for pr in a.provider_results:
            if not best or (pr.score or 0) >= (best.score or 0):
                best = pr
        out.append(
            AddressOut(
                id=a.id,
                raw_address=a.raw_address,
                normalized_address=a.normalized_address,
                cep=a.cep,
                status=a.status,
                winner_provider=(best.provider_name if best else None),
                best_score=(best.score if best else None),
                results=[
                    ProviderResultOut(
                        provider_name=pr.provider_name,
                        matched_address=pr.matched_address,
                        cep=pr.cep,
                        score=pr.score,
                        extra_metadata=pr.extra_metadata,
                        classification=classify_score(pr.score),
                    )
                    for pr in a.provider_results
                ],
            )
        )
    return out


@router.get("/addresses/{addr_id}", response_model=AddressOut)
async def get_address(addr_id: int, db: Session = Depends(get_db)):
    a = db.query(Address).filter(Address.id == addr_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    best = None
    for pr in a.provider_results:
        if not best or (pr.score or 0) >= (best.score or 0):
            best = pr
    return AddressOut(
        id=a.id,
        raw_address=a.raw_address,
        normalized_address=a.normalized_address,
        cep=a.cep,
        status=a.status,
        winner_provider=(best.provider_name if best else None),
        best_score=(best.score if best else None),
        results=[
            ProviderResultOut(
                provider_name=pr.provider_name,
                matched_address=pr.matched_address,
                cep=pr.cep,
                score=pr.score,
                extra_metadata=pr.extra_metadata,
                classification=classify_score(pr.score),
            )
            for pr in a.provider_results
        ],
    )
