import React, {useContext, useEffect} from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../../context";

function Base() {
    const navigator = useNavigate();
    const auth = useContext(AuthContext);

    useEffect(() => {
        auth.token ? navigator("/home") : navigator("/login");
    }, [])

    return (
        <></>
    )
}

export default Base;