import { apiClient } from './apiClient';

export interface SidraRecord {
  V?: string; // Valor
  D1N?: string; // Territorial
  D2N?: string; // Variável
  D3N?: string; // Ano/Período
  [key: string]: any;
}

export interface SidraResponse {
  source: string;
  record_count: number;
  data: SidraRecord[];
}

export const ibgeService = {
  fetchPib: async (period = 'last 5') => 
    apiClient<SidraResponse>(`/ibge/pib?period=${period}`),
    
  fetchPam: async (crop = '81/all', period = 'last 1') => 
    apiClient<SidraResponse>(`/ibge/pam?period=${period}&classification=${crop}`),

  fetchPevs: async (period = 'last 5') => 
    apiClient<SidraResponse>(`/ibge/pevs?period=${period}`),

  fetchBdiaMetadata: async () => 
    apiClient<any>('/ibge/bdia/metadata'),
    
  fetchAtlasLayers: async () =>
    apiClient<any>('/atlas/layers'),
};
