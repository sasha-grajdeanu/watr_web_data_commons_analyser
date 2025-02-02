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

  // Calculate total pages
  const totalPages = Math.ceil(data.length / itemsPerPage);

  // Get current page items
  const currentItems = data.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  return (
    <div className="w-full h-full flex flex-col justify-center items-center">
      <div className="overflow-x-auto w-full justify-center items-center flex-grow-1 h-full my-auto"> {/* Added horizontal scroll container */}
        <table className="min-w-full h-full flex-grow-1 border border-gray-300 text-xs sm:text-lg">
          <thead>
            <tr className="bg-watr-100 text-white">
              {Object.keys(data[0] || {}).map((key, index) => (
                // Ensure 'Property' column is always first
                <th key={key} className="border p-2">
                  {index === 0 ? shortenEdgeLabel('Property') : shortenEdgeLabel(key)}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {currentItems.map((item, index) => (
              <tr key={index} className="border bg-watr-200 text-white">
                {Object.entries(item).map(([key, value], i) => (
                  // Ensure the first column (property) is rendered first
                  <td key={i} className="border border-white p-2 text-center">
                    {i === 0 ? shortenEdgeLabel('Property') : shortenEdgeLabel(value)}
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
        <span className="px-2 py-1 hidden min-[400px]:block">Page {currentPage} of {totalPages}</span>
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
