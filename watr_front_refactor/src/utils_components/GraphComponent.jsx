import React, { useEffect, useRef, useMemo } from "react";
import { Network, DataSet } from "vis-network/standalone/umd/vis-network.min.js";

const shortenEdgeLabel = (label) => {
    // Remove common prefixes like 'https://', 'http://', and 'www.'
    label = label
      .replace(/https?:\/\//g, "") // Remove 'http://' or 'https://'
      .replace(/www\./g, ""); // Remove 'www.'
  
    // Define patterns to shorten specific terms
    const patterns = [
      { match: /schema\.org\//g, replace: "schema:" }, // schema.org/ → schema:
      { match: /w3\.org\/1999\/02\/22-rdf-syntax-ns#/g, replace: "rdf:" }, // w3. → rdf:
      { match: /owl\./g, replace: "owl:" }, // owl. → owl:
      { match: /xmlns\.com\//g, replace: "xmlns:" }, // xmlns.com/ → xmlns:
      // Add more patterns as needed
    ];
  
    // Apply each pattern to the label
    let shortenedLabel = label;
    patterns.forEach((pattern) => {
      shortenedLabel = shortenedLabel.replace(pattern.match, pattern.replace);
    });
  
    return shortenedLabel;
  };

const parseGraphML = (graphMLData) => {
  const parser = new DOMParser();
  const xmlDoc = parser.parseFromString(graphMLData, "application/xml");

  const nodes = [];
  const edges = [];

  const graphmlNodes = xmlDoc.getElementsByTagName("node");
  for (let i = 0; i < graphmlNodes.length; i++) {
    const node = graphmlNodes[i];
    const id = node.getAttribute("id");
    const label = node.getElementsByTagName("data")[0]?.textContent || id;
    nodes.push({ id, label });
  }

  const graphmlEdges = xmlDoc.getElementsByTagName("edge");
  for (let i = 0; i < graphmlEdges.length; i++) {
    const edge = graphmlEdges[i];
    const source = edge.getAttribute("source");
    const target = edge.getAttribute("target");

    const dataElements = edge.getElementsByTagName("data");
    let label = "";
    if (dataElements.length > 0) {
      label = dataElements[0].textContent;
      // Shorten the edge label
      label = shortenEdgeLabel(label);
    }

    edges.push({ from: source, to: target, label });
  }

  return { nodes, edges };
};

const GraphMLViewer = React.memo(({ graphMLData }) => {
  const graphContainer = useRef(null);

  const { nodes, edges } = useMemo(
    () => parseGraphML(graphMLData),
    [graphMLData]
  );

  useEffect(() => {
    if (graphContainer.current) {
      const data = {
        nodes: new DataSet(nodes),
        edges: new DataSet(edges),
      };
      const options = {
        physics: {
          enabled: true, // Enable physics for initial layout
          stabilization: {
            enabled: true,
            iterations: 100, // Adjust the number of iterations
          },
        },
        nodes: { shape: "dot", size: 10 },
        layout: {
          improvedLayout: false,
        },
      };

      new Network(graphContainer.current, data, options);
    }
  }, [nodes, edges]);

  return (
    <div
      ref={graphContainer}
      className="graph-container"
      style={{ height: "500px", width: "100%" }}
    ></div>
  );
});

export default GraphMLViewer;