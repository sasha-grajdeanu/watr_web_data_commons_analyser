import React, { useEffect, useState, useRef } from "react";
import "../styles/Classification.css";
import "chart.js/auto";
import { Network, DataSet } from "vis-network/standalone/umd/vis-network.min.js";

const Classification = () => {
    const [selectedClass, setSelectedClass] = useState("");
    const [selectedProperty, setSelectedProperty] = useState("");
    const [results, setResults] = useState([]);
    const [moreStats, setMoreStats] = useState([]);
    const [propertyOptions, setPropertyOptions] = useState([]);
    const [graphMLData, setGraphMLData] = useState("");
    const graphContainer = useRef(null);
    const [graphFile, setGraphFile] = useState("");
    const [uniqueGraphFile, setUniqueGraphFile] = useState("");

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
            const response = await fetch(`http://localhost:5000/api/classify/stats?class=${selectedClass}&property=${selectedProperty}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },  
            });

            if (!response.ok) {
                throw new Error("API call failed");
            }

            const data = await response.json();
            setResults(data.data);
            setMoreStats(data.unique_data);
            setGraphFile(data.graph_file);
            setUniqueGraphFile(data.unique_graph_file);

            const graphmlResponse = await fetch(`http://localhost:5000/api/classify/graph?class=${selectedClass}&property=${selectedProperty}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
               
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

    const handleDownload = async (fileName) => {
        try {
            const response = await fetch(`http://localhost:5000/api/download-stats?graph_file=${encodeURIComponent(fileName)}`);
            if (!response.ok) {
                throw new Error("Failed to download file");
            }
    
            const blob = await response.blob();
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = 'graph_data.ttl';  
            link.click();  
        } catch (error) {
            console.error("Error downloading file:", error);
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
                <h2>Statistics</h2>
                {moreStats.length > 0 ? (
                <div>
                    <div className="download-buttons">
                        <p>Download stats:</p>
                        <button onClick={() => handleDownload(graphFile)}>Download File 1</button>
                        <button onClick={() => handleDownload(uniqueGraphFile)}>Download File 2</button>
                    </div>
                    <div className="stats-summary">
                        <p><strong>Unique Objects Count:</strong> {moreStats.length}</p>
                        {
                            moreStats.map((item, index) => (
                                <p id="stats-summary-p" key={index}>
                                    {item.uniqueSubject} : {item.numberOfOccurrences}
                                </p>
                            ))
                        }
                    </div>
                </div>
                ) : (
                    <p>No stats to display;</p>
                )}
                
                {results.length > 0 ? (
                    <table className="results-table">
                        <thead>
                            <tr>
                                <th>Initial Subject</th>
                                <th>Initial Predicate</th>
                                <th>Number of Levels</th>
                            </tr>
                        </thead>
                        <tbody>
                            {results.map((item, index) => (
                                <tr key={index}>
                                    <td>{item.initialSubject}</td>
                                    <td>{item.initialPredicate}</td>
                                    <td>{item.numberOfLevels}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                ) : (
                    <p>No results to display.</p>
                )}
            </div>

            <div ref={graphContainer} className="graph-container"></div>
        </div>
    );
};

export default Classification;
