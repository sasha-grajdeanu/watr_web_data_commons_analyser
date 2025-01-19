import React, { useState } from "react";
import "../styles/Classification.css"; 
import { Bar } from "react-chartjs-2"; 
import "chart.js/auto";

const Classification = () => {
    const [selectedClass, setSelectedClass] = useState("");
    const [selectedProperty, setSelectedProperty] = useState("");
    const [results, setResults] = useState([]); 
    const [chartData, setChartData] = useState(null); 

    // Example class, property
    const classOptions = ["AdministrativeArea", "Place", "Movie"];
    const propertyOptions = ["containsPlace", "schema:author", "schema:datePublished"];

    // Simulate fetching results (replace with actual backend calls)
    const handleClassify = async () => {
        try{
            console.log(selectedClass);
            console.log(selectedProperty);
            const response = await fetch("http://localhost:5000/api/classify",{
                method: "POST",
                headers: {
                    "Content-Type": "application/json", 
                },
                body: JSON.stringify({
                    class: selectedClass,
                    property: selectedProperty,
                }),
            });

            if(!response.ok){
                throw new Error("API call failed");
            }

            const data = await response.json();
            setResults(data);

            const labels = data.map((item) => item.propertyValue);
            const counts = data.map((item) => item.count);


            setChartData({
                labels,
                datasets: [
                    {
                        label: "Count of Entities",
                        data: counts,
                        backgroundColor: ["#4caf50", "#2196f3", "#ff5722"],
                        borderWidth: 1,
                    },
                ],
            });
        }catch(error){
            console.error("Error fetching classification data: ", error);
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

                {chartData && (
                    <div className="chart-container">
                        <Bar data={chartData} />
                    </div>
                )}

                {results.length > 0 ? (
                    <table className="results-table">
                        <thead>
                            <tr>
                                <th>Subject</th>
                                <th>Predicate</th>
                                <th>Object</th>
                            </tr>
                        </thead>
                        <tbody>
                            {results.map((item, index) => (
                                <tr key={index}>
                                    <td>{item.subject}</td>
                                    <td>{item.predicate}</td>
                                    <td>{item.object}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                ) : (
                    <p>No results to display.</p>
                )}
            </div>
        </div>
    );
};

export default Classification;
