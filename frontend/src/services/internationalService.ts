import { apiClient } from './apiClient';

export interface WbRecord {
  year: string;
  value: number | null;
}

export interface WbResponse {
  source: string;
  indicator: string;
  country: string;
  data: WbRecord[];
}

export const internationalService = {
  fetchWorldBankIndicator: async (indicatorKey: string, country = 'BRA', date = '2015:2024') =>
    apiClient<WbResponse>(`/worldbank/fetch/${indicatorKey}?country=${country}&date=${date}`),

  fetchIrenaEmployment: async () =>
    apiClient<any>('/irena/employment'),
    
  fetchExternalDirectory: async () =>
    apiClient<any>('/external/directory'),
};
