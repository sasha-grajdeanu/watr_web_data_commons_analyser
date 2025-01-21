import React, { useEffect, useState } from "react";
import "../styles/Classification.css"; 
import { Bar } from "react-chartjs-2"; 
import "chart.js/auto";

const Classification = () => {
    const [selectedClass, setSelectedClass] = useState("");
    const [selectedProperty, setSelectedProperty] = useState("");
    const [results, setResults] = useState([]); 
    const [chartData, setChartData] = useState(null); 
    const [propertyOptions, setPropertyOptions] = useState([]);

    // Example class, property
    const classOptions = [
        "AdministrativeArea", "Airport", "Answer", "Book", "City", "ClaimReview", "CollegeOrUniversity",
        "Continent", "Country", "CreativeWork", "Dataset", "EducationalOrganization", "Event", "FAQPage", "GeoCoordinates", 
        "GovernmentOrganization", "Hospital", "Hotel", "JobPosting", "LakeBodyOfWater", "LandmarksOrHistoricalBuildings", 
        "Language", "Library", "LocalBusiness", "Mountain", "Movie", "Museum", "MusicAlbum", "MusicRecording", "Organization",
        "Painting", "Park", "Person", "Place", "Product", "QAPage", "Question", "RadioStation", "Recipe", "Restaurant", "RiverBodyOfWater",
        "School", "SearchAction", "ShoppingCenter", "SkiResort", "SportsEvent", "SportsTeam", "StadiumOrArena", "TVEpisode", "TelevisionStation"
    ];
    
    // const propertyOptions = ["containsPlace", "schema:author", "schema:datePublished"];

    useEffect(() => {
        if(selectedClass){
            fecthProperties(selectedClass);
        }
    }, [selectedClass]);


    const fecthProperties = async (rdfClass) => {
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
    }


    const handleClassify = async () => {
        try {
            console.log(selectedClass);
            console.log(selectedProperty);
            const response = await fetch("http://localhost:5000/api/classify", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json", 
                    "Accept": "*/*"
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

            // Prepare data for the chart
            const labels = data.map((item) => item.initial_subject);  // Assuming initial_subject can serve as the label
            const counts = data.map((item) => item.blankNode ? 1 : 0);  // Example for counting blankNodes

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
        } catch (error) {
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

                {/* {chartData && (
                    <div className="chart-container">
                        <Bar data={chartData} />
                    </div>
                )} */}

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
        </div>
    );
};

export default Classification;
