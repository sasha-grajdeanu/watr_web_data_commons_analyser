import React, {useState } from "react";
import "../styles/Alignment.css";
import "chart.js/auto";

const Alignment = () => {
    const [selectedSource, setSelectedSource] = useState("");
    const [selectedTarget, setSelectedTarget] = useState("");

    const sourceOptions = [
        "AdministrativeArea", "Airport", "Answer", "Book", "City", "ClaimReview",
        "CollegeOrUniversity", "Continent", "Country", "CreativeWork", "Dataset",
        "EducationalOrganization", "Event", "FAQPage", "GeoCoordinates", "GovernmentOrganization",
        "Hospital", "Hotel", "JobPosting", "LakeBodyOfWater", "LandmarksOrHistoricalBuildings",
        "Language", "Library", "LocalBusiness", "Mountain", "Movie", "Museum",
        "MusicAlbum", "MusicRecording", "Organization", "Painting", "Park", "Person",
        "Place", "Product", "QAPage", "Question", "RadioStation", "Recipe",
        "Restaurant", "RiverBodyOfWater", "School", "SearchAction", "ShoppingCenter",
        "SkiResort", "SportsEvent", "SportsTeam", "StadiumOrArena", "TVEpisode", "TelevisionStation"
    ];


    
    return (
        <div className="alignment-page">
            <h1>Alignment</h1>
            <div className="input-panel">
                <h2>Input Panel</h2>
                <label htmlFor="source-class">Source Class:</label>
                <select
                    id="source-class"
                    value={selectedSource}
                    onChange={(e) => setSelectedSource(e.target.value)}>

                        <option value="">Select a Source Class</option>
                        {sourceOptions.map((option, index) => (
                            <option key={index} value={option}>
                                {option}
                            </option>
                        ))}

                </select>

                <label htmlFor="target-class">Target Class ("might delete later"):</label>
                <select
                    id="target-class"
                    value={selectedTarget}
                    onChange={(e) => setSelectedTarget(e.target.value)}
                >
                    <option value="">Select a Target Class</option>
                    {sourceOptions.map((option, index) => (
                        <option key={index} value={option}>
                            {option}
                        </option>
                    ))}
                </select>

                <button >Classify</button>
            </div>

        </div>
    );
};

export default Alignment;
