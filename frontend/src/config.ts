import {createContext} from 'react';

export const ConfigContext = createContext<NodeJS.ProcessEnv | null>(null);