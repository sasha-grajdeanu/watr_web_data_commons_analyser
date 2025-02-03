import React, { useEffect, useRef, useMemo, useState } from "react";
import { Network, DataSet } from "vis-network/standalone/umd/vis-network.min.js";

const shortenEdgeLabel = (label) => {
  label = label
    .replace(/https?:\/\//g, "")
    .replace(/www\./g, "");

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
      label = shortenEdgeLabel(label);
    }

    edges.push({ from: source, to: target, label });
  }

  return { nodes, edges };
};

const GraphMLViewer = ({ graphMLData }) => {
  const graphContainer = useRef(null);
  const [network, setNetwork] = useState(null);

  const { nodes, edges } = useMemo(() => parseGraphML(graphMLData), [graphMLData]);

  useEffect(() => {
    if (graphContainer.current) {
      const data = {
        nodes: new DataSet(nodes),
        edges: new DataSet(edges),
      };

      const options = {
        physics: {
          enabled: true,
          stabilization: {
            enabled: true,
            iterations: 500,
          },
        },
        nodes: {
          shape: "dot",
          size: 14,
          color: {
            background: "#1a4078",
            border: "#1a4078",
            highlight: {
              background: "#686ea7",
              border: "#aea8d6",
            },
            hover: {
              background: "#686ea7",
              border: "#aea8d6",
            },
          },
        },
        edges: {
          arrows: {
            to: { enabled: true, scaleFactor: 1 },
          },
        },
        layout: {
          improvedLayout: false,
        },
      };

      const networkInstance = new Network(graphContainer.current, data, options);
      setNetwork(networkInstance);

      networkInstance.on("stabilizationIterationsDone", () => {
        networkInstance.fit();
      });

      const handleResize = () => {
        if (graphContainer.current && networkInstance) {
          networkInstance.setSize(
            `${graphContainer.current.clientWidth}px`,
            `${graphContainer.current.clientHeight}px`
          );
          networkInstance.fit();
        }
      };

      window.addEventListener("resize", handleResize);

      return () => {
        window.removeEventListener("resize", handleResize);
        networkInstance.destroy();
      };
    }
  }, [nodes, edges]);

  return (
    <div
      ref={graphContainer}
      className="w-full h-full"
      style={{ width: "100%", height: "100%" }}
    ></div>
  );
};

export default GraphMLViewer;
