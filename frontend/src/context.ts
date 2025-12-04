import {createContext} from 'react';

export interface Config {
  BACKEND_URL: string;
  BACKEND_WS_URL: string;
  API_KEY: string;
}

export interface AuthState {
  token: string | null;
  setToken: (t: string | null) => void;

  user_id: string | null;
  setUserId: (t: string | null) => void;
}

export const ConfigContext = createContext<Config>(null!);
export const AuthContext = createContext<AuthState>(null!);