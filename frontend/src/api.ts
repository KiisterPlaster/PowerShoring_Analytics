const API_BASE = '/api';

export interface Cluster {
  id: string;
  name: string;
  region: string;
  state: string;
  lat: number;
  lng: number;
  port: string;
  vocations: string[];
  energy_sources: string[];
  critical_minerals: string[];
  hydrogen_potential: string;
  description: string;
}

export interface LayerInfo {
  layer_key: string;
  display_name: string;
  category: string;
  icon: string;
}

export interface MatchmakerResponse {
  cluster_recommended: string;
  cluster_id: string;
  location: string;
  justification: string;
  energy_profile: string;
  logistics: string;
  socioeconomic_impact: string;
  transition_justa: string;
  raw_model: string;
}

export interface GeoJSONResponse {
  layer: string;
  feature_count: number;
  source: string;
  geojson: GeoJSON.FeatureCollection;
}

export interface DecarbonizationMetrics {
  cluster_id: string;
  cluster_name: string;
  proximity_metrics: {
    nearest_transmission_grid_km: number;
    nearest_energy_plant_km: number;
    grid_connection_cost_est: string;
  };
  decarbonization_synergy: {
    score_percentage: number;
    carbon_offset_tons_year: number;
    renewable_penetration_index: string;
    regulatory_friction: string;
  };
  industrial_simulation: {
    estimated_green_jobs: number;
    attracted_investment_usd_m: number;
  };
}

// --- Clusters ---
export async function fetchClusters(): Promise<Cluster[]> {
  const res = await fetch(`${API_BASE}/clusters/`);
  if (!res.ok) throw new Error('Failed to fetch clusters');
  return res.json();
}

export async function fetchCluster(id: string): Promise<Cluster> {
  const res = await fetch(`${API_BASE}/clusters/${id}`);
  if (!res.ok) throw new Error(`Failed to fetch cluster: ${id}`);
  return res.json();
}

// --- Analytics ---
export async function fetchDecarbonizationMetrics(clusterId: string): Promise<DecarbonizationMetrics> {
  const res = await fetch(`${API_BASE}/analytics/decarbonization/${clusterId}`);
  if (!res.ok) throw new Error(`Failed to fetch analytics for cluster: ${clusterId}`);
  return res.json();
}

// --- Layers ---
export async function fetchLayerCatalog(): Promise<{ layers: LayerInfo[] }> {
  const res = await fetch(`${API_BASE}/layers/catalog`);
  if (!res.ok) throw new Error('Failed to fetch layer catalog');
  return res.json();
}

export async function fetchLayerGeoJSON(layerKey: string): Promise<GeoJSONResponse> {
  const res = await fetch(`${API_BASE}/layers/${layerKey}?resultRecordCount=2000`);
  if (!res.ok) throw new Error(`Failed to fetch layer: ${layerKey}`);
  return res.json();
}

// --- Matchmaker ---
export async function runMatchmaker(query: string): Promise<MatchmakerResponse> {
  const res = await fetch(`${API_BASE}/matchmaker/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(err.detail || 'Matchmaker failed');
  }
  return res.json();
}

// --- Health ---
export async function checkHealth(): Promise<Record<string, unknown>> {
  const res = await fetch(`${API_BASE}/health`);
  return res.json();
}
