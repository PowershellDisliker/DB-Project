import {useState, useEffect, useContext} from "react";

import { ConfigContext, AuthContext } from "../../context";
import type { PostFriendRequest, PostOpenGamesResponse } from "../../dto";

import { LoadingIcon } from '../../components/loading';
import { Friend } from '../../components/friend';
import OutgoingFriendRequest from "../../components/outgoing-friend/outgoing-friend";
import IncomingFriendRequest from "../../components/incoming-friend/incoming-friend";
import { OpenGameComp } from "../../components/open-game";
import { PreviousGame } from "../../components/previous-game";
import { getPublicUser, getOpenGames, getFriends, postOpenGame } from "../../api";

import globalStyles from "../../global.module.css";
import homeStyles from "./home.module.css";

import type { HomeViewModel } from "./home-vm";
import { useNavigate } from "react-router-dom";
import { getIncomingFriendRequests, getOutgoingFriendRequests, getPublicUserFromUsername, postFriend } from "../../api/api";

function Home() {
    const navigate = useNavigate();
    
    const config = useContext(ConfigContext);
    const auth = useContext(AuthContext);
    
    const [viewModel, setViewModel] = useState<HomeViewModel>({
        friends: null,
        open_games: null,
        closed_games: null,
        user_details: null,
        outgoing_friend_requests: null,
        incoming_friend_requests: null,

        failed_to_create_game: false,
        failed_to_post_friend: false,

        need_to_update: false,

        username_input: "",
    });


    const updateState = () => {
        setViewModel((prev) => ({
            ...prev,
            need_to_update: true,
        }))
    }


    useEffect(() => {
        if (!auth.user_id || !auth.token) return;

        const fetchData = async () => {
            const userDetails            = await getPublicUser(config.BACKEND_URL, auth.token!, auth.user_id!);
            const openGames              = await getOpenGames(config.BACKEND_URL, auth.token!);
            const confirmedFriends       = await getFriends(config.BACKEND_URL, auth.token!);
            const outGoingFriendRequests = await getOutgoingFriendRequests(config.BACKEND_URL, auth.token!);
            const incomingFriendRequests = await getIncomingFriendRequests(config.BACKEND_URL, auth.token!);

            setViewModel(prev => ({
                ...prev,
                user_details: userDetails,
                open_games: openGames,
                friends: confirmedFriends.users,
                outgoing_friend_requests: outGoingFriendRequests.users,
                incoming_friend_requests: incomingFriendRequests.users,
                need_to_update: false,
            }));
        };

        fetchData();
    }, [auth.user_id, viewModel.need_to_update]);

    const createGameHandler = async () => {
        if (!auth.token) return;

        const response: PostOpenGamesResponse = await postOpenGame(config.BACKEND_URL, auth.token);

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
        const user_id_from_name = (await getPublicUserFromUsername(config.BACKEND_URL, auth.token!, viewModel.username_input)).user_id;
        await postFriend(config.BACKEND_URL, auth.token!, {requestor_id: auth.user_id, requestee_id: user_id_from_name} as PostFriendRequest)
        updateState();
    }

    return (
        <div className={`${globalStyles.row} ${globalStyles.globalCenter} ${homeStyles.mainContainer}`}>
            
            <div className={`${globalStyles.roundedContainer} ${globalStyles.column} ${globalStyles.center} ${homeStyles.loginColumn}`}>
                <h1>Friends List</h1>
                <div className={`${globalStyles.column} ${globalStyles.spaceBetween} ${homeStyles.loginColumn}`}>
                    {viewModel.friends == null && <LoadingIcon/>}

                    <div className={`${globalStyles.column} ${globalStyles.center}`}>
                        <h3>Friends</h3>
                        <ul className={`${globalStyles.scroll}`}>
                            {viewModel.friends?.map((value) => {
                                return (
                                    <Friend user={value} state_update={updateState} key={value.user_id}/>
                                )
                            })}
                        </ul>
                    </div>
                        
                    <div className={`${globalStyles.column} ${globalStyles.center}`}>
                        <h3>Incoming Friend Requests</h3>
                        <ul className={`${globalStyles.scroll}`}>
                            {viewModel.incoming_friend_requests?.map((value) => {
                                return (
                                    <IncomingFriendRequest user={value} state_update={updateState} key={value.user_id}/>
                                )
                            })}
                        </ul>
                    </div>

                    <div className={`${globalStyles.column} ${globalStyles.center}`}>
                        <h3>Outgoing Friend Requests</h3>
                        <ul className={`${globalStyles.scroll}`}>
                            {viewModel.outgoing_friend_requests?.map((value) => {
                                return (
                                    <OutgoingFriendRequest user={value} state_update={updateState} key={value.user_id}/>
                                )
                            })}
                        </ul>
                    </div>

                    <div className={`${globalStyles.center}`}>
                        <input type="text" onChange={(event) => {
                            setViewModel((prev) => ({
                                ...prev,
                                username_input: event.target.value
                            }))
                        }}/>
                        <button onClick={addFriendHandler}>Add Friend</button>
                    </div>

                </div>
            </div>


            {/* OPEN SERVERS */}
            <div className={`${globalStyles.column} ${globalStyles.roundedContainer} ${globalStyles.globalCenter} ${homeStyles.centerContainer} ${globalStyles.spaceBetween}`}>
                <div className={`${globalStyles.centerText}`}>
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

            {/* CLOSED GAMES */}
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