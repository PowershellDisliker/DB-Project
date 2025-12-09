import {createContext} from 'react';

export interface Config {
  BACKEND_URL: string;
  BACKEND_WS_URL: string;
  API_KEY: string;
}

export const ConfigContext = createContext<Config>(null!);