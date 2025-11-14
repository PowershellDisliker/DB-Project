/* 
The Viewmodel will contain the state object definition and all API logic that is used on
this page. This format will be followed on all pages.
*/

export type loginViewModel = {
    username: string | null;
    password: string | null;

    failedLoginAttempt: boolean;
}

export const AttemptLogin = async (username: string, password: string): Promise<Boolean> => {
    const res = await fetch(
        "http://127.0.0.1:8000/login",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user_attempt: username,
                pass_attempt: password,
            })
        }
    )

    if (!res.ok) {
        return false;
    }

    const data = await res.json()

    return data.success as boolean;
}