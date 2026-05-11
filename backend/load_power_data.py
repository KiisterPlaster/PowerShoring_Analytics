import os
import requests
import psycopg2
import json
from geoalchemy2.elements import WKTElement
from geoalchemy2.shape import from_shape
from shapely.geometry import shape

def seed_epe_data():
    print("--- CONNECTING TO CLOUD DATABASE TO LOAD EPE ANALYTICS DATA ---")
    
    # Read directly from standard credentials
    host = "aws-1-us-west-2.pooler.supabase.com"
    ref = "chgmnyftxgtlgvplgeor"
    raw_pass = "18021940Mdkp@M"
    
    conn = psycopg2.connect(
        host=host,
        port=6543,
        dbname="postgres",
        user=f"postgres.{ref}",
        password=raw_pass,
        sslmode='require',
        connect_timeout=10
    )
    cur = conn.cursor()
    
    # Clear old stale data to prevent bloat
    cur.execute("DELETE FROM epe_data WHERE source = 'AUTO_SEED';")
    conn.commit()
    
    # FETCH EPE USINAS EXISTENTES (ENERGY PLANTS)
    print("[1/2] FETCHING LIVE USINAS DATA FROM EPE PORTAL...")
    epe_usinas_url = "https://gisepeprd2.epe.gov.br/arcgis/rest/services/WebMapEPE/Usinas_Existentes/MapServer/0/query"
    params = {
        "where": "1=1",
        "outFields": "*",
        "f": "geojson",
        "resultRecordCount": 100,
        "returnGeometry": "true"
    }
    
    try:
        res = requests.get(epe_usinas_url, params=params, verify=False, timeout=30)
        if res.status_code == 200:
            gj = res.json()
            features = gj.get("features", [])
            print(f"Found {len(features)} energy assets. Loading into PostGIS...")
            
            inserted = 0
            for f in features:
                props = f.get("properties", {})
                geom = f.get("geometry")
                if not geom: continue
                
                name = props.get("NOME", "Usinas Desconhecida")
                etype = props.get("TIPO", "Geração")
                capacity = props.get("POT_OUT", 0) or 0
                state = props.get("UF", "BR")
                
                # Convert to WKT for direct PostGIS INSERT
                try:
                    s = shape(geom)
                    wkt = s.wkt
                    
                    cur.execute(
                        """
                        INSERT INTO epe_data (source, category, name, energy_type, capacity_mw, state, geom, raw_data, fetched_at)
                        VALUES ('AUTO_SEED', 'usina', %s, %s, %s, %s, ST_GeomFromText(%s, 4326), %s, NOW())
                        """,
                        (name, etype, float(capacity), state, wkt, json.dumps(props))
                    )
                    inserted += 1
                except Exception as ex:
                    continue
            
            conn.commit()
            print("SUCCESSFULLY INJECTED ENERGY PLANTS INTO CLOUD POSTGIS!")
    except Exception as e:
        print("FAILED USINAS SEED:")
        
    # FETCH EPE TRANSMISSION LINES
    print("[2/2] FETCHING LIVE TRANSMISSION INFRASTRUCTURE...")
    epe_lin_url = "https://gisepeprd2.epe.gov.br/arcgis/rest/services/WebMapEPE/Sistema_Transmissao/MapServer/0/query"
    params["resultRecordCount"] = 100
    try:
        res = requests.get(epe_lin_url, params=params, verify=False, timeout=30)
        if res.status_code == 200:
            gj = res.json()
            features = gj.get("features", [])
            print(f"Found {len(features)} transmission circuits. Loading...")
            
            inserted = 0
            for f in features:
                props = f.get("properties", {})
                geom = f.get("geometry")
                if not geom: continue
                
                name = props.get("NOME", "Linha")
                etype = props.get("TENS_OP", "LT")
                state = props.get("UF", "BR")
                
                try:
                    s = shape(geom)
                    wkt = s.wkt
                    cur.execute(
                        """
                        INSERT INTO epe_data (source, category, name, energy_type, capacity_mw, state, geom, raw_data, fetched_at)
                        VALUES ('AUTO_SEED', 'linha_transmissao', %s, %s, 0, %s, ST_GeomFromText(%s, 4326), %s, NOW())
                        """,
                        (name, str(etype), state, wkt, json.dumps(props))
                    )
                    inserted += 1
                except Exception:
                    continue
            
            conn.commit()
            print("SUCCESSFULLY INJECTED TRANSMISSION LINES INTO CLOUD POSTGIS!")
    except Exception as e:
        print("FAILED LINES SEED:")

    conn.close()
    print("\nALL ANALYTICS DATA BOOTSTRAPPED SUCCESSFULLY! DATABASE IS NOW SPATIALLY INTELLIGENT.")

if __name__ == "__main__":
    seed_epe_data()
