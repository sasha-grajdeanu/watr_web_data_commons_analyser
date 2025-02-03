import { useState } from "react";
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
import VisualisationCharts from "../utils_components/Visualize_charts";
import ChartWithPagination from "../utils_components/Visualize_charts";
import DataVisualization from "../utils_components/Visualize_charts";

export default function Visualize() {
  const [selectedClass, setSelectedClass] = useState("");
  const [haveLimit, setHaveLimit] = useState("false");
  const [limit, setLimit] = useState("");
  const [loading, setLoading] = useState(false);

  const [currentView, setCurrentView] = useState(true);

  const [graphData, setGraphData] = useState("");
  const [statistics, setStatistics] = useState("");
  const [showStatistics, setShowStatistics] = useState(false);

  const [errors, setErrors] = useState({
    selectedClass: "",
    limit: "",
  });

  const importAsHTML = async () => {
    if (!showStatistics) {
      alert("Please submit the forms!");
      return;
    }

    try {
      const url = `${uriRequest}visualise/html?class=${selectedClass}&limit=${haveLimit}${
      haveLimit === "true" ? `&count_limit=${limit}` : ""
    }`;

      const response = await fetch(url, { method: "GET" });

      if (!response.ok) {
        throw new Error("Failed to fetch the HTML file.");
      }

      const htmlData = await response.text();

      // Create a blob and trigger download
      const blob = new Blob([htmlData], { type: "text/html" });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = `Visualize_${selectedClass}_data.html`; // Name of the downloaded file
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
      const url = `${uriRequest}visualise/json_ld?class=${selectedClass}&limit=${haveLimit}${
      haveLimit === "true" ? `&count_limit=${limit}` : ""
    }`;

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
      link.download = `Visualize_${selectedClass}_data.jsonld`; // Name of the downloaded file
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error("Error importing JSON-LD:", error);
      alert("Error", error);
      return;
    }
  };

  const importStatistics = async () => {
    if (!showStatistics) {
      alert("Please submit the forms!");
      return;
    }

    try {
      const url = `${uriRequest}visualise/download_statistics?class=${selectedClass}&limit=${haveLimit}${
      haveLimit === "true" ? `&count_limit=${limit}` : ""
    }`;

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
      link.download = `Visualize_${selectedClass}_statistics.jsonld`; // Name of the downloaded file
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error("Error importing Statistics:", error);
      alert("Error", error);
      return;
    }
  };

  const importFunctionalities = [
    { name: "Export as HTML", action: importAsHTML },
    { name: "Export as JSON-LD", action: importAsJSONLD },
    { name: "Export statistics", action: importStatistics },
  ];

  const handleSubmit = () => {
    let newErrors = {};
    if (!selectedClass) {
      newErrors.selectedClass = "Please select a class";
    }
    if (haveLimit === "true" && (!limit || limit <= 0)) {
      newErrors.limit = "Please enter a valid limit.";
    }

    setErrors(newErrors);

    return Object.keys(newErrors).length === 0;
  };

  const fetchGraphData = async (selectedClass, haveLimit, limit) => {
    const graphUrl = `${uriRequest}visualise/graph?class=${selectedClass}&limit=${haveLimit}${
      haveLimit === "true" ? `&count_limit=${limit}` : ""
    }`;
    const response = await fetch(graphUrl, { method: "GET" });
    if (!response.ok) {
      throw new Error("Graph API call failed");
    }
    return response.text();
  };

  const fetchStatisticsData = async (selectedClass, haveLimit, limit) => {
    const statsUrl = `${uriRequest}visualise/statistics?class=${selectedClass}&limit=${haveLimit}${
      haveLimit === "true" ? `&count_limit=${limit}` : ""
    }`;
    const response = await fetch(statsUrl, { method: "GET" });
    if (!response.ok) {
      throw new Error("Statistics API call failed");
    }
    return response.json();
  };
  const handleVisualise = async () => {
    if (!handleSubmit()) {
      return;
    }

    try {
      setLoading(true);
      setShowStatistics(false);
      const [graphData, statsData] = await Promise.all([
        fetchGraphData(selectedClass, haveLimit, limit),
        fetchStatisticsData(selectedClass, haveLimit, limit),
      ]);

      setGraphData(graphData);
      setStatistics(statsData);
      setLoading(false);
      setShowStatistics(true);
      console.log("Graph data:", graphData);
    } catch (error) {
      console.error("Error during visualization process:", error);
    }
  };

  const classes = classOptions;

  return (
    <div className="bg-radial from-violet-200 from-40% to-pink-200 min-h-[calc(100vh-64px)] w-full flex flex-col items-center">
      <h1 className="text-3xl font-semibold p-3 mt-2">Visualisation</h1>
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
            <Field className="flex flex-col w-full px-1 pb-2">
              <Label htmlFor="limit" className="py-1">
                To have a limit:
              </Label>
              <Select
                id="limit"
                value={haveLimit}
                className="w-full bg-watr-400 p-2 rounded-md"
                onChange={(e) => setHaveLimit(e.target.value)}
              >
                <option id="id_1" value="false">No</option>
                <option id="id_2" value="true">Yes</option>
              </Select>
            </Field>
            {haveLimit === "true" && (
              <Field className="flex flex-col w-full px-1 pb-2">
                <Label htmlFor="limit_count" className="py-1">
                  Limit:
                </Label>
                <Input
                  id="limit_count"
                  type="number"
                  value={limit}
                  className="w-full bg-watr-400 p-2 rounded-md"
                  onChange={(e) => setLimit(e.target.value)}
                  min="1"
                  placeholder="Enter a limit"
                />
                {errors.limit && <ErrorsMessage errorMessage={errors.limit} />}
              </Field>
            )}
            <Field className="flex flex-col w-full pt-2 px-1">
              <Button
                onClick={handleVisualise}
                className="rounded bg-watr-200 hover:bg-watr-100 text-xl py-2 duration-300 text-white w-full"
              >
                Visualize
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
            <div className="w-full h-full flex flex-col items-center justify-center">
             <Spinner size="lg" color="watr" />

            </div>
          )}
          {showStatistics ? (
            !currentView ? (
              <div className="flex flex-grow-1 flex-col items-center justify-around lg:h-full h-96 w-full">
                {/* Your graph component goes here */}
                {graphData && (
          <GraphMLViewer graphMLData={graphData}/>)}
              </div>
            ) : (
              <div className="flex flex-grow-1 flex-col items-center justify-around lg:h-full h-96 w-full">
                {/* Your statistics component goes here */}
                <DataVisualization data={statistics} />
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
