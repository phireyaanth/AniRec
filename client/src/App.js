import React, { useState, useEffect } from "react";
import AnimeRecommendation from "./AnimeRecommendation";
import LoginScreen from "./loginScreen";

function App() {
    const [token, setToken] = useState(localStorage.getItem("token"));

    useEffect(() => {
        if (token) {
            localStorage.setItem("token", token);
        }
    }, [token]);

    return (
        <div className="flex justify-center items-center min-h-screen">
            {token ? <AnimeRecommendation /> : <LoginScreen setToken={setToken} />}
        </div>
    );
}

export default App;
