import { ConfigContext, type Config, AuthContext} from "./context";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useMemo, useState } from "react";
import { Login, Home, Game } from "./routes";

function App() {

  let configuration: Config = useMemo(() => ({
    BACKEND_URL: import.meta.env.VITE_BACKEND_URL,
    API_KEY: import.meta.env.VITE_API_KEY,
    BACKEND_WS_URL: import.meta.env.VITE_BACKEND_WS_URL,
  }), [])

  const [token, setToken] = useState<string | null>(null);

  return (
    <ConfigContext.Provider value={configuration}>
      <AuthContext.Provider value={{token, setToken}}>
        <BrowserRouter>
          <Routes>
            <Route path="/home" element={<Home/>}/>
            <Route path="/login" element={<Login/>}/>
            <Route path="/game" element={<Game />} />
          </Routes>
        </BrowserRouter>
      </AuthContext.Provider>
    </ConfigContext.Provider>
  )
}

export default App
