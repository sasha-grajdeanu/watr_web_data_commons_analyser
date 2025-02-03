import { useState } from "react";
import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

export default function DataVisualization({ data }) {
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 1;

  const shortenEdgeLabel = (label) => {
    label = label.replace(/https?:\/\//g, "").replace(/www\./g, "");

    const patterns = [
      { match: /schema\.org\//g, replace: "schema:" },
      { match: /w3\.org\/1999\/02\/22-rdf-syntax-ns#/g, replace: "rdf:" },
      { match: /owl\./g, replace: "owl:" },
      { match: /xmlns\.com\//g, replace: "xmlns:" },
    ];

    let shortenedLabel = label;
    patterns.forEach((pattern) => {
      shortenedLabel = shortenedLabel.replace(pattern.match, pattern.replace);
    });

    return shortenedLabel;
  };

  const transformData = (source) => {
    return {
      labels: Object.keys(source).map(shortenEdgeLabel),
      datasets: [
        {
          data: Object.values(source),
          backgroundColor: [
            "#FF6384",
            "#36A2EB",
            "#FFCE56",
            "#4BC0C0",
            "#9966FF",
            "#FF9F40",
            "#E7E9ED",
            "#8C564B",
          ],
          hoverOffset: 4,
        },
      ],
    };
  };

  const chartSections = [
    { title: "Properties Type", data: data.properties_type },
    { title: "Type Entity", data: data.type_entity },
    { title: "Value Type", data: data.value_type },
  ].filter((section) => Object.keys(section.data).length > 0);

  const totalPages = Math.ceil(chartSections.length / itemsPerPage);
  const currentCharts = chartSections.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  return (
    <div className="flex flex-col justify-between items-center p-4 w-full h-full text-monserrat">
      <div className="flex flex-col flex-grow-1 w-full h-full justify-center items-center">
        {currentCharts.map((section, index) => (
          <div
            key={index}
            className="p-2 bg-transparency w-full h-full flex flex-col items-center justify-around mb-4"
          >
            <h3 className="text-xl font-semibold mb-4">{section.title}</h3>
            <div className="w-full h-full flex flex-col lg:flex-row justify-center items-center">

              <div className="w-full h-60 lg:h-full lg:w-2/3 flex flex-grow-1">
                <Pie
                  data={transformData(section.data)}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false, 
                    plugins: {
                      legend: {
                        display: false, 
                      },
                    },
                    layout: {
                      padding: {
                        right: 20,
                      },
                    },
                  }}
                />
              </div>
              <div className="hidden lg:flex flex-col justify-start w-full lg:w-1/3 mt-4 md:mt-0 max-h-60 overflow-y-auto px-2">
                {Object.keys(section.data).map((label, idx) => (
                  <div key={idx} className="flex items-center mb-2">
                    <div
                      className="w-4 h-4 rounded-full shrink-0"
                      style={{
                        backgroundColor: [
                          "#FF6384",
                          "#36A2EB",
                          "#FFCE56",
                          "#4BC0C0",
                          "#9966FF",
                          "#FF9F40",
                          "#E7E9ED",
                          "#8C564B",
                        ][idx % 8],
                      }}
                    ></div>
                    <span className="ml-2 whitespace-nowrap overflow-hidden text-ellipsis">
                      {shortenEdgeLabel(label)}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
      <div className="flex justify-center gap-4">
        <button
          onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
          disabled={currentPage === 1}
          className="px-4 py-2 bg-watr-200 text-white rounded disabled:opacity-50 hover:bg-watr-100"
        >
          Previous
        </button>
        <span className="px-4 py-2">
          Page {currentPage} of {totalPages}
        </span>
        <button
          onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
          disabled={currentPage === totalPages}
          className="px-4 py-2 bg-watr-200 text-white rounded disabled:opacity-50 hover:bg-watr-100"
        >
          Next
        </button>
      </div>
    </div>
  );
}
