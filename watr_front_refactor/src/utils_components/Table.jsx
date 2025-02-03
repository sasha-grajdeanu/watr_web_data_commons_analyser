import { useState } from "react";

const TableWithPagination = ({ data }) => {
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;

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

  const totalPages = Math.ceil(data.length / itemsPerPage);

  const currentItems = data.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  const allKeys = data.length > 0 ? Object.keys(data[0]) : [];
  const formattedKeys = allKeys.map((key) => (key === "property" ? "Property" : key));
  const sortedKeys = ["Property", ...formattedKeys.filter((key) => key !== "Property")];

  return (
    <div className="w-full h-full flex flex-col justify-center items-center">
      <div className="overflow-x-auto w-full justify-center items-center flex-grow-1 h-full my-auto">
        <table className="min-w-full h-full flex-grow-1 text-xs sm:text-lg">
          <thead>
            <tr className="bg-watr-100 text-white">
              {sortedKeys.map((key) => (
                <th key={key} className="p-2">
                  {shortenEdgeLabel(key)}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {currentItems.map((item, index) => (
              <tr key={index} className="bg-watr-400 text-watr-100">
                {sortedKeys.map((key, i) => (
                  <td key={i} className="border-white p-2 text-center">
                    {shortenEdgeLabel(item[key === "Property" ? "property" : key] || "")}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="flex justify-center mt-4 space-x-2">
        <button
          className="px-2 py-2 bg-watr-200 text-white rounded disabled:opacity-50 hover:bg-watr-100"
          onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
          disabled={currentPage === 1}
        >
          Previous
        </button>
        <span className="px-2 py-1 hidden min-[400px]:block">
          Page {currentPage} of {totalPages}
        </span>
        <button
          className="px-2 py-2 bg-watr-200 text-white rounded disabled:opacity-50 hover:bg-watr-100"
          onClick={() => setCurrentPage((prev) => Math.min(prev + 1, totalPages))}
          disabled={currentPage === totalPages}
        >
          Next
        </button>
      </div>
    </div>
  );
};

export default TableWithPagination;
