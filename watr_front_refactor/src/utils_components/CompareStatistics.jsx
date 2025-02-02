import { useState } from "react";

export default function CompareStatistics({ statistics }) {
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 1;

  // Convert statistics object into an array
  let categories = Object.entries(statistics);

  // Function to shorten URLs or labels
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

  const totalPages = categories.length;

  const handleNext = () => {
    if (currentPage < totalPages) setCurrentPage(currentPage + 1);
  };

  const handlePrev = () => {
    if (currentPage > 1) setCurrentPage(currentPage - 1);
  };

  return (
    <div className="p-4 flex flex-col justify-between w-full h-full bg-watr-400 shadow-lg rounded-2xl">
      {categories
        .slice(currentPage - 1, currentPage)
        .map(([category, details]) => (
          <div key={category} className="flex flex-col flex-grow-1 mb-6">
            <h2 className="text-xl font-semibold mb-4 text-watr-100">{category}</h2>

            {category === "common_properties" ? (
              <div className="flex flex-wrap gap-2 mb-4">
                {details.map((prop) => (
                  <span
                    key={prop}
                    className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm"
                  >
                    {shortenEdgeLabel(prop)}
                  </span>
                ))}
              </div>
            ) : (
              <>
                <div className="flex flex-col sm:flex-row justify-between mb-4">
                  {details.most_used && (
                    <p className="text-green-600 font-medium">
                      Most Used: {shortenEdgeLabel(details.most_used)}
                    </p>
                  )}
                  {details.least_used && (
                    <p className="text-red-600 font-medium">
                      Least Used: {shortenEdgeLabel(details.least_used)}
                    </p>
                  )}
                </div>

                {details["unique_properties"] && (
                  <div className="mt-4">
                    <h3 className="text-lg font-semibold mb-2 text-gray-800">
                      Unique properties ({details["unique_properties"].length}):
                    </h3>
                    <div className="flex flex-wrap gap-2 max-h-40 sm:max-h-48 md:max-h-50 overflow-y-auto px-2 my-2">
                      {details["unique_properties"].map((prop) => (
                        <span
                          key={prop}
                          className="px-4 py-2 mr-2 mb-2 bg-watr-300 text-watr-100 rounded-full text-sm flex-shrink-0"
                        >
                          {shortenEdgeLabel(prop)}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
        ))}

      <div className="flex justify-between mt-4 items-center">
        <button
          onClick={handlePrev}
          disabled={currentPage === 1}
          className="px-4 py-2 bg-watr-200 text-white rounded-md disabled:opacity-50 transition duration-300 ease-in-out"
        >
          Previous
        </button>
        <span className="px-4 py-2 text-sm min-[400px]:block hidden">
          Page {currentPage} of {totalPages}
        </span>
        <button
          onClick={handleNext}
          disabled={currentPage === totalPages}
          className="px-4 py-2 bg-watr-200 text-white rounded-md disabled:opacity-50 transition duration-300 ease-in-out"
        >
          Next
        </button>
      </div>
    </div>
  );
}
