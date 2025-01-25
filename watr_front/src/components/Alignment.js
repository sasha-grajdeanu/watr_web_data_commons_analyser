import React, {useState } from "react";
import "../styles/Alignment.css";
import "chart.js/auto";

const Alignment = () => {
    const [selectedTarget, setSelectedTarget] = useState("");

    const sourceOptions = [
        "schema.org", "DBPedia"
    ];


    
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

                <button >Align</button>
            </div>

        </div>
    );
};

export default Alignment;
