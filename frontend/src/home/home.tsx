import React from "react";
import globalStyles from "../global.module.css";
import homeStyles from "./home.module.css";

function Home() {

    return (
        <div className={`${globalStyles.row} ${globalStyles.center}`}>
            <div className={`${globalStyles.roundedContainer}`}>
                <h1>Friends List</h1>
            </div>
            <div className={`${globalStyles.column} ${globalStyles.roundedContainer}`}>
                <h1>Hello User!</h1>
                <h3>Open Server / Lobby List</h3>
            </div>
            <div className={`${globalStyles.roundedContainer}`}>
                <h1>Player Stats</h1>
            </div>
        </div>
    )
}

export default Home;