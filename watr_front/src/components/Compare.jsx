import React, { useEffect, useState, useRef } from "react";
import "chart.js/auto";
import { Network, DataSet } from "vis-network/standalone/umd/vis-network.min.js";
import "../styles/Visualisation.css";
import VisualisationCharts from "./VisualisationCharts";

const Compare = () => {
    const [selectedClassOne, setSelectedClassOne] = useState("");
    const [selectedClassTwo, setSelectedClassTwo] = useState("");
    const [compareData, setCompareData] = useState("");
    const [jsonStatisticsData, setJsonStatisticsData] = useState("");
    const [showStatistics, setShowStatistics] = useState(false); // State to control visibility of statistics div
    const dataContainer = useRef(null);

    const classOptions = [
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



const handleVisualise = async () => {
    if (!selectedClassOne || !selectedClassTwo) {
        alert("Please select a class to visualize");
        return;
    }
    if (selectedClassOne === selectedClassTwo) {
        alert("Please select different classes to compare");
        return;
    }

    try {
        // Fetch DataML Data
        const dataUrl = `http://localhost:5000/api/compare/data?class_one=${selectedClassOne}&class_two=${selectedClassTwo}`
        const dataResponse = await fetch(dataUrl, {
            method: "GET",
        });
        if (!dataResponse.ok) {
            throw new Error("Compare API call failed");
        }
        const data = await dataResponse.json();
        setCompareData(data);

        // Fetch Statistics Data
        const statsUrl = `http://localhost:5000/api/compare/statistics?class_one=${selectedClassOne}&class_two=${selectedClassTwo}`
        const statsResponse = await fetch(statsUrl, {
            method: "GET",
        });
        if (!statsResponse.ok) {
            throw new Error("Statistics API call failed");
        }
        const statsData = await statsResponse.json(); // Assume the statistics endpoint returns JSON
        setJsonStatisticsData(statsData);
        setShowStatistics(true); // Show statistics panel after successful visualization
    } catch (error) {
        console.error("Error during visualization process:", error);
    }
};

const handleImportHTML = async () => {
    if (!showStatistics) {
        alert("Please visualize the data first!");
        return;
    }

    try {
        const url = `http://localhost:5000/api/compare/html?class_one=${selectedClassOne}&class_two=${selectedClassTwo}`

        const response = await fetch(url, { method: "GET" });

        if (!response.ok) {
            throw new Error("Failed to fetch the HTML file.");
        }

        const htmlData = await response.text();

        // Create a blob and trigger download
        const blob = new Blob([htmlData], { type: "text/html" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = `Compare_${selectedClassOne}_${selectedClassTwo}_data.html`; // Name of the downloaded file
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } catch (error) {
        console.error("Error importing HTML:", error);
    }
};

const handleImportJSON_LD = async () => {
    if (!showStatistics) {
        alert("Please visualize the data first!");
        return;
    }

    try {
        const url = `http://localhost:5000/api/compare/json_ld?class_one=${selectedClassOne}&class_two=${selectedClassTwo}`

        const response = await fetch(url, { method: "GET" });

        if (!response.ok) {
            throw new Error("Failed to fetch the JSON-LD file.");
        }

        const jsonLDData = await response.json();

        // Create a blob and trigger download
        const blob = new Blob([JSON.stringify(jsonLDData, null, 2)], { type: "application/ld+json" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = `Compare_${selectedClassOne}_${selectedClassTwo}_data.jsonld`; // Name of the downloaded file
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } catch (error) {
        console.error("Error importing JSON-LD:", error);
    }
};

const handleImportStatistics = async () => {
    if (!showStatistics) {
        alert("Please show the statistics first!");
        return;
    }

    try {
        const url = `http://localhost:5000/api/compare/download_statistics?class_one=${selectedClassOne}&class_two=${selectedClassTwo}`

        const response = await fetch(url, { method: "GET" });

        if (!response.ok) {
            throw new Error("Failed to fetch the JSON-LD file.");
        }

        const jsonLDData = await response.json();

        // Create a blob and trigger download
        const blob = new Blob([JSON.stringify(jsonLDData, null, 2)], { type: "application/ld+json" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = `Compare_${selectedClassOne}_${selectedClassTwo}_statistics.jsonld`; // Name of the downloaded file
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } catch (error) {
        console.error("Error importing JSON-LD:", error);
    }
};
    return (
        <div className="visualisation-page">
            <h1>Compare</h1>
            <div className="input-panel">
                <h2>Input Panel</h2>

                {/* Class Select Dropdown */}
                <label htmlFor="class">Class one:</label>
                <select
                    id="class"
                    className="input-field"
                    value={selectedClassOne}
                    onChange={(e) => setSelectedClassOne(e.target.value)}
                >
                    <option value="">Select a Class</option>
                    {classOptions.map((option, index) => (
                        <option key={index} value={option}>
                            {option}
                        </option>
                    ))}
                </select>

                <label htmlFor="class">Class two:</label>
                <select
                    id="class"
                    className="input-field"
                    value={selectedClassTwo}
                    onChange={(e) => setSelectedClassTwo(e.target.value)}
                >
                    <option value="">Select a Class</option>
                    {classOptions.map((option, index) => (
                        <option key={index} value={option}>
                            {option}
                        </option>
                    ))}
                </select>

                {/* Visualize Button */}
                <button onClick={handleVisualise}>Compare</button>

                {/* Data Container */}

                {compareData && (
                    <div className="compare-table">
                        <h2>Comparison Data</h2>
                        <table>
                            <thead>
                                <tr>
                                    <th>Property</th>
                                    <th>{selectedClassOne}</th>
                                    <th>{selectedClassTwo}</th>
                                </tr>
                            </thead>
                            <tbody>
                                {compareData.map((row, index) => (
                                    <tr key={index}>
                                        <td>{row.property}</td>
                                        <td>{row[selectedClassOne]}</td>
                                        <td>{row[selectedClassTwo]}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}

                {/* Statistics Div (Conditionally Rendered) */}
                {showStatistics && jsonStatisticsData && (
                    <div className="statistics-panel">
                        <h2>Statistics</h2>
                        <div className="statistics-section">
                            <h3>{selectedClassOne}</h3>
                            <p><strong>Least Used Property:</strong> {jsonStatisticsData[selectedClassOne].least_used}</p>
                            <p><strong>Most Used Property:</strong> {jsonStatisticsData[selectedClassOne].most_used}</p>
                            <p><strong>Total Properties:</strong> {jsonStatisticsData[selectedClassOne].total_count}</p>
                            <p><strong>Unique Properties:</strong></p>
                            <ul>
                                {jsonStatisticsData[selectedClassOne].unique_properties.map((prop, index) => (
                                    <li key={index}>{prop}</li>
                                ))}
                            </ul>
                        </div>
                        <div className="statistics-section">
                            <h3>{selectedClassTwo}</h3>
                            <p><strong>Least Used Property:</strong> {jsonStatisticsData[selectedClassTwo].least_used}</p>
                            <p><strong>Most Used Property:</strong> {jsonStatisticsData[selectedClassTwo].most_used}</p>
                            <p><strong>Total Properties:</strong> {jsonStatisticsData[selectedClassTwo].total_count}</p>
                            <p><strong>Unique Properties:</strong></p>
                            <ul>
                                {jsonStatisticsData[selectedClassTwo].unique_properties.map((prop, index) => (
                                    <li key={index}>{prop}</li>
                                ))}
                            </ul>
                        </div>
                        <div className="statistics-section">
                            <h3>Common Properties</h3>
                            <ul>
                                {jsonStatisticsData.common_properties.map((prop, index) => (
                                    <li key={index}>{prop}</li>
                                ))}
                            </ul>
                        </div>
                    </div>
                )}

                {/* Buttons for imports */}
                {compareData && (
                    <div className="import-buttons">
                    <button onClick={handleImportHTML}>Import HTML with Data</button>
                    <button onClick={handleImportJSON_LD}>Import JSON-LD with Data</button>
                    <button onClick={handleImportStatistics}>Import Statistics</button>
                </div>)}
            </div>
        </div>
    );
};

export default Compare;