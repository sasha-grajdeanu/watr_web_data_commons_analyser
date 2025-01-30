import { useState } from "react";
import { classOptions } from "../utils";
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

export default function Visualize() {
  const [selectedClass, setSelectedClass] = useState("");
  const [haveLimit, setHaveLimit] = useState("false");
  const [limit, setLimit] = useState("");

  const [currentView, setCurrentView] = useState(true);

  const [graphData, setGraphData] = useState("");
  const [statistics, setStatistics] = useState("");
  const [showStatistics, setShowStatistics] = useState(true);

  const [errors, setErrors] = useState({
    selectedClass: "",
    limit: "",
  });

  const importAsHTML = () => {
    console.log("Importing as HTML");
  };

  const importAsJSONLD = () => {
    console.log("Importing as JSON-LD");
  };

  const importStatistics = () => {
    console.log("Importing statistics");
  };

  const importFunctionalities = [
    { name: "Import as HTML", action: importAsHTML },
    { name: "Import as JSON-LD", action: importAsJSONLD },
    { name: "Import statistics", action: importStatistics },
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

    if (Object.keys(newErrors).length === 0) {
      console.log("Form submitted successfully!");
    }
  };

  const classes = classOptions;

  return (
    <div className="bg-gradient-to-b from-watr-400 to-watr-300 min-h-[calc(100vh-64px)] w-full flex flex-col items-center">
      <h1 className="text-2xl font-semibold p-3">Visualisation</h1>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-2 w-full px-4 my-auto justify-center lg:h-128">
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
                <option value="false">No</option>
                <option value="true">Yes</option>
              </Select>
            </Field>
            {haveLimit === "true" && (
              <Field className="flex flex-col w-full px-1 pb-2">
                <Label htmlFor="limit" className="py-1">
                  Limit:
                </Label>
                <Input
                  id="limit"
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
                onClick={handleSubmit}
                className="rounded bg-watr-200 hover:bg-watr-100 text-xl py-2 duration-300 text-white w-full"
              >
                Visualize
              </Button>
            </Field>

            {selectedClass && (
              <div className="w-full hidden lg:block">
                <ImportButtons importFunctionalities={importFunctionalities} />
              </div>
            )}
          </Fieldset>
        </div>
        <div
          className={`${
            !selectedClass ? "hidden" : "flex"
          } lg:flex flex-col items-center justify-center col-span-2 bg-watr-300 p-4 rounded-md shadow-2xl`}
        >
          <div
            className={`w-full justify-end mb-4 ${
              !selectedClass ? "hidden" : "flex"
            }`}
          >
            <div className="flex items-center space-x-3">
              <span
                className={`text-sm font-medium ${
                  !currentView ? "text-watr-500" : "text-watr-100"
                }`}
              >
                Graph
              </span>
              <Switch
                checked={currentView}
                onChange={setCurrentView}
                className="group relative flex h-7 w-14 cursor-pointer rounded-full bg-white/10 p-1 transition-colors duration-200 ease-in-out focus:outline-none 
        data-[focus]:outline-1 data-[focus]:outline-white data-[checked]:bg-white/10"
              >
                <span
                  aria-hidden="true"
                  className="pointer-events-none inline-block size-5 translate-x-0 rounded-full bg-white ring-0 shadow-lg transition duration-200 ease-in-out 
          group-data-[checked]:translate-x-7"
                />
              </Switch>
              <span
                className={`text-sm font-medium ${
                  currentView ? "text-watr-500" : "text-watr-100"
                }`}
              >
                Statistics
              </span>
            </div>
          </div>
          {selectedClass ? (
            !currentView ? (
              <div className="w-full h-full flex items-center justify-center">
                {/* Your graph component goes here */}
                <p>Graph will be displayed here</p>
              </div>
            ) : (
              <div className="w-full h-full flex items-center justify-center">
                {/* Your statistics component goes here */}
                <p>Statistics will be displayed here</p>
              </div>
            )
          ) : (
            <div className="w-full h-full flex flex-col items-center justify-center">
                <img src={sadcat} alt="sad cat" className="w-78" />
                <p>If you submit, i'll show you some informations.</p>
            </div>
          )}
        </div>
        {selectedClass && (
          <div className="w-full block lg:hidden">
            <ImportButtons importFunctionalities={importFunctionalities} />
          </div>
        )}
      </div>
    </div>
  );
}
