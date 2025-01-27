import React, {useState } from "react";
import "../styles/Alignment.css";
import "chart.js/auto";

const Alignment = () => {
    const [selectedTarget, setSelectedTarget] = useState("");
    const [results, setResults] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    const sourceOptions = [
        "schema.org", "DBPedia"
    ];

    const handleClassify = async () => {
        if(!selectedTarget){
            alert("Please select an ontology for aligning.");
            return;
        }

        setIsLoading(true);

        try{
            const response = await fetch("http://localhost:5000/api/align/table",
                {
                    method: "POST",
                    headers:{
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        target: selectedTarget
                    })
                }
            );

            if(!response.ok){
                throw new Error("API call failed");
            }

            const data = await response.json();
            setResults(data.results);
        }
        catch (error){
            console.error("Error fetching alignment data:", error);
        }
        finally{
            setIsLoading(false);
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
