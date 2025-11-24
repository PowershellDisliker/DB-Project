import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Login } from "./login";
import { Home } from "./home";
import { Game } from "./game";

function App() {

  let loggedIn: boolean = false;

  return (
      <BrowserRouter>
        <Routes>
          <Route path="/" element = {loggedIn ? <Home/> : <Login/>}/>
          <Route path="/home" element={<Home/>}/>
          <Route path="/login" element={<Login/>}/>
          <Route path="/game" element={<Game />} />
        </Routes>
      </BrowserRouter>
  )
}

export default App
