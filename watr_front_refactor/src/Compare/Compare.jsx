import { useState } from "react";
import { classOptions, uriRequest } from "../utils";
import {
  Label,
  Legend,
  Select,
  Field,
  Fieldset,
  Button,
} from "@headlessui/react";
import ErrorsMessage from "../utils_components/Errors";
import ImportButtons from "../utils_components/ImportButtons";
import sadcat from "../assets/sadsadfatcat.jpg";
import SwitchDisplay from "../utils_components/Switch";
import Spinner from "../utils_components/Loading";
import TableWithPagination from "../utils_components/Table";
import CompareStatistics from "../utils_components/CompareStatistics";

export default function Compare() {
  const [selectedClassOne, setSelectedClassOne] = useState("");
  const [selectedClassTwo, setSelectedClassTwo] = useState("");
  const [loading, setLoading] = useState(false);

  const [currentView, setCurrentView] = useState(true);

  const [compareData, setCompareData] = useState("");
  const [statistics, setStatistics] = useState("");
  const [showStatistics, setShowStatistics] = useState(false);

  const [errors, setErrors] = useState({
    selectedClassOne: "",
    selectedClassTwo: "",
  });

  const importAsHTML = async () => {
    if (!showStatistics) {
      alert("Please submit the forms!");
      return;
    }

    try {
      const url = `${uriRequest}compare/html?class_one=${selectedClassOne}&class_two=${selectedClassTwo}`;

      const response = await fetch(url, { method: "GET" });

      if (!response.ok) {
        throw new Error("Failed to fetch the HTML file.");
      }

      const htmlData = await response.text();

      // Create a blob and trigger download
      const blob = new Blob([htmlData], { type: "text/html" });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = `Compare_${selectedClassOne}_${selectedClassTwo}_data.html`; // Name of the downloaded file
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
      const url = `${uriRequest}compare/json_ld?class_one=${selectedClassOne}&class_two=${selectedClassTwo}`;

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
      link.download = `Compare_${selectedClassOne}_${selectedClassTwo}_data.jsonld`; // Name of the downloaded file
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
      const url = `${uriRequest}compare/download_statistics?class_one=${selectedClassOne}&class_two=${selectedClassTwo}`;

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
      link.download = `Compare_${selectedClassOne}_${selectedClassTwo}_statistics.jsonld`; // Name of the downloaded file
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
    { name: "Import as HTML", action: importAsHTML },
    { name: "Import as JSON-LD", action: importAsJSONLD },
    { name: "Import statistics", action: importStatistics },
  ];

  const handleSubmit = () => {
    let newErrors = {};
    if (!selectedClassOne) {
      newErrors.selectedClassOne = "Please select a class";
    }
    if (!selectedClassTwo) {
        newErrors.selectedClassTwo = "Please select a class";
    }
    if (selectedClassOne === selectedClassTwo) {
        newErrors.selectedClassTwo = "Please select another class";
    }
    setErrors(newErrors);

    return Object.keys(newErrors).length === 0;
  };

  const fetchData = async (selectedClassOne, selectedClassTwo) => {
    const dataUrl = `${uriRequest}compare/data?class_one=${selectedClassOne}&class_two=${selectedClassTwo}`;
    const response = await fetch(dataUrl, { method: "GET" });
    if (!response.ok) {
      throw new Error("Data API call failed");
    }
    return response.json();
  };

  const fetchStatisticsData = async (selectedClassOne, selectedClassTwo) => {
    const statsUrl = `${uriRequest}compare/statistics?class_one=${selectedClassOne}&class_two=${selectedClassTwo}`;
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
      const [compareData, statsData] = await Promise.all([
        fetchData(selectedClassOne, selectedClassTwo),
        fetchStatisticsData(selectedClassOne, selectedClassTwo),
      ]);

      setCompareData(compareData);
      setStatistics(statsData);
      setLoading(false);
      setShowStatistics(true);
      console.log("data:", compareData);
      console.log("stats:", statistics);
    } catch (error) {
      console.error("Error during visualization process:", error);
    }
  };

  const classes = classOptions;

  return (
    <div className="bg-radial from-violet-200 from-40% to-pink-200 min-h-[calc(100vh-64px)] w-full flex flex-col items-center">
      <h1 className="text-3xl font-semibold p-3 mt-2">Comparison</h1>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 w-full px-4 lg:my-auto mx:auto justify-center lg:h-128">
        <div className="flex flex-col w-full justify-around lg:justify-center col-span-1 bg-transparent lg:p-4 h-full">
          <Fieldset className="flex flex-col items-center justify-center rounded-md border-watr-100 p-4 bg-watr-300 shadow-2xl">
            <Legend className="font-medium text-xl">Input panel</Legend>
            <Field className="flex flex-col w-full p-1">
              <Label htmlFor="classOne" className="py-1">
                Select first class:
              </Label>
              <Select
                id="classOne"
                value={selectedClassOne}
                className="w-full bg-watr-400 p-2 rounded-md font-montserrat"
                onChange={(e) => setSelectedClassOne(e.target.value)}
              >
                <option value="">Select a Class</option>
                {classes.map((option, index) => (
                  <option key={index} value={option}>
                    {option}
                  </option>
                ))}
              </Select>
              {errors.selectedClassOne && (
                <ErrorsMessage errorMessage={errors.selectedClassOne} />
              )}
            </Field>
            <Field className="flex flex-col w-full p-1">
              <Label htmlFor="classTwo" className="py-1">
                Select second class:
              </Label>
              <Select
                id="classTwo"
                value={selectedClassTwo}
                className="w-full bg-watr-400 p-2 rounded-md font-montserrat"
                onChange={(e) => setSelectedClassTwo(e.target.value)}
              >
                <option value="">Select a Class</option>
                {classes.map((option, index) => (
                  <option key={index} value={option}>
                    {option}
                  </option>
                ))}
              </Select>
              {errors.selectedClassTwo && (
                <ErrorsMessage errorMessage={errors.selectedClassTwo} />
              )}
            </Field>
            <Field className="flex flex-col w-full pt-2 px-1">
              <Button
                onClick={handleVisualise}
                className="rounded bg-watr-200 hover:bg-watr-100 text-xl py-2 duration-300 text-white w-full"
              >
                Compare
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
          <div
            className={`w-full justify-end mb-4 ${
              !showStatistics ? "hidden" : "flex"
            }`}
          >
            <SwitchDisplay
              checked={currentView}
              onChange={setCurrentView}
              name_one="Table"
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
              <div className="flex flex-grow-1 flex-col items-center justify-between lg:h-full w-full">
                {/* Your graph component goes here */}
                {compareData && (
          <TableWithPagination data={compareData}/>)}
              </div>
            ) : (
              <div className="flex flex-grow-1 flex-col items-center justify-around lg:h-full w-full">
                {/* Your statistics component goes here */}
                <CompareStatistics statistics={statistics} />
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
