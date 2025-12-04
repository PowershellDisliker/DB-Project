import React, {useState, useEffect, useContext} from "react";
import { jwtDecode } from "jwt-decode";

import { ConfigContext, AuthContext } from "../../context";
import type { C4JWT, GetPublicUserResponse, PostOpenGamesResponse } from "../../dto";

import { LoadingIcon } from '../../components/loading';
import { Friend } from '../../components/friend';
import { OpenGameComp } from "../../components/open-game";
import { PreviousGame } from "../../components/previous-game";
import { getPublicUser, getOpenGames, getFriends, postOpenGame } from "../../api";

import globalStyles from "../../global.module.css";
import homeStyles from "./home.module.css";

import type { HomeViewModel } from "./home-vm";
import { useNavigate } from "react-router-dom";

function Home() {
    const navigate = useNavigate();
    
    const config = useContext(ConfigContext);
    const {token} = useContext(AuthContext);
    
    const [user_id, setUserId] = useState<string | null>(null);
    const [viewModel, setViewModel] = useState<HomeViewModel>({
        friends: null,
        open_games: null,
        closed_games: null,
        user_details: null,

        failed_to_create_game: false,
    });

    useEffect(() => {
        if (!token) {
            return;
        }
    
        try {
            const sub: string = jwtDecode<C4JWT>(token).sub;

            if (typeof sub !== "string") {
                throw new Error("Invalid JWT Payload: missing sub");
            }

            setUserId(sub)
        }

        catch (err) {
            console.error("JWT Decode Error:", err);
            navigate("/login");
        }
    
    }, [token]);


    useEffect(() => {
        if (!user_id || !token) return;

        const fetchData = async () => {
            const userDetails = await getPublicUser(config.BACKEND_URL, token, user_id);
            const openGames = await getOpenGames(config.BACKEND_URL, token);
            const friends = await getFriends(config.BACKEND_URL, token);

            let friends_details: Array<GetPublicUserResponse> = []

            if (friends.friend_ids) {
                for (const value of friends.friend_ids) {
                    friends_details.push(await getPublicUser(config.BACKEND_URL, token ,value[0]));
                }
            }

            setViewModel(prev => ({
                ...prev,
                user_details: userDetails,
                open_games: openGames,
                friends: friends_details
            }));
        };

        fetchData();
    }, [user_id]);

    const createGameHandler = async () => {
        if (!token) return;

        const response: PostOpenGamesResponse = await postOpenGame(config.BACKEND_URL, token);

        if (!response.success) {
            setViewModel((prev) => ({
                ...prev,
                failed_to_create_game: true,
            }))
            return;
        }

        navigate(`/game?game_id=${response.game_id}`)
    };

    
    const addFriendHandler = async () => {

    }


    return (
        <div className={`${globalStyles.row} ${globalStyles.globalCenter} ${homeStyles.mainContainer}`}>

            <div className={`${globalStyles.column} ${globalStyles.roundedContainer} ${globalStyles.globalCenter} ${globalStyles.spaceBetween}`}>
                <div>
                    <h1>Friends List</h1>
                </div>
                {viewModel.friends == null && <LoadingIcon/>}
                <ul>
                    {viewModel.friends?.map((value) => {
                        return (
                            <Friend username={value.username} online={value.online}/>
                        )
                    })}
                </ul>
                <div className={`${globalStyles.column}`}>
                    <input type="text" />
                    <button onClick={addFriendHandler}>Add Friend</button>
                </div>
            </div>

            <div className={`${globalStyles.column} ${globalStyles.roundedContainer} ${globalStyles.globalCenter} ${homeStyles.centerContainer} ${globalStyles.spaceBetween}`}>
                <div>
                    <h1>Hello {viewModel.user_details?.username}!</h1>
                    <h3>Open Server / Lobby List</h3>
                </div>
                {viewModel.open_games == null && <LoadingIcon/>}
                <ul>
                    {viewModel.open_games?.games?.map((value) => {
                        return (
                            <OpenGameComp game={value} key={value.game_id}/>
                        )
                    })}
                </ul>
                <button onClick={createGameHandler}>Create Game</button>
            </div>

            <div className={`${globalStyles.column} ${globalStyles.roundedContainer} ${globalStyles.spaceBetween} ${globalStyles.globalCenter}`}>
                <div>
                    <h1>Player Stats</h1>
                </div>
                {viewModel.user_details == null && <LoadingIcon/>}
                <ul>
                    {viewModel?.closed_games?.games?.map((value) => {
                        return (
                            <PreviousGame id={value.game_id} key={value.game_id}/>
                        )
                    })}
                </ul>
            </div>
        </div>
    )
}

export default Home;