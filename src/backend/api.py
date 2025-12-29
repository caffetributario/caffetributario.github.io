# src/backend/api.py
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from .services.company_search import CompanySearchOrchestrator
import os

app = FastAPI(title="Il Caffè Tributario - Enterprise Hub API")

# Setup CORS per permettere al frontend di comunicare con il backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In produzione, restringere al dominio ilcaffetributario.it
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inizializzazione orchestratore
# In produzione: os.getenv("UK_API_KEY")
orchestrator = CompanySearchOrchestrator(uk_api_key="DEMO_KEY")

@app.get("/api/company/search")
async def search_company(
    country: str = Query(..., regex="^(UK|US)$", description="Codice paese (UK o US)"),
    q: str = Query(..., min_length=2, description="Query di ricerca")
):
    """
    Endpoint per la ricerca aziende internazionale.
    Architettura Zero Leakage: ogni dato è normalizzato e tradotto.
    """
    try:
        results = await orchestrator.search(country, q)
        if not results:
            return []
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore interno del server: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Monitoraggio dello stato del sistema."""
    return {"status": "online", "message": "Enterprise Hub Proxy operativo"}

# NEW: PDF Report Endpoint
from fastapi.responses import Response
from .services.pdf_generator import PDFGenerator
import json

pdf_service = PDFGenerator()

@app.post("/api/company/report")
async def generate_report(company_data: dict):
    """
    Genera un report PDF professionale on-the-fly.
    Riceve i dati della società e restituisce un file PDF brandizzato.
    """
    try:
        pdf_content = pdf_service.generate_company_report(company_data)
        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=Report_{company_data.get('numero_registrazione', 'NA')}.pdf"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore generazione PDF: {str(e)}")
