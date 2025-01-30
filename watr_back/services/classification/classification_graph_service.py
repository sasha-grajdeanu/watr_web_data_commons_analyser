import os
import tempfile

import networkx as nx
from flask import jsonify, send_file

from auxiliary.classification_auxiliary.execute_classification_query import execute_classification_query
from auxiliary.classification_auxiliary.process_classification_output import process_classification_output


def generate_graph_data(rdf_class, rdf_property):
    """
    Service function that returns a graph visualization of the results of classification
    """
    output = execute_classification_query(rdf_class, rdf_property)
    results = process_classification_output(output)
    try:
        graph = create_graph_edges(results)

        # Generate temp file
        temp_file = write_graph_to_temp_file(graph)

        # Send the temp file to frontend
        return send_file(temp_file, as_attachment=True, download_name="output_graph.graphml")

    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500


def clean_property_name(prop):
    if "#" in prop:
        return "rdf:" + prop.split('/')[-1].split('#')[-1]
    else:
        return "schema:" + prop.split('/')[-1]


def create_graph_edges(results):
    edges = set()

    for result in results:
        subject = result.get("initial_subject")
        predicate = clean_property_name(result.get("initial_predicate"))
        obj = result.get("blankNode")

        edges.add((subject, predicate, obj))

        if result.get("level1_predicate") is not None:
            edges.add((obj, clean_property_name(result["level1_predicate"]), result["level1_object"]))

        if result.get("level2_predicate") is not None:
            edges.add(
                (result["level1_object"], clean_property_name(result["level2_predicate"]), result["level2_object"]))

        if result.get("level3_predicate") is not None:
            edges.add(
                (result["level2_object"], clean_property_name(result["level3_predicate"]), result["level3_object"]))

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

    return temp_file.name
