import { apiClient } from './apiClient';

export interface AnpRecord {
  [key: string]: any;
}

export interface AnpResponse {
  source: string;
  dataset_key: string;
  data: AnpRecord[];
}

export const energyService = {
  // ANP Endpoints
  fetchAnpData: async (datasetKey: string, limit = 1000) =>
    apiClient<AnpResponse>(`/anp/data/${datasetKey}?limit=${limit}`),
  
  // Fuel-specific quick getters
  fetchEtanolVendas: async () =>
    apiClient<AnpResponse>(`/anp/data/etanol?limit=1000`),
    
  fetchBiodieselVendas: async () =>
    apiClient<AnpResponse>(`/anp/data/biodiesel?limit=1000`),

  // EPE GIS Endpoints
  fetchEpeLayers: async () =>
    apiClient<{ available_shortcuts: string[], base_url: string }>('/epe/layers'),

  fetchEpeGeoJson: async (shortcut: string) =>
    apiClient<any>(`/epe/query/${shortcut}`),
    
  // ANEEL CKAN Endpoints
  fetchAneelSiga: async () =>
    apiClient<any>('/aneel/info'),
};
