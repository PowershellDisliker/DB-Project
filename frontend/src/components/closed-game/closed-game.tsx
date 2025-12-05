import { getClosedGames } from "../../api";
import StaticCanvas from "../static-canvas/static-canvas";
import { useEffect } from "react";

interface ClosedGameProps {
    game_id: string;
}

function ClosedGame({game_id}: ClosedGameProps) {

    // Get Game Data
    useEffect(() => {
        const inner = async () => {
            await getClosedGameDetail()
        }

        inner();
    });

    return (
        <div>
            <StaticCanvas />
        </div>
    )
}

export default ClosedGame;