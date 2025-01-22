import os
import tempfile

import networkx as nx
from SPARQLWrapper import SPARQLWrapper, JSON
from flask import jsonify, send_file

from watr_back.sparql_queries.classification_queries import CLASSIFY_NEW


sparql = SPARQLWrapper("http://localhost:3030/watr-dataset/sparql")


def generate_graph_data(rdf_class, rdf_property):
    sparql_query = CLASSIFY_NEW.format(rdf_class=rdf_class, property=rdf_property)
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        output = []

        for result in results["results"]["bindings"]:
            row = {
                "initial_subject": result.get("initial_subject", {}).get("value", None),
                "initial_predicate": result.get("initial_predicate", {}).get("value", None),
                "blankNode": result.get("blankNode", {}).get("value", None),
            }

            # Check for level 1 data
            if "level1_predicate" in result and "level1_object" in result:
                row["level1_predicate"] = result["level1_predicate"]["value"]
                row["level1_object"] = result["level1_object"]["value"]

            # Check for level 2 data
            if "level2_predicate" in result and "level2_object" in result:
                row["level2_predicate"] = result["level2_predicate"]["value"]
                row["level2_object"] = result["level2_object"]["value"]

            # Check for level 3 data
            if "level3_predicate" in result and "level3_object" in result:
                row["level3_predicate"] = result["level3_predicate"]["value"]
                row["level3_object"] = result["level3_object"]["value"]

            output.append(row)

        graph = create_graph_edges(output)

        # Generate temp file
        temp_file = write_graph_to_temp_file(graph)

        # Send the temp file to frontend
        return send_file(temp_file, as_attachment=True, download_name="output_graph.graphml")

    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

def create_graph_edges(results):
    edges = set()

    for result in results:
        subject = result.get("initial_subject")
        predicate = result.get("initial_predicate")
        obj = result.get("blankNode")

        edges.add((subject, predicate, obj))

        if result.get("level1_predicate") is not None:
            edges.add((obj, result["level1_predicate"], result["level1_object"]))

        if result.get("level2_predicate") is not None:
            edges.add((result["level1_object"], result["level2_predicate"], result["level2_object"]))

        if result.get("level3_predicate") is not None:
            edges.add((result["level2_object"], result["level3_predicate"], result["level3_object"]))

    return edges

def write_graph_to_temp_file(graph):
    G = nx.DiGraph()  # Directed Graph

    # Add edges to the graph
    for edge in graph:
        G.add_edge(edge[0], edge[2], label=edge[1])

    # create a temp file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".graphml")

    try:
        # save graph to temp file
        nx.write_graphml(G, temp_file.name)
    except Exception as e:
        temp_file.close()
        os.unlink(temp_file.name)
        raise e

    # return path
    return temp_file.name