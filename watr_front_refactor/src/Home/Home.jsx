export default function Home() {
    return (
      <div className="bg-radial from-violet-200 from-40% to-pink-200 min-h-[calc(100vh-64px)] flex md:flex-row flex-col items-center justify-center xl:px-32 px-14">
        <div className="flex flex-col md:w-1/2 md:items-end items-center font-montserrat md:pr-8 pb-8">
          <h1 className="xl:text-8xl text-6xl max-[480px]:text-7xl min-[480px]:text-9xl font-bold text-gray-800 mb-4">Hello!</h1>
          <h1 className="xl:text-5xl text-4xl max-[520px]:text-5xl min-[520px]:text-6xl font-semibold">This is WATR.</h1>
        </div>
        {/* <div className="hidden md:block w-px bg-gray-400 h-48 mx-8"></div> */}
        <div className="md:w-1/2">
        <div className="max-w-2xl p-8 bg-pink-200 rounded-2xl shadow-lg">
          <p className="text-gray-600 leading-relaxed">
            The Web Data Commons Analyzer (WATR) is a web-based application
            designed to process and analyze metadata extracted from the{" "}
            <a role="doc-biblioref" href="#" className="text-blue-500 underline">
              Web Data Commons
            </a>
            . Through this platform, users can perform complex tasks such as
            visualizing the structure and relationships within the data,
            classifying it according to predefined categories, comparing data, and
            aligning the data with existing ontologies.
          </p>
          <p className="text-gray-600 leading-relaxed mt-4">
            The system uses{" "}
            <a role="doc-biblioref" href="#" className="text-blue-500 underline">
              SPARQL
            </a>{" "}
            queries to an
            <a role="doc-biblioref" href="#" className="text-blue-500 underline">
              {" "}
              Apache Jena Fuseki
            </a>{" "}
            server to retrieve the data, and results are available in HTML,
            <a role="doc-biblioref" href="#" className="text-blue-500 underline">
              {" "}
              JSON-LD
            </a>{" "}
            and JSON formats. Various statistics for each operation are provided
            using the
            <a role="doc-biblioref" href="#" className="text-blue-500 underline">
              {" "}
              RDF Data Cube vocabulary
            </a>
            .
          </p>
        </div>
        </div>
      </div>
    );
  }
  