import { useState } from "react";

export default function AnimeRecommendation() {
    const [uid, setUid] = useState("");
    const [recommendations, setRecommendations] = useState([]);
    const [error, setError] = useState("");

    const getRecommendations = async () => {
        setError(""); // Clear previous errors
        setRecommendations([]); // Clear previous recommendations
        
        if (!uid) {
            setError("Please enter a valid UID.");
            return;
        }
        
        try {
            const response = await fetch("http://127.0.0.1:8000/recommend", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ uid: parseInt(uid) })
            });
            
            const data = await response.json();
            if (data.recommended_titles) {
                setRecommendations(data.recommended_titles);
            } else {
                setError(data.error || "No recommendations found.");
            }
        } catch (error) {
            setError("Failed to fetch recommendations. Please check your server.");
        }
    };

    return (
        <div className="flex flex-col items-center p-6">
            <h2 className="text-2xl font-bold mb-4">Anime Recommendation System</h2>
            <input 
                type="number" 
                placeholder="Enter Anime UID" 
                value={uid} 
                onChange={(e) => setUid(e.target.value)}
                className="border p-2 mb-4 rounded"
            />
            <button 
                onClick={getRecommendations} 
                className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-700"
            >
                Get Recommendations
            </button>
            {error && <p className="text-red-500 mt-4">{error}</p>}
            {recommendations.length > 0 && (
                <div className="mt-6">
                    <h3 className="text-xl font-semibold">Recommended Animes:</h3>
                    <ul className="list-disc list-inside">
                        {recommendations.map((title, index) => (
                            <li key={index}>{title}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}
