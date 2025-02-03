import { useState } from "react";

const AlignTableWithPagination = ({ data, average }) => {
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;

  // Convert object data to an array
  const formattedData = Object.entries(data).map(([key, value]) => ({ id: key, ...value }));

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
  const totalPages = Math.ceil(formattedData.length / itemsPerPage);

  // Get current page items
  const currentItems = formattedData.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  return (
    <div className="w-full h-full flex flex-col justify-center items-center p-2">
      <p className="text-xl mb-4 font-bold text-white">Average Measure: {average["average_measure"]}</p>
      <div className="overflow-x-auto w-full justify-center items-center flex-grow-1 h-full my-auto">
        <table className="min-w-full h-full flex-grow-1 border-gray-300 text-md sm:text-md">
          <thead>
            <tr className="bg-watr-100 text-white">
              <th className=" p-2">Aligned Entity</th>
              <th className="p-2">Original Entity</th>
              <th className="max-sm:hidden p-2">Relation</th>
              <th className="p-2">Measure</th>
            </tr>
          </thead>
          <tbody>
            {currentItems.map((item) => (
              <tr key={item.id} className=" bg-watr-400 text-watr-100">
                <td className=" border-white p-2 text-center">{shortenEdgeLabel(item.alignedEntity)}</td> 
                <td className=" border-white p-2 text-center">{shortenEdgeLabel(item.originalEntity)}</td>
                <td className="max-sm:hidden  p-2 text-center">{item.relation}</td>
                <td className=" border-white p-2 text-center">{item.measure}</td>
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

export default AlignTableWithPagination;
