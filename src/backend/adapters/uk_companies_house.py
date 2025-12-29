# src/backend/adapters/uk_companies_house.py
import httpx
from typing import Dict, List, Any
from ..utils.translator import translate_status, translate_type, format_date_it

class UKCompaniesHouseAdapter:
    """Adapter per il registro UK (Companies House) con policy 'Zero Leakage'."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.company-information.service.gov.uk"
        #timeout di 10 secondi per resilienza
        self.timeout = httpx.Timeout(10.0, connect=5.0)

    async def search(self, query: str) -> List[Dict[str, Any]]:
        """Esegue la ricerca e normalizza i dati in italiano."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Basic Auth con API Key (senza password)
                auth = httpx.BasicAuth(self.api_key, "")
                response = await client.get(
                    f"{self.base_url}/search/companies",
                    params={"q": query, "items_per_page": 10},
                    auth=auth
                )
                
                if response.status_code != 200:
                    return []
                
                raw_data = response.json()
                return self._normalize(raw_data.get("items", []))
                
        except Exception as e:
            # In caso di errore API, ritorna lista vuota per fallback
            return []

    def _normalize(self, items: List[Dict]) -> List[Dict[str, Any]]:
        """Trasforma i dati grezzi in formato italiano standard 'Zero Leakage'."""
        normalized = []
        for item in items:
            normalized.append({
                "nome": item.get("title", "N/D"),
                "numero_registrazione": item.get("company_number", "N/D"),
                "stato": translate_status(item.get("company_status")),
                "indirizzo_legale": item.get("address_snippet", "N/D"),
                "data_costituzione": format_date_it(item.get("date_of_creation")),
                "tipo_societa": translate_type(item.get("company_type") or "ltd"),
                "paese": "Regno Unito"
                # ZERO LEAKAGE: rimosse source_url, id esterni, link ai bilanci
            })
        return normalized
