import React, {useState} from "react";

import { LoadingIcon } from '../components/loading';
import { Friend } from '../components/friend';
import { OpenGame } from "../components/open-game";
import { PreviousGame } from "../components/previous-game";

import globalStyles from "../global.module.css";
import homeStyles from "./home.module.css";

import type { HomeViewModel, getFriends, getOpenGames, getPreviousGames, getUserDetails } from "./home-vm";
import type { FriendProps } from "../common/types";


function Home() {
    const [viewModel, setViewModel] = useState<HomeViewModel>();

    console.log(viewModel);

    return (
        <div className={`${globalStyles.row} ${globalStyles.globalCenter} ${homeStyles.mainContainer}`}>

            <div className={`${globalStyles.column} ${globalStyles.roundedContainer} ${globalStyles.globalCenter} ${globalStyles.spaceBetween}`}>
                <div>
                    <h1>Friends List</h1>
                </div>
                {!viewModel?.friends && <LoadingIcon/>}
                <ul>
                    {viewModel?.friends?.map((value) => {
                        return (
                            <Friend username={value.username} online={value.online}/>
                        )
                    })}
                </ul>
            </div>

            <div className={`${globalStyles.column} ${globalStyles.roundedContainer} ${globalStyles.globalCenter} ${homeStyles.centerContainer} ${globalStyles.spaceBetween}`}>
                <div>
                    <h1>Hello User!</h1>
                    <h3>Open Server / Lobby List</h3>
                </div>
                {!viewModel?.open_games && <LoadingIcon/>}
                <ul>
                    {viewModel?.open_games?.map((value) => {
                        return (
                            <OpenGame id={value.id} />
                        )
                    })}
                </ul>
            </div>

            <div className={`${globalStyles.column} ${globalStyles.roundedContainer} ${globalStyles.spaceBetween} ${globalStyles.globalCenter}`}>
                <div>
                    <h1>Player Stats</h1>
                </div>
                {!viewModel?.previous_games && <LoadingIcon/>}
                <ul>
                    {viewModel?.previous_games?.map((value) => {
                        return (
                            <PreviousGame id={value.id} />
                        )
                    })}
                </ul>
            </div>

        </div>
    )
}

export default Home;