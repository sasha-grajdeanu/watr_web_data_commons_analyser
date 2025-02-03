import React, {useState } from "react";
import "../styles/Alignment.css";
import "chart.js/auto";

const Alignment = () => {
    const [selectedTarget, setSelectedTarget] = useState("");
    const [results, setResults] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [stats, setStats] = useState(0.0);
    const [graphFile, setGraphFile] = useState("");

    const sourceOptions = [
        "schema.org", "DBPedia"
    ];

    const handleClassify = async () => {
        setIsLoading(true);
        
        if(!selectedTarget){
            alert("Please select an ontology for aligning.");
            return;
        }


        try{
            const response = await fetch(`http://localhost:5000/api/align/table?target=${selectedTarget}`,
                {
                    method: "GET",
                    headers:{
                        "Content-Type": "application/json",
                    },
                    
                }
            );

            if(!response.ok){
                throw new Error("API call failed");
            }

            const data = await response.json();
            setResults(data);

            const statsResponse = await fetch(`http://localhost:5000/api/align/statistics?target=${selectedTarget}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
                
            });

            if (!statsResponse.ok) {
                throw new Error("API call failed");
            }

            const statsData = await statsResponse.json();
            setStats(statsData.average_measure);

            const statsGraphResponse = await fetch(`http://127.0.0.1:5000/api/align/statistics/graph?target=${selectedTarget}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
            });

            if (!statsGraphResponse.ok) {
                throw new Error("API call failed");
            }
            const statsGraphData = await statsGraphResponse.text();
            setGraphFile(statsGraphData);
        }
        catch (error){
            console.error("Error fetching alignment data:", error);
        }
        finally{
            setIsLoading(false);
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
        <div className="alignment-page">
            <h1>Alignment</h1>
            <div className="input-panel">
                <h2>Input Panel</h2>
                <label htmlFor="target-ontology">Target Ontology:</label>
                <select
                    id="target-ontology"
                    value={selectedTarget}
                    onChange={(e) => setSelectedTarget(e.target.value)}>

                        <option value="">Select a Target Ontology</option>
                        {sourceOptions.map((option, index) => (
                            <option key={index} value={option}>
                                {option}
                            </option>
                        ))}

                </select>

                <button onClick={handleClassify}>Align</button>
            </div>
            
            <div className="results-area">
                <h2>Statistics</h2>
                    {stats ? (
                    <div>
                        <div className="download-buttons">
                            <p>Download stats:</p>
                            <button onClick={() => handleDownload(graphFile)}>Download Statistics</button>
                        </div>
                        <div className="stats-summary">
                            <p><strong>Average Measure:</strong> {stats}</p>
                        </div>
                    </div>
                    ) : (
                        <p>No stats to display.</p>
                    )}
                <h2>Alignment Results</h2>
                {
                    !isLoading ? (
                        results.length > 0 ? (
                            <table className="results-table"> 
                                <thead>
                                    <tr>
                                        <th>Original Entity</th>
                                        <th>Aligned Entity</th>
                                        <th>Measure</th>
                                        <th>Relation</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {
                                        results.map((item, index) => (
                                            <tr key={index}>
                                                <td>{item.originalEntity}</td>
                                                <td>{item.alignedEntity}</td>
                                                <td>{item.measure}</td>
                                                <td>{item.relation}</td>
                                            </tr>
                                        ))
                                    }
                                </tbody>
                            </table>
                        ) : (
                            <p>No results to display.</p>
                        )
                    ) : (
                        <p>Loading...</p>
                    )
                }

            </div>
        </div>
    );
};

export default Alignment;
