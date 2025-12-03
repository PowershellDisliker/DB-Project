import React, {useState, useEffect, useContext} from "react";
import { jwtDecode } from "jwt-decode";

import { ConfigContext, AuthContext } from "../../context";
import type { C4JWT, GetPublicUserResponse } from "../../dto";

import { LoadingIcon } from '../../components/loading';
import { Friend } from '../../components/friend';
import { OpenGame } from "../../components/open-game";
import { PreviousGame } from "../../components/previous-game";
import { getPublicUser, getOpenGames, getFriends } from "../../api";

import globalStyles from "../global.module.css";
import homeStyles from "./home.module.css";

import type { HomeViewModel } from "./home-vm";
import { useNavigate } from "react-router-dom";

function Home() {
    const navigate = useNavigate();

    const config = useContext(ConfigContext);
    const {token} = useContext(AuthContext);

    if (!token) {
        navigate("/login")
        return;
    }

    const user_id: string = jwtDecode<C4JWT>(token).su;

    const [viewModel, setViewModel] = useState<HomeViewModel>({
        friends: null,
        open_games: null,
        closed_games: null,
        user_details: null,
    });


    useEffect(() => {
        const fetchData = async () => {
            const userDetails = await getPublicUser(config.BACKEND_URL, token, user_id);
            const openGames = await getOpenGames(config.BACKEND_URL, token);
            const friends = await getFriends(config.BACKEND_URL, token);

            let friends_details: Array<GetPublicUserResponse> = []

            for (const value of friends.friend_ids!) {
                friends_details.push(await getPublicUser(config.BACKEND_URL, token ,value[0]));
            }

            setViewModel(prev => ({
                ...prev,
                user_details: userDetails,
                open_games: openGames,
                friends: friends_details
            }));
        };

        fetchData();
    }, []);


    return (
        <div className={`${globalStyles.row} ${globalStyles.globalCenter} ${homeStyles.mainContainer}`}>

            <div className={`${globalStyles.column} ${globalStyles.roundedContainer} ${globalStyles.globalCenter} ${globalStyles.spaceBetween}`}>
                <div>
                    <h1>Friends List</h1>
                </div>
                {!viewModel.friends && <LoadingIcon/>}
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
                {!viewModel.open_games && <LoadingIcon/>}
                <ul>
                    {viewModel?.open_games?.games.map((value) => {
                        return (
                            <OpenGame id={value.game_id} />
                        )
                    })}
                </ul>
            </div>

            <div className={`${globalStyles.column} ${globalStyles.roundedContainer} ${globalStyles.spaceBetween} ${globalStyles.globalCenter}`}>
                <div>
                    <h1>Player Stats</h1>
                </div>
                {!viewModel.user_details && <LoadingIcon/>}
                <ul>
                    {viewModel?.closed_games?.games.map((value) => {
                        return (
                            <PreviousGame id={value.game_id} />
                        )
                    })}
                </ul>
            </div>
        </div>
    )
}

export default Home;