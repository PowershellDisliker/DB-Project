import React, { useState, useContext } from "react";
import {useNavigate} from "react-router-dom";
import { ConfigContext } from "../../context";
import loginStyles from "./login.module.css";
import globalStyles from "../../global.module.css";
import { type loginViewModel } from "./login-vm";
import { attemptLogin, attemptRegister, postInvalidToken } from "../../api";
import type { AuthResponse } from "../../dto";
import { useCookies } from 'react-cookie';

function Login() {
    // Used for SPA re-routing
    const navigate = useNavigate();

    // grab configuration
    const config = useContext(ConfigContext);

    // Hooks into cookie state
    const [cookies, setCookie, removeCookie] = useCookies(['jwt', 'id']);

    // Component State
    const [viewModel, updateViewModel] = useState<loginViewModel>({
        username: null,
        password: null,

        failedLoginAttempt: false,
        failedRegisterAttempt: false,
    });

    // Interaction Handlers
    const setUsername = (e: React.ChangeEvent<HTMLInputElement>) => {
       updateViewModel(prev => ({
           ...prev,
           username: e.target.value,
       }));
    };

    const setPassword = (e: React.ChangeEvent<HTMLInputElement>) => {
        updateViewModel(prev => ({
            ...prev,
            password: e.target.value,
        }));
    };

    const loginHandler = async () => {
        const response: AuthResponse = await attemptLogin(config.BACKEND_URL, viewModel.username ?? "", viewModel.password ?? "");

        if (response.success) {
            setCookie('jwt', response.token ?? "");
            setCookie('id', response.user_id ?? "");
            navigate("/home");
        } else {
            updateViewModel(prev => ({
                ...prev,
                failedLoginAttempt: true
            }))
        }
    };

    const registerHandler = async () => {
        const response: AuthResponse = await attemptRegister(config.BACKEND_URL, viewModel.username ?? "", viewModel.password ?? "");

        if (response.success) {
            setCookie('jwt', response.token ?? "");
            setCookie('id', response.user_id ?? "");
            navigate("/home");
        } else {
            updateViewModel(prev => ({
                ...prev,
                failedRegisterAttempt: true
            }))
        }
    };

    return (
        <div className={`${globalStyles.globalCenter} ${globalStyles.column}`}>
            <div className={`${globalStyles.globalCenter} ${globalStyles.column}`}>
                <div className={`${globalStyles.roundedContainer} ${globalStyles.column} ${globalStyles.spaceBetween} ${loginStyles.mainContainer}`}>
                    <div className={`${globalStyles.spaceBetween} ${loginStyles.inputElement}`}>
                        <label htmlFor="username">Username:</label>
                        <input type="text" onChange={setUsername} id="username" name="username" autoComplete="username"/>
                    </div>
                    <div className={`${globalStyles.spaceBetween} ${loginStyles.inputElement}`}>
                        <label htmlFor="password">Password:</label>
                        <input type="password" onChange={setPassword} id="password" name="password" autoComplete="password"/>
                    </div>
                    <div className={`${globalStyles.spaceBetween}  ${globalStyles.row} ${loginStyles.gap}`}>
                        <button className={loginStyles.button} onClick={registerHandler}>Register</button>
                        <button className={loginStyles.button} onClick={loginHandler}>Login</button>
                    </div>
                </div>

            </div>
            <div>
                {viewModel.failedLoginAttempt && <h3>Username or Password unkown</h3>}
            </div>
        </div>
    )
}

export default Login;