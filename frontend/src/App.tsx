import { ConfigContext, type Config } from "./config";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useMemo } from "react";
import { Login } from "./login";
import { Home } from "./home";
import { Game } from "./game";

function App() {

  let configuration: Config = useMemo(() => ({
    BACKEND_URL: import.meta.env.VITE_BACKEND_URL,
    API_KEY: import.meta.env.VITE_API_KEY,
  }), [])

  return (
    <ConfigContext.Provider value={configuration}>
      <BrowserRouter>
        <Routes>
          <Route path="/home" element={<Home/>}/>
          <Route path="/login" element={<Login/>}/>
          <Route path="/game" element={<Game />} />
        </Routes>
      </BrowserRouter>
    </ConfigContext.Provider>
  )
}

export default App
