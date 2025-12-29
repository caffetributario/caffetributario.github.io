# src/backend/services/company_search.py
from typing import Dict, List, Any, Optional
from ..adapters.uk_companies_house import UKCompaniesHouseAdapter
from ..adapters.us_sec_edgar import USSecEdgarAdapter

class CompanySearchOrchestrator:
    """Orchestratore per la ricerca aziende internazionale."""
    
    def __init__(self, uk_api_key: str):
        self.adapters = {
            "UK": UKCompaniesHouseAdapter(uk_api_key),
            "US": USSecEdgarAdapter()
        }
        # Semplice cache in memoria per demo/sessione
        self._cache = {}

    async def search(self, country: str, query: str) -> List[Dict[str, Any]]:
        """Esegue la ricerca tramite l'adapter corrispondente."""
        adapter = self.adapters.get(country)
        if not adapter:
            return []

        # Prova cache (TTL ignorato per semplicità in questa fase)
        cache_key = f"{country}:{query.lower()}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Esecuzione ricerca
        results = await adapter.search(query)
        
        # Salvataggio in cache
        if results:
            self._cache[cache_key] = results
            
        return results
