"""
World Bank Data Router — Direct consumption of World Bank Data API v2.
Provides global economic, energy and CO2 comparative analytics.
"""
import httpx
from fastapi import APIRouter, HTTPException, Query
from core.cache import cached

router = APIRouter(prefix="/api/worldbank", tags=["World Bank"])

BASE_URL = "https://api.worldbank.org/v2"

# Popular energy/climate indicators
INDICATORS = {
    "co2_emissions": "EN.ATM.CO2E.PC", # Metric tons per capita
    "renewable_energy": "EG.FEC.RNEW.ZS", # % of total final energy consumption
    "gdp_growth": "NY.GDP.MKTP.KD.ZG", # Annual %
    "energy_use": "EG.USE.PCAP.KG.OE", # kg of oil equivalent per capita
}

@router.get("/indicators")
async def get_tracked_indicators():
    """List pre-configured popular World Bank indicators."""
    return INDICATORS

@router.get("/fetch/{indicator_key}")
@cached(ttl=86400, key_prefix="worldbank")
async def fetch_data(
    indicator_key: str, 
    country: str = Query("BRA", description="ISO3 Country Code, default Brazil"),
    date: str = Query("2015:2024", description="Date range YYYY:YYYY")
):
    """Query the World Bank API for specific country indicator."""
    ind_code = INDICATORS.get(indicator_key, indicator_key)
    
    # URL format: /v2/country/{country}/indicator/{indicator}?format=json
    url = f"{BASE_URL}/country/{country}/indicator/{ind_code}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params={"format": "json", "date": date})
            response.raise_for_status()
            data = response.json()
            
            # Handle World Bank weird JSON list of lists response
            if isinstance(data, list) and len(data) > 1:
                 records = data[1]
                 return {
                     "source": "World Bank Data API",
                     "indicator": ind_code,
                     "country": country,
                     "data": [
                         {"year": d.get("date"), "value": d.get("value")}
                         for d in records if d.get("value") is not None
                     ]
                 }
            return {"message": "No data found or unexpected format", "raw": data}
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"World Bank API Error: {str(e)}")
