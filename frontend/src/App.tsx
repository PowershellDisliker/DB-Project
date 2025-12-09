import { ConfigContext, type Config} from "./context";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useMemo } from "react";
import { Login, Home, Game, Base, Messages } from "./routes";
import { CookiesProvider } from 'react-cookie';

function App() {

  let configuration: Config = useMemo(() => ({
    BACKEND_URL: import.meta.env.VITE_BACKEND_URL,
    API_KEY: import.meta.env.VITE_API_KEY,
    BACKEND_WS_URL: import.meta.env.VITE_BACKEND_WS_URL,
  }), [])

  return (
    <CookiesProvider>
      <ConfigContext.Provider value={configuration}>
          <BrowserRouter>
            <Routes>
              <Route path="/" element={<Base/>}/>
              <Route path="/home" element={<Home/>}/>
              <Route path="/login" element={<Login/>}/>
              <Route path="/game" element={<Game />} />
              <Route path="/messages" element={<Messages />} />
            </Routes>
          </BrowserRouter>
      </ConfigContext.Provider>
    </CookiesProvider>
  )
}

export default App
