import { useEffect, useState } from "react";
import { classOptions, uriRequest } from "../utils";
import {
  Label,
  Legend,
  Select,
  Field,
  Fieldset,
  Input,
  Button,
  Switch,
} from "@headlessui/react";
import ErrorsMessage from "../utils_components/Errors";
import ImportButtons from "../utils_components/ImportButtons";
import sadcat from "../assets/sadsadfatcat.jpg";
import SwitchDisplay from "../utils_components/Switch";
import Spinner from "../utils_components/Loading";
import GraphMLViewer from "../utils_components/GraphComponent";
import StatisticsCard from "../utils_components/ClassifyStatistics";

export default function Classify() {
  const [selectedClass, setSelectedClass] = useState("");
  const [selectedProperties, setSelectedProperties] = useState("");
  const [propertyOptions, setPropertyOptions] = useState([]);
  const [loading, setLoading] = useState(false);

  const [currentView, setCurrentView] = useState(true);

  const [graphData, setGraphData] = useState("");
  const [results, setResults] = useState([]);
  const [moreStats, setMoreStats] = useState([]);
  const [graphFile, setGraphFile] = useState("");
  const [uniqueGraphFile, setUniqueGraphFile] = useState("");
  const [showStatistics, setShowStatistics] = useState(false);

  const [errors, setErrors] = useState({
    selectedClass: "",
    selectedProperties: "",
  });

  const importAsHTML = async () => {
    if (!showStatistics) {
      alert("Please submit the forms!");
      return;
    }

    try {
      const url = `${uriRequest}classify/html?class=${selectedClass}&property=${selectedProperties}`;

      const response = await fetch(url, { method: "GET" });

      if (!response.ok) {
        throw new Error("Failed to fetch the HTML file.");
      }

      const htmlData = await response.text();

      // Create a blob and trigger download
      const blob = new Blob([htmlData], { type: "text/html" });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = `Classify_${selectedClass}_${selectedProperties}_data.html`; // Name of the downloaded file
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error("Error importing HTML:", error);
      alert("Error", error);
      return;
    }
  };

  const importAsJSONLD = async () => {
    if (!showStatistics) {
      alert("Please submit the forms!");
      return;
    }

    try {
      const url = `http://localhost:5000/api/classify/json_ld?class=${selectedClass}&property=${selectedProperties}`;

      const response = await fetch(url, { method: "GET" });
      if (!response.ok) {
        throw new Error("Failed to fetch the JSON-LD file.");
      }

      const jsonLDData = await response.text();

      // Create a blob and trigger download
      const blob = new Blob([JSON.stringify(jsonLDData, null, 2)], {
        type: "application/ld+json",
      });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = `Classify_${selectedClass}_${selectedProperties}_data.jsonld`; // Name of the downloaded file
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error("Error importing JSON-LD:", error);
      alert("Error", error);
      return;
    }
  };

  const fetchProperties = async (rdfClass) => {
    try {
      const response = await fetch(
        `${uriRequest}/classify/properties?class=${rdfClass}`
      );
      if (!response.ok) {
        throw new Error("Failed to fetch properties");
      }
      const data = await response.json();
      setPropertyOptions(data);
    } catch (error) {
      console.error("Error fetching properties:", error);
    }
  };

  useEffect(() => {
    if (selectedClass) {
        console.log("Fetching properties for class: ", selectedClass);
        fetchProperties(selectedClass);
    }
}, [selectedClass]);

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

    const importLevels = async () => {
        handleDownload(graphFile);
    }

    const importSubjects = async () => {
        handleDownload(uniqueGraphFile);
    }

  const importFunctionalities = [
    { name: "Download Levels Distribution Statistics", action: importLevels },
    { name: "Download Unique Subjects Distribution Statistics", action: importSubjects },
    { name: "Export as HTML", action: importAsHTML },
    { name: "Export as JSON-LD", action: importAsJSONLD },
  ];

  const handleSubmit = () => {
    let newErrors = {};
    if (!selectedClass) {
      newErrors.selectedClass = "Please select a class";
    }
    if (!selectedProperties) {
        newErrors.selectedProperties = "Please select a property";
    }

    setErrors(newErrors);

    return Object.keys(newErrors).length === 0;
  };

  const fetchGraphData = async (selectedClass, selectedProperty) => {
    const graphmlResponse = await fetch(
      `http://localhost:5000/api/classify/graph?class=${selectedClass}&property=${selectedProperty}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    if (!graphmlResponse.ok) {
      throw new Error("Failed to fetch GraphML data");
    }

    const graphMLData = await graphmlResponse.text();
    setGraphData(graphMLData);
  };

  const fetchStatisticsData = async (selectedClass, selectedProperties) => {
    const response = await fetch(
      `${uriRequest}classify/statistics?class=${selectedClass}&property=${selectedProperties}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    if (!response.ok) {
      throw new Error("API call failed");
    }

    const data = await response.json();
    setResults(data);
    setMoreStats(data.unique_data);
    console.log("Data", data);
  };

  const fetchStatisticsDataFiles = async (selectedClass, selectedProperties) => {
    const response = await fetch(
      `${uriRequest}classify/statistics/graph?class=${selectedClass}&property=${selectedProperties}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    if (!response.ok) {
      throw new Error("API call failed");
    }

    const data = await response.json();
    setGraphFile(data.graph_file);
    setUniqueGraphFile(data.unique_graph_file);
    console.log("Data", data);
  };

  const handleVisualise = async () => {
    if (!handleSubmit()) {
      return;
    }

    try {
      setLoading(true);
      setShowStatistics(false);
      const [graphData, statistics, statisticsFiles] = await Promise.all([
        fetchGraphData(selectedClass, selectedProperties),
        fetchStatisticsData(
          selectedClass,
          selectedProperties
        ),
        fetchStatisticsDataFiles(selectedClass, selectedProperties),
      ]);
      setLoading(false);
      setShowStatistics(true);
    } catch (error) {
      console.error("Error during visualization process:", error);
    }
  };

  const classes = classOptions;

  return (
    <div className="bg-radial from-violet-200 from-40% to-pink-200 min-h-[calc(100vh-64px)] w-full flex flex-col items-center">
      <h1 className="text-3xl font-semibold p-3 mt-2">Classification</h1>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 w-full px-4 lg:my-auto mx:auto justify-center lg:h-128">
        <div className="flex flex-col w-full justify-around lg:justify-center col-span-1 bg-transparent lg:p-4 h-full">
          <Fieldset className="flex flex-col items-center justify-center rounded-md border-watr-100 p-4 bg-watr-300 shadow-2xl">
            <Legend className="font-medium text-xl">Input panel</Legend>
            <Field className="flex flex-col w-full p-1">
              <Label htmlFor="class" className="py-1">
                Select a class:
              </Label>
              <Select
                id="class"
                value={selectedClass}
                className="w-full bg-watr-400 p-2 rounded-md font-montserrat"
                onChange={(e) => setSelectedClass(e.target.value)}
              >
                <option value="">Select a Class</option>
                {classes.map((option, index) => (
                  <option key={index} value={option}>
                    {option}
                  </option>
                ))}
              </Select>
              {errors.selectedClass && (
                <ErrorsMessage errorMessage={errors.selectedClass} />
              )}
            </Field>
            <Field className="flex flex-col w-full p-1">
              <Label htmlFor="properties" className="py-1">
                Select a property:
              </Label>
              <Select
                id="properties"
                value={selectedProperties}
                className="w-full bg-watr-400 p-2 rounded-md font-montserrat"
                onChange={(e) => setSelectedProperties(e.target.value)}
              >
                <option value="">Select a property</option>
                {propertyOptions.map((option, index) => (
                  <option key={index} value={option}>
                    {option}
                  </option>
                ))}
              </Select>
              {errors.selectedClass && (
                <ErrorsMessage errorMessage={errors.selectedProperties} />
              )}
            </Field>
            <Field className="flex flex-col w-full pt-2 px-1">
              <Button
                onClick={handleVisualise}
                className="rounded bg-watr-200 hover:bg-watr-100 text-xl py-2 duration-300 text-white w-full"
              >
                Classify
              </Button>
            </Field>

            {showStatistics && (
              <div className="w-full hidden lg:block">
                <ImportButtons importFunctionalities={importFunctionalities} />
              </div>
            )}
          </Fieldset>
        </div>
        <div
          className={`lg:flex flex-col items-center justify-center col-span-1 lg:col-span-2 bg-watr-300 p-4 rounded-md shadow-2xl`}
        >
          <div
            className={`w-full justify-end mb-4 ${
              !showStatistics ? "hidden" : "flex"
            }`}
          >
            <SwitchDisplay
              checked={currentView}
              onChange={setCurrentView}
              name_one="Graph"
              name_two="Statistics"
            />
          </div>
          {loading && (
            <div className="w-full lg:h-full h-96 flex flex-col items-center justify-center">
              <Spinner size="lg" color="watr" />
            </div>
          )}
          {showStatistics ? (
            !currentView ? (
              <div className="flex flex-grow-1 flex-col items-center justify-around lg:h-full h-96 w-full">
                {/* Your graph component goes here */}
                {graphData && <GraphMLViewer graphMLData={graphData} />}
              </div>
            ) : (
              <div className="flex flex-grow-1 flex-col items-center justify-around lg:h-full w-full">
                {console.log(results)}
                <StatisticsCard data={results} />
              </div>
            )
          ) : (
            <div
              className={`w-full h-full flex-col items-center justify-center ${
                loading ? "hidden" : "flex"
              }`}
            >
              <img src={sadcat} alt="sad cat" className="w-78" />
              <p>If you submit, i'll show you some informations.</p>
            </div>
          )}
        </div>
        {showStatistics && (
          <div className="w-full block lg:hidden mb-6">
            <ImportButtons importFunctionalities={importFunctionalities} />
          </div>
        )}
      </div>
    </div>
  );
}
