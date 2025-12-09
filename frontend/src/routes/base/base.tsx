import {useEffect} from "react";
import { useNavigate } from "react-router-dom";
import { useCookies } from "react-cookie";

function Base() {
    const navigator = useNavigate();
    const [cookies] = useCookies(['jwt']);

    useEffect(() => {
        cookies.jwt ? navigator("/home") : navigator("/login");
    }, [])

    return (
        <></>
    )
}

export default Base;