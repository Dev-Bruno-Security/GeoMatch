import io
import logging
from typing import List, Optional

import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from ..database import get_db, engine, Base
from ..models import Address, ProviderResult, AuditLog
from ..schemas import AddressOut, ProviderResultOut
from ..config import API_PROVIDERS
from ..providers import get_providers
from ..services.matching import normalize_address, classify_score, similarity_score_with_cep
from ..services.parser import read_csv_addresses, parse_sql_addresses
from ..utils.validators import extract_cep, normalize_cep

logger = logging.getLogger("upload")
router = APIRouter()

# Cria tabelas na primeira importação (bootstrap simples)
Base.metadata.create_all(bind=engine)


def _process_addresses(addresses: List[str], db: Session) -> List[AddressOut]:
    providers = get_providers(API_PROVIDERS)
    results_out: List[AddressOut] = []

    for raw_addr in addresses:
        raw_addr = str(raw_addr)
        norm = normalize_address(raw_addr)
        
        # Extrai CEP do endereço de entrada
        input_cep = extract_cep(raw_addr)
        clean_input_cep = normalize_cep(input_cep) if input_cep else None

        addr = Address(
            raw_address=raw_addr, 
            normalized_address=norm,
            cep=clean_input_cep
        )
        db.add(addr)
        db.commit()
        db.refresh(addr)

        provider_results = []
        best_score = 0.0
        winner_provider = None
        for p in providers:
            try:
                r = p.validate(raw_addr)
                
                # Extrai CEP do resultado do provider de forma segura
                provider_cep = None
                if r.get("metadata") and isinstance(r.get("metadata"), dict):
                    provider_cep = r["metadata"].get("cep")
                
                # Recalcula score considerando CEP se disponível
                adjusted_score = similarity_score_with_cep(
                    norm, 
                    normalize_address(r["matched_address"]),
                    clean_input_cep,
                    provider_cep
                )
                
                pr = ProviderResult(
                    address_id=addr.id,
                    provider_name=p.name,
                    matched_address=r["matched_address"],
                    cep=provider_cep,
                    score=adjusted_score,
                    extra_metadata=r.get("metadata"),
                )
                db.add(pr)
                db.commit()
                db.refresh(pr)
                provider_results.append(pr)
                if pr.score >= best_score:
                    best_score = pr.score
                    winner_provider = pr.provider_name
                if pr.score >= 95:
                    break
            except Exception as ex:
                logger.exception("Provedor %s falhou: %s", p.name, ex)
                db.add(AuditLog(event="provider_error", details=f"{p.name}: {ex}"))
                db.commit()
                continue

        addr.status = classify_score(best_score)
        db.commit()

        results_out.append(
            AddressOut(
                id=addr.id,
                raw_address=addr.raw_address,
                normalized_address=addr.normalized_address,
                cep=addr.cep,
                status=addr.status,
                winner_provider=winner_provider,
                best_score=best_score,
                results=[
                    ProviderResultOut(
                        provider_name=pr.provider_name,
                        matched_address=pr.matched_address,
                        cep=pr.cep,
                        score=pr.score,
                        extra_metadata=pr.extra_metadata,
                        classification=classify_score(pr.score),
                    )
                    for pr in provider_results
                ],
            )
        )
    return results_out


@router.post("/upload/csv", response_model=List[AddressOut])
async def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Apenas arquivos .csv são aceitos")
    content = await file.read()
    try:
        addresses = read_csv_addresses(content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    out = _process_addresses(addresses, db)
    db.add(AuditLog(event="upload_csv", details=f"file={file.filename}; rows={len(addresses)}"))
    db.commit()
    return out


@router.post("/upload/sql", response_model=List[AddressOut])
async def upload_sql(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename.lower().endswith(".sql"):
        raise HTTPException(status_code=400, detail="Apenas arquivos .sql são aceitos")
    content = (await file.read()).decode("utf-8", errors="ignore")
    try:
        addresses = parse_sql_addresses(content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    out = _process_addresses(addresses, db)
    db.add(AuditLog(event="upload_sql", details=f"file={file.filename}; rows={len(addresses)}"))
    db.commit()
    return out


@router.post("/upload", response_model=List[AddressOut])
async def upload_auto(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    name = file.filename.lower()
    if name.endswith(".csv"):
        content = await file.read()
        try:
            addresses = read_csv_addresses(content)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        out = _process_addresses(addresses, db)
        db.add(AuditLog(event="upload_csv", details=f"file={file.filename}; rows={len(addresses)}"))
        db.commit()
        return out
    elif name.endswith(".sql"):
        content = (await file.read()).decode("utf-8", errors="ignore")
        try:
            addresses = parse_sql_addresses(content)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        out = _process_addresses(addresses, db)
        db.add(AuditLog(event="upload_sql", details=f"file={file.filename}; rows={len(addresses)}"))
        db.commit()
        return out
    else:
        raise HTTPException(status_code=400, detail="Extensão de arquivo não suportada. Envie .csv ou .sql")
