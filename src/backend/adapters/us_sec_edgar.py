# src/backend/adapters/us_sec_edgar.py
import httpx
import json
from typing import Dict, List, Any
from ..utils.translator import translate_type

class USSecEdgarAdapter:
    """Adapter per SEC EDGAR (USA) con policy 'Zero Leakage'."""
    
    def __init__(self):
        self.base_url = "https://www.sec.gov"
        self.data_url = "https://data.sec.gov"
        # SEC richiede User-Agent specifico
        self.headers = {
            "User-Agent": "IlCaffeTributario/1.0 (contact@ilcaffetributario.it)",
            "Accept-Encoding": "gzip, deflate"
        }
        self.timeout = httpx.Timeout(10.0, connect=5.0)

    async def search(self, query: str) -> List[Dict[str, Any]]:
        """Esegue la ricerca tramite indice pubblico SEC."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout, headers=self.headers) as client:
                # 1. Recupera indice tickers/nomi
                response = await client.get(f"{self.base_url}/files/company_tickers.json")
                if response.status_code != 200:
                    return []
                
                all_companies = response.json()
                query_lower = query.lower()
                
                # 2. Filtra per nome o ticker
                matches = []
                for key, val in all_companies.items():
                    title = val.get("title", "").lower()
                    ticker = val.get("ticker", "").lower()
                    
                    if query_lower in title or query_lower in ticker:
                        matches.append(val)
                        if len(matches) >= 10: break
                
                return self._normalize(matches)
                
        except Exception:
            return []

    def _normalize(self, items: List[Dict]) -> List[Dict[str, Any]]:
        """Trasforma i dati SEC in formato italiano 'Zero Leakage'."""
        normalized = []
        for item in items:
            # CIK deve essere di 10 cifre
            cik = str(item.get("cik_str", "N/D")).zfill(10)
            normalized.append({
                "nome": item.get("title", "N/D"),
                "numero_registrazione": f"CIK-{cik}",
                "stato": "Attiva (Quotata USA)", 
                "indirizzo_legale": "Sede legale USA (disponibile via filing 10-K)",
                "data_costituzione": "N/D (Vedi atti costitutivi USA)",
                "tipo_societa": translate_type("quotata-usa"),
                "paese": "Stati Uniti"
            })
        return normalized
