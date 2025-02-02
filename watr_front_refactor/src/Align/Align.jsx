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
import AlignTableWithPagination from "../utils_components/AlignTable";

export default function Align() {
  const [selectedOntology, setSelectedOntology] = useState("");
  const [loading, setLoading] = useState(false);

  const [currentView, setCurrentView] = useState(true);
  const [results, setResults] = useState([]);
  const [stats, setStats] = useState("");
  const [graphFile, setGraphFile] = useState("");

  const [showStatistics, setShowStatistics] = useState(false);

  const [errors, setErrors] = useState({
    selectedOntology: "",
  });

  const sourceOptions = ["schema.org", "DBPedia"];

  const handleDownload = async (fileName) => {
    try {
      const response = await fetch(
        `http://localhost:5000/api/download-stats?graph_file=${encodeURIComponent(
          fileName
        )}`
      );
      if (!response.ok) {
        throw new Error("Failed to download file");
      }

      const blob = await response.blob();
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = "graph_data.ttl";
      link.click();
    } catch (error) {
      console.error("Error downloading file:", error);
    }
  };

  const importLevels = async () => {
    handleDownload(graphFile);
  };


  const importFunctionalities = [
    { name: "Download stats", action: importLevels }
  ];

  const handleSubmit = () => {
    let newErrors = {};
    if (!selectedOntology) {
      newErrors.selectedOntology = "Please select an ontology";
    }

    setErrors(newErrors);

    return Object.keys(newErrors).length === 0;
  };

  const fetchData = async (selectedTarget) => {
    const response = await fetch(
      `http://localhost:5000/api/align/table?target=${selectedTarget}`,
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
    setResults(data.results);
    console.log(results);
  };

  const fetchStatisticsData = async (selectedTarget) => {
    const response = await fetch(
      `http://localhost:5000/api/align/stats?target=${selectedTarget}`,
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

    const statsData = await response.json();
    setStats(statsData.stats);
    setGraphFile(statsData.graph_file);
  };

  const handleVisualise = async () => {
    if (!handleSubmit()) {
      return;
    }

    try {
      setLoading(true);
      setShowStatistics(false);
      const graphData = await fetchData(selectedOntology);
      const statistics = await fetchStatisticsData(selectedOntology);
      setLoading(false);
      setShowStatistics(true);
    } catch (error) {
      console.error("Error during visualization process:", error);
    }
  };


  return (
    <div className="bg-radial from-violet-200 from-40% to-pink-200 min-h-[calc(100vh-64px)] w-full flex flex-col items-center">
      <h1 className="text-3xl font-semibold p-3 mt-2">Alignment</h1>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 w-full px-4 lg:my-auto mx:auto justify-center lg:h-128">
        <div className="flex flex-col w-full justify-around lg:justify-center col-span-1 bg-transparent lg:p-4 h-full">
          <Fieldset className="flex flex-col items-center justify-center rounded-md border-watr-100 p-4 bg-watr-300 shadow-2xl">
            <Legend className="font-medium text-xl">Input panel</Legend>
            <Field className="flex flex-col w-full p-1">
              <Label htmlFor="ontology" className="py-1">
                Select an ontology:
              </Label>
              <Select
                id="ontology"
                value={selectedOntology}
                className="w-full bg-watr-400 p-2 rounded-md font-montserrat"
                onChange={(e) => setSelectedOntology(e.target.value)}
              >
                <option value="">Select an ontology</option>
                {sourceOptions.map((option, index) => (
                  <option key={index} value={option}>
                    {option}
                  </option>
                ))}
              </Select>
              {errors.selectedClass && (
                <ErrorsMessage errorMessage={errors.selectedOntology} />
              )}
            </Field>
            <Field className="flex flex-col w-full pt-2 px-1">
              <Button
                onClick={handleVisualise}
                className="rounded bg-watr-200 hover:bg-watr-100 text-xl py-2 duration-300 text-white w-full"
              >
                Align
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
          className={`${
            !showStatistics ? "hidden" : "flex"
          } lg:flex flex-col items-center justify-center col-span-1 lg:col-span-2 bg-watr-300 p-4 rounded-md shadow-2xl`}
        >
          {loading && (
            <div className="w-full h-full flex flex-col items-center justify-center">
              <Spinner size="lg" color="watr" />
            </div>
          )}
          {showStatistics ? (
            <div className="flex flex-grow-1 flex-col items-center justify-around lg:h-full w-full">
            {/* Your statistics component goes here */}
            <p><strong>Average Measure:</strong> {stats}</p>
            <AlignTableWithPagination data={results} />
          </div>
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
