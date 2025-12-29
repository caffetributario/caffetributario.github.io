# src/backend/utils/translator.py

STATUS_MAP = {
    "active": "Attiva",
    "dissolved": "Sciolta",
    "liquidation": "In liquidazione",
    "receivership": "In fallimento",
    "administration": "In amministrazione controllata",
    "voluntary-arrangement": "Accordo volontario",
    "converted-closed": "Chiusa (convertita)",
    "insolvency-proceedings": "Procedura di insolvenza",
    "removed": "Rimossa",
    "registered": "Registrata",
    "removed-from-the-register": "Rimossa dal registro",
    "archived": "Archiviata"
}

TYPE_MAP = {
    "ltd": "Società a responsabilità limitata (LTD)",
    "plc": "Società per azioni (PLC)",
    "llp": "Società a responsabilità limitata (LLP)",
    "private-limited-guarant-nsc-limited-exemption": "Società limitata da garanzia",
    "private-limited-guarant-nsc": "Società limitata da garanzia",
    "industrial-and-provident-society": "Società industriale e di previdenza",
    "private-unlimited": "Società privata illimitata",
    "charity": "Ente di beneficenza",
    "community-interest-company": "Società di interesse comunitario",
    "quotata-usa": "Società quotata (USA)",
    "corp": "Corporation (USA)",
    "inc": "Incorporated (USA)"
}

def translate_status(status: str) -> str:
    """Traduce lo stato della società in italiano."""
    if not status: return "N/D"
    return STATUS_MAP.get(status.lower(), f"Altro ({status})")

def translate_type(company_type: str) -> str:
    """Traduce il tipo di società in italiano."""
    if not company_type: return "Altro"
    return TYPE_MAP.get(company_type.lower(), f"Altro ({company_type})")

def format_date_it(date_str: str) -> str:
    """Formatta la data in standard italiano (DD/MM/YYYY)."""
    if not date_str: return "N/D"
    try:
        from datetime import datetime
        # Gestione formati comuni (YYYY-MM-DD)
        if "-" in date_str:
            dt = datetime.strptime(date_str[:10], "%Y-%m-%d")
            return dt.strftime("%d/%m/%Y")
        return date_str
    except:
        return date_str
