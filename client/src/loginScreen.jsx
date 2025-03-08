import React, { useState } from "react";

const LoginScreen = ({ setToken }) => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [isLogin, setIsLogin] = useState(true);
    const [error, setError] = useState(null);

    const handleAuth = async (e) => {
        e.preventDefault();
        setError(null);
        
        const url = isLogin ? "http://localhost:8001/login" : "http://localhost:8001/register";
        const data = isLogin 
        ? new URLSearchParams({ username, password }) 
        : JSON.stringify({ username, password });

        
        const options = {
            method: "POST",
            headers: { "Content-Type": isLogin ? "application/x-www-form-urlencoded" : "application/json" },
            body: data,
        };
        
        try {
            const response = await fetch(url, options);
            const result = await response.json();
            if (!response.ok) throw new Error(result.detail || "Something went wrong");
            
            if (isLogin) {
                localStorage.setItem("token", result.access_token);
                setToken(result.access_token);
            } else {
                alert(result.message ? result.message : "User registered successfully! You can now log in.");
                setIsLogin(true);
            }
        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <div className="flex flex-col items-center p-6">
            <h2 className="text-2xl font-bold mb-4">{isLogin ? "Login" : "Register"}</h2>
            <form onSubmit={handleAuth} className="flex flex-col gap-4">
                <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} required className="border p-2 rounded" />
                <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required className="border p-2 rounded" />
                <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-700">{isLogin ? "Login" : "Register"}</button>
            </form>
            {error && <p className="text-red-500 mt-4">{error}</p>}
            <p onClick={() => setIsLogin(!isLogin)} className="cursor-pointer text-blue-600 mt-4">
                {isLogin ? "Need an account? Register" : "Already have an account? Login"}
            </p>
        </div>
    );
};

export default LoginScreen;
