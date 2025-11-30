import { ConfigContext, type ConfigData } from "./config";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Login } from "./login";
import { Home } from "./home";
import { Game } from "./game";
import * as dotenv from 'dotenv';

function App() {

  let loggedIn: boolean = false;
  dotenv.config();

  return (
    <ConfigContext.Provider value={process.env}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element = {loggedIn ? <Home/> : <Login/>}/>
          <Route path="/home" element={<Home/>}/>
          <Route path="/login" element={<Login/>}/>
          <Route path="/game" element={<Game />} />
        </Routes>
      </BrowserRouter>
    </ConfigContext.Provider>
  )
}

export default App
