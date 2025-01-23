import React, { useEffect, useState, useRef } from "react";
import "chart.js/auto";
import { Network, DataSet } from "vis-network/standalone/umd/vis-network.min.js";

const Visualize = () => {
    const [selectedClass, setSelectedClass] = useState("");
    const [graphMLData, setGraphMLData] = useState("");
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
    
                        edges.push({ from: source, to: target, label});
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
            if(!selectedClass){
                alert("Please select a class to visualize");
                return;
            }
            try{
                const response = await fetch(`http://localhost:5000/api/visualise?class=${selectedClass}`, {
                    method: "GET",
                });
                if (!response.ok) {
                    throw new Error("API call failed");
                }
                const data = await response.text();
                setGraphMLData(data);
            }
            catch (error) {
                console.error("Error fetching classification data:", error);
            }
        };

        return (
            <div className="classification-page">
            <h1>Visualisation</h1>
            <div className="input-panel">
                <h2>Input Panel</h2>
                <label htmlFor="class">Class:</label>
                <select
                    id="class"
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

                <button onClick={handleVisualise}>Visualize</button>
                <div ref={graphContainer} style={{ height: "500px", border: "1px solid black" }}></div>
            </div>
        </div>
        )
}

export default Visualize;