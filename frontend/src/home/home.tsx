import React, {useState, useEffect} from "react";

import { LoadingIcon } from '../components/loading';
import { Friend } from '../components/friend';
import { OpenGame } from "../components/open-game";
import { PreviousGame } from "../components/previous-game";
import { GetUserInfo, GetOpenGames, GetFriends } from "../api/api";

import globalStyles from "../global.module.css";
import homeStyles from "./home.module.css";

import type { HomeViewModel } from "./home-vm";

function Home() {
    const [viewModel, setViewModel] = useState<HomeViewModel>({
        friends: null,
        open_games: null,
        previous_games: null,
        user_details: null,
    });

    let loadingFriends = true;
    const FriendsList = viewModel.friends;

    let loadingOpenGames = true;
    const OpenGames = viewModel.open_games;

    let loadingPreviousGames = true;
    const PreviousGames = viewModel.previous_games;

    let loadingUserDetails = true;
    const UserDetails = viewModel.user_details;


    useEffect(() => {
        const fetchData = async () => {
            const userDetails = await GetUserInfo("TOKEN");
            const openGames = await GetOpenGames();
            const friends = await GetFriends(userDetails.username);

            setViewModel(prev => ({
                ...prev,
                user_details: userDetails,
                open_games: openGames,
                friends: friends,
            }));
        };

        fetchData();
    }, [UserDetails]);


    return (
        <div className={`${globalStyles.row} ${globalStyles.globalCenter} ${homeStyles.mainContainer}`}>

            <div className={`${globalStyles.column} ${globalStyles.roundedContainer} ${globalStyles.globalCenter} ${globalStyles.spaceBetween}`}>
                <div>
                    <h1>Friends List</h1>
                </div>
                {loadingFriends && <LoadingIcon/>}
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
                {loadingOpenGames && <LoadingIcon/>}
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
                {loadingUserDetails && <LoadingIcon/>}
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