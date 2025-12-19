import csv
import io
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse, PlainTextResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Address, ProviderResult

router = APIRouter()


@router.get("/export/csv")
def export_csv(db: Session = Depends(get_db)):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "raw_address", "normalized_address", "status", "provider", "matched_address", "score"])

    q = db.query(Address).all()
    for a in q:
        for pr in a.provider_results:
            writer.writerow([a.id, a.raw_address, a.normalized_address, a.status, pr.provider_name, pr.matched_address, pr.score])

    output.seek(0)
    headers = {"Content-Disposition": "attachment; filename=geomatch_results.csv"}
    return StreamingResponse(iter([output.read()]), media_type="text/csv", headers=headers)


@router.get("/export/sql")
def export_sql(db: Session = Depends(get_db)):
    # Dump simples de inserts SQL para integração
    lines = []
    for a in db.query(Address).all():
        lines.append(
            f"INSERT INTO addresses (id, raw_address, normalized_address, status, created_at) VALUES ({a.id}, '{a.raw_address.replace("'", "''")}', '{a.normalized_address.replace("'", "''")}', '{a.status}', '{a.created_at}');"
        )
        for pr in a.provider_results:
            lines.append(
                f"INSERT INTO provider_results (address_id, provider_name, matched_address, score, created_at) VALUES ({a.id}, '{pr.provider_name}', '{pr.matched_address.replace("'", "''")}', {pr.score}, '{pr.created_at}');"
            )
    sql_text = "\n".join(lines)
    headers = {"Content-Disposition": "attachment; filename=geomatch_results.sql"}
    return PlainTextResponse(sql_text, headers=headers)
