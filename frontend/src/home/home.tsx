import React, {useState} from "react";

import { LoadingIcon } from '../components/loading';
import { Friend } from '../components/friend';
import { OpenGame } from "../components/open-game";
import { PreviousGame } from "../components/previous-game";

import globalStyles from "../global.module.css";
import homeStyles from "./home.module.css";

import type { HomeViewModel } from "./home-vm";
import type { FriendProps } from "../common/types";


function Home() {
    const [viewModel, setViewModel] = useState<HomeViewModel>();

    return (
        <div className={`${globalStyles.row} ${globalStyles.globalCenter}`}>

            <div className={`${globalStyles.roundedContainer}`}>
                <h1>Friends List</h1>
                {viewModel?.friends && <LoadingIcon/>}
                <ul>
                    {viewModel?.friends.map((value) => {
                        return (
                            <Friend props={value}/>
                        )
                    })}
                </ul>
            </div>

            <div className={`${globalStyles.column} ${globalStyles.roundedContainer}`}>
                <h1>Hello User!</h1>
                <h3>Open Server / Lobby List</h3>
                {viewModel?.open_games && <LoadingIcon/>}
                <ul>
                    {viewModel?.open_games.map((value) => {
                        return (
                            <OpenGame props={value} />
                        )
                    })}
                </ul>
            </div>

            <div className={`${globalStyles.roundedContainer}`}>
                <h1>Player Stats</h1>
                {viewModel?.previous_games && <LoadingIcon/>}
                <ul>
                    {viewModel?.previous_games.map((value) => {
                        return (
                            <PreviousGame props={value} />
                        )
                    })}
                </ul>
            </div>

        </div>
    )
}

export default Home;