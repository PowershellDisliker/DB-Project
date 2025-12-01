import { ConfigContext } from "./config";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Login } from "./login";
import { Home } from "./home";
import { Game } from "./game";
import * as dotenv from 'dotenv';

interface Config {
  BACKEND_URL: string
  API_KEY: string
}

function App() {

  let configuration: Config = {
    BACKEND_URL: import.meta.env.BACKEND_URL,
    API_KEY: import.meta.env.API_KEY,
  }

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
