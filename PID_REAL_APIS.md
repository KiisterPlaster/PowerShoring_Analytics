# Direcionador de APIs Reais - Plataforma PID (Reverse Engineered)

> **IMPORTANTE:** Este documento registra as URLs diretas dos FeatureServers da ESRI ArcGIS que alimentam a plataforma PID oficial. Elas dispensam mockagem e garantem dados dinâmicos e reais.

## Endpoints Rest - FeatureServer Base:
**Base URL:** `https://services6.arcgis.com/I9CTS4kjOw8Dsslu/arcgis/rest/services/`

### 🌳 Ambiental & Fundiário
| Camada | URL do Endpoint | Formato |
| :--- | :--- | :--- |
| **Unidades de Conservação** | `.../Unidades_Conservacao/FeatureServer/0` | FeatureLayer (Polígono) |
| **Terras Quilombolas** | `.../Terras_Quilombolas/FeatureServer/0` | FeatureLayer (Polígono) |
| **Terras Indígenas** | `.../Terras_Indigenas/FeatureServer/0` | FeatureLayer (Polígono) |
| **Pastagens Degradadas (Inter.)** | `.../areas_potenciais_inter/FeatureServer/0` | FeatureLayer (Polígono) |
| **Pastagens Degradadas (Severa)** | `.../areas_potenciais_severa/FeatureServer/0` | FeatureLayer (Polígono) |

### ⚡ Energia & Infraestrutura Logística
| Componente | URL do Endpoint | Camada ID |
| :--- | :--- | :--- |
| **Portos** | `.../Infraestruturas_WFL1/FeatureServer` | `0` |
| **Aeroportos** | `.../Infraestruturas_WFL1/FeatureServer` | `1` |
| **Estradas** | `.../Infraestruturas_WFL1/FeatureServer` | `2` |
| **Hidrovias** | `.../Infraestruturas_WFL1/FeatureServer` | `3` |
| **Ferrovias** | `.../Infraestruturas_WFL1/FeatureServer` | `4` |
| **Hubs H2** | `.../Hubs_H2/FeatureServer` | `1` |
| **Minerais Críticos** | `.../Minerais_Criticos/FeatureServer` | `0` |
| **Energia Solar (UFV)** | `.../Solar_UFV/FeatureServer` | `0 (Existente) / 1 (Planejada)` |

### 🛰️ Imageria & Raster (Uso do Solo / CO2)
| Dataset | Base URL | Tipo |
| :--- | :--- | :--- |
| **MapBiomas Uso Solo** | `https://ic.imagery1.arcgis.com/arcgis/rest/services/MapBiomas/ImageServer` | ImageServer |
| **Emissões CO2 Global** | `https://tiledimageservices.arcgis.com/jIL9msH9OI208GCb/arcgis/rest/services/Global_Anthropogenic_CO2_Emissions_2018__tiled_/ImageServer` | ImageServer (Tiled) |

---
## Padrão de Consumo (Frontend)
No React-Leaflet/MapLibre, utilize o provedor ESRI para carregamento dinâmico de tiles ou GeoJSON via:
`.../FeatureServer/0/query?where=1%3D1&outFields=*&f=geojson`
