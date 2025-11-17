async function RequestFromServer<T>(request: Object) {
    const URI: string = "http://127.0.0.1:8000/login"

    const res = await fetch(
        URI,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(request)
        }
    )

    if (!res.ok) {
        throw new Error(`Error Contacting backend: ${res.status}`);
    }

    const jsonData = await res.json();

    return jsonData as T;
}

export const AttemptLogin = async (username: string, password: string): Promise<Boolean> => {
    return RequestFromServer<Boolean>({username: username, password: password});
}