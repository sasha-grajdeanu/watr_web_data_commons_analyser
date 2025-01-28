import React, { useEffect, useState, useRef } from "react";
import "chart.js/auto";
import { Network, DataSet } from "vis-network/standalone/umd/vis-network.min.js";
import "../styles/Visualisation.css";
import VisualisationCharts from "./VisualisationCharts";

const Visualize = () => {
    const [selectedClass, setSelectedClass] = useState("");
    const [limit, setLimit] = useState("false"); // Default to "false"
    const [count_limit, setCountLimit] = useState("");
    const [graphMLData, setGraphMLData] = useState("");
    const [jsonStatisticsData, setJsonStatisticsData] = useState("");
    const [showStatistics, setShowStatistics] = useState(false); // State to control visibility of statistics div
    const graphContainer = useRef(null);

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

    useEffect(() => {
        if (graphMLData) {
            try {
                const parser = new DOMParser();
                const xmlDoc = parser.parseFromString(graphMLData, "application/xml");

                const nodes = [];
                const edges = [];

                const graphmlNodes = xmlDoc.getElementsByTagName("node");
                for (let i = 0; i < graphmlNodes.length; i++) {
                    const node = graphmlNodes[i];
                    const id = node.getAttribute("id");
                    const label = node.getElementsByTagName("data")[0]?.textContent || id;
                    nodes.push({ id, label });
                }

                const graphmlEdges = xmlDoc.getElementsByTagName("edge");
                for (let i = 0; i < graphmlEdges.length; i++) {
                    const edge = graphmlEdges[i];
                    const source = edge.getAttribute("source");
                    const target = edge.getAttribute("target");

                    const dataElements = edge.getElementsByTagName("data");
                    let label = "";
                    if (dataElements.length > 0) {
                        label = dataElements[0].textContent;
                    }

                    edges.push({ from: source, to: target, label });
                }

                const data = {
                    nodes: new DataSet(nodes),
                    edges: new DataSet(edges),
                };

                const options = {
                    physics: { enabled: true },
                    nodes: { shape: "dot", size: 10 },
                };

                new Network(graphContainer.current, data, options);
            } catch (error) {
                console.error("Error parsing GraphML data: ", error);
            }
        }
    }, [graphMLData]);


const handleVisualise = async () => {
    if (!selectedClass) {
        alert("Please select a class to visualize");
        return;
    }

    try {
        // Fetch GraphML Data
        const graphUrl = `http://localhost:5000/api/visualise/graph?class=${selectedClass}&limit=${limit}${
            limit === "true" ? `&count_limit=${count_limit}` : ""
        }`;
        const graphResponse = await fetch(graphUrl, {
            method: "GET",
        });
        if (!graphResponse.ok) {
            throw new Error("Graph API call failed");
        }
        const graphData = await graphResponse.text();
        setGraphMLData(graphData);

        // Fetch Statistics Data
        const statsUrl = `http://localhost:5000/api/visualise/statistics?class=${selectedClass}&limit=${limit}${
            limit === "true" ? `&count_limit=${count_limit}` : ""
        }`;
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
    if (!selectedClass) {
        alert("Please select a class first!");
        return;
    }

    try {
        const url = `http://localhost:5000/api/visualise/html?class=${selectedClass}&limit=${limit}${
            limit === "true" ? `&count_limit=${count_limit}` : ""
        }`;

        const response = await fetch(url, { method: "GET" });

        if (!response.ok) {
            throw new Error("Failed to fetch the HTML file.");
        }

        const htmlData = await response.text();

        // Create a blob and trigger download
        const blob = new Blob([htmlData], { type: "text/html" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = `${selectedClass}_data.html`; // Name of the downloaded file
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } catch (error) {
        console.error("Error importing HTML:", error);
    }
};

const handleImportJSON_LD = async () => {
    if (!selectedClass) {
        alert("Please select a class first!");
        return;
    }

    try {
        const url = `http://localhost:5000/api/visualise/json_ld?class=${selectedClass}&limit=${limit}${
            limit === "true" ? `&count_limit=${count_limit}` : ""
        }`;

        const response = await fetch(url, { method: "GET" });

        if (!response.ok) {
            throw new Error("Failed to fetch the JSON-LD file.");
        }

        const jsonLDData = await response.json();

        // Create a blob and trigger download
        const blob = new Blob([JSON.stringify(jsonLDData, null, 2)], { type: "application/ld+json" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = `${selectedClass}_data.jsonld`; // Name of the downloaded file
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } catch (error) {
        console.error("Error importing JSON-LD:", error);
    }
};

const handleImportStatistics = async () => {
    if (!selectedClass) {
        alert("Please select a class first!");
        return;
    }

    try {
        const url = `http://localhost:5000/api/visualise/download_statistics?class=${selectedClass}&limit=${limit}${
            limit === "true" ? `&count_limit=${count_limit}` : ""
        }`;

        const response = await fetch(url, { method: "GET" });

        if (!response.ok) {
            throw new Error("Failed to fetch the JSON-LD file.");
        }

        const jsonLDData = await response.json();

        // Create a blob and trigger download
        const blob = new Blob([JSON.stringify(jsonLDData, null, 2)], { type: "application/ld+json" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = `${selectedClass}_statistics.jsonld`; // Name of the downloaded file
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } catch (error) {
        console.error("Error importing JSON-LD:", error);
    }
};
    return (
        <div className="visualisation-page">
            <h1>Visualisation</h1>
            <div className="input-panel">
                <h2>Input Panel</h2>

                {/* Class Select Dropdown */}
                <label htmlFor="class">Class:</label>
                <select
                    id="class"
                    className="input-field"
                    value={selectedClass}
                    onChange={(e) => setSelectedClass(e.target.value)}
                >
                    <option value="">Select a Class</option>
                    {classOptions.map((option, index) => (
                        <option key={index} value={option}>
                            {option}
                        </option>
                    ))}
                </select>

                {/* Limit Select Dropdown */}
                <label htmlFor="limit">Limit:</label>
                <select
                    id="limit"
                    className="input-field"
                    value={limit}
                    onChange={(e) => setLimit(e.target.value)}
                >
                    <option value="false">False</option>
                    <option value="true">True</option>
                </select>

                {/* Count Limit Input (Conditionally Rendered) */}
                {limit === "true" && (
                    <>
                        <label htmlFor="count_limit">Count Limit:</label>
                        <input
                            id="count_limit"
                            className="input-field"
                            type="number"
                            value={count_limit}
                            onChange={(e) => setCountLimit(e.target.value)}
                            min="1"
                            placeholder="Enter count limit"
                        />
                    </>
                )}

                {/* Visualize Button */}
                <button onClick={handleVisualise}>Visualize</button>

                {/* Graph Container */}
                <div ref={graphContainer} style={{ height: "500px", border: "1px solid black" }}></div>

                {/* Statistics Div (Conditionally Rendered) */}
                {showStatistics && (
                    <VisualisationCharts data={jsonStatisticsData}/>// Pass the statistics data to the component
                )}

                {/* Buttons for imports */}
                <div className="import-buttons">
                    <button onClick={handleImportHTML}>Import HTML with Data</button>
                    <button onClick={handleImportJSON_LD}>Import JSON-LD with Data</button>
                    <button onClick={handleImportStatistics}>Import Statistics</button>
                </div>
            </div>
        </div>
    );
};

export default Visualize;