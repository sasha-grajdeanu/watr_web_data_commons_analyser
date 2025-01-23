import React, { useEffect, useState, useRef } from "react";
import "../styles/Classification.css";
import "chart.js/auto";
import { Network, DataSet } from "vis-network/standalone/umd/vis-network.min.js";

const Classification = () => {
    const [selectedClass, setSelectedClass] = useState("");
    const [selectedProperty, setSelectedProperty] = useState("");
    const [results, setResults] = useState([]);
    const [propertyOptions, setPropertyOptions] = useState([]);
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
        if (selectedClass) {
            fetchProperties(selectedClass);
        }
    }, [selectedClass]);


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


    const fetchProperties = async (rdfClass) => {
        try {
            const response = await fetch(`http://localhost:5000/api/properties?class=${rdfClass}`);
            if (!response.ok) {
                throw new Error("Failed to fetch properties");
            }
            const data = await response.json();
            setPropertyOptions(data);
        } catch (error) {
            console.error("Error fetching properties:", error);
        }
    };


    const handleClassify = async () => {
        if (!selectedClass || !selectedProperty) {
            alert("Please select both a class and a property.");
            return;
        }

        try {
            const response = await fetch("http://localhost:5000/api/classify", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    class: selectedClass,
                    property: selectedProperty,
                }),
            });

            if (!response.ok) {
                throw new Error("API call failed");
            }

            const data = await response.json();
            setResults(data);

            const graphmlResponse = await fetch("http://localhost:5000/api/classify/graph", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    class: selectedClass,
                    property: selectedProperty,
                }),
            });

            if (!graphmlResponse.ok) {
                throw new Error("Failed to fetch GraphML data");
            }

            const graphMLData = await graphmlResponse.text();
            setGraphMLData(graphMLData);

        } catch (error) {
            console.error("Error fetching classification data:", error);
        }
    };


    return (
        <div className="classification-page">
            <h1>Classification</h1>
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

                <label htmlFor="property">Property:</label>
                <select
                    id="property"
                    value={selectedProperty}
                    onChange={(e) => setSelectedProperty(e.target.value)}
                >
                    <option value="">Select a Property</option>
                    {propertyOptions.map((option, index) => (
                        <option key={index} value={option}>
                            {option}
                        </option>
                    ))}
                </select>

                <button onClick={handleClassify}>Classify</button>
            </div>

            <div className="results-area">
                <h2>Results Area</h2>
                {results.length > 0 ? (
                    <table className="results-table">
                        <thead>
                            <tr>
                                <th>Subject</th>
                                <th>Predicate</th>
                                <th>BlankNode</th>
                                <th>Level 1 Predicate</th>
                                <th>Level 1 Object</th>
                                <th>Level 2 Predicate</th>
                                <th>Level 2 Object</th>
                                <th>Level 3 Predicate</th>
                                <th>Level 3 Object</th>
                            </tr>
                        </thead>
                        <tbody>
                            {results.map((item, index) => (
                                <tr key={index}>
                                    <td>{item.initial_subject}</td>
                                    <td>{item.initial_predicate}</td>
                                    <td>{item.blankNode}</td>
                                    <td>{item.level1_predicate || "N/A"}</td>
                                    <td>{item.level1_object || "N/A"}</td>
                                    <td>{item.level2_predicate || "N/A"}</td>
                                    <td>{item.level2_object || "N/A"}</td>
                                    <td>{item.level3_predicate || "N/A"}</td>
                                    <td>{item.level3_object || "N/A"}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                ) : (
                    <p>No results to display.</p>
                )}
            </div>

            <div ref={graphContainer} style={{ height: "500px", border: "1px solid black" }}></div>
        </div>
    );
};


export default Classification;