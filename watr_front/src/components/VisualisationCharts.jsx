import React from "react";
import { Pie } from "react-chartjs-2";

const VisualisationCharts = ({ data }) => {
    const { unique_entities, ...chartsData } = data; // Extract unique_entities and the rest for charts

    // Convert JSON data into chart datasets dynamically
    const chartData = Object.entries(chartsData).map(([key, value]) => {
        const labels = Object.keys(value);
        const values = Object.values(value);

        return {
            label: key,
            data: {
                labels,
                datasets: [
                    {
                        label: key,
                        data: values,
                        backgroundColor: labels.map(
                            (_, i) => `hsl(${(i * 360) / labels.length}, 70%, 60%)`
                        ), // Generate unique colors
                    },
                ],
            },
        };
    });

    return (
        <div>
            <h2>Statistics about your query</h2>

            {/* Display unique entities information */}
            {unique_entities && (
                <div style={{ marginBottom: "20px", padding: "10px", backgroundColor: "#f9f9f9", border: "1px solid #ddd" }}>
                    <h3>Number of Unique Entities: {unique_entities}</h3>
                </div>
            )}

            {/* Render a Pie chart for each dataset */}
            <div style={{ display: "flex", flexWrap: "wrap", gap: "20px" }}>
                {chartData.map((chart, index) => (
                    <div key={index} style={{ width: "400px", margin: "20px auto" }}>
                        <h3>{chart.label}</h3>
                        <Pie data={chart.data} />
                    </div>
                ))}
            </div>
        </div>
    );
};

export default VisualisationCharts;
