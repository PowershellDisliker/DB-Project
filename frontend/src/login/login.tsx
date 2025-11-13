import React, {useState, useEffect} from "react";
import {useNavigate} from "react-router-dom";
import loginStyles from "./login.module.css";
import globalStyles from "../global.module.css";
import { type loginViewModel, AttemptLogin } from "./login-vm";

function Login() {
    const navigate = useNavigate();

    const [viewModel, updateViewModel] = useState<loginViewModel>({
        username: null,
        password: null,

        failedLoginAttempt: false,
    });

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

    const submitForm = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        if (await AttemptLogin(viewModel.username ?? "", viewModel.password ?? "")) {
            navigate("/home");
        } else {
            updateViewModel(prev => ({
                ...prev,
                failedLoginAttempt: true
            }))
        };
    }

    return (
        <div className={`${globalStyles.center} ${globalStyles.column}`}>
            <form className={`${globalStyles.roundedContainer} ${globalStyles.column}`} onSubmit={submitForm}>
                <div className={`${globalStyles.center} ${loginStyles.inputElement}`}>
                    <label htmlFor="username">Username:</label>
                    <input type="text" onChange={setUsername} id="username" name="username" autoComplete="username"/>
                </div>
                <div className={`${globalStyles.center} ${loginStyles.inputElement}`}>
                    <label htmlFor="password">Password:</label>
                    <input type="password" onChange={setPassword} id="password" name="password" autoComplete="password"/>
                </div>
                <input type="submit" />
            </form>

            {viewModel.failedLoginAttempt && <h3>Username or Password unkown</h3>}
        </div>
    )
}

export default Login;