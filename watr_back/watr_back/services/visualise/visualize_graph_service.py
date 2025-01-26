from flask import jsonify, send_file

from auxiliary.visualise_auxiliary.execute_visualise_query import execute_sparql_query
from auxiliary.visualise_auxiliary.process_sparql_results import process_sparql_results
from auxiliary.visualise_auxiliary.write_graph_format import write_graph_format
from auxiliary.visualise_auxiliary.create_graph_base import create_init_graph

def visualise_graph_service(rdf_class, limit, count_limit):
    """
    Returns the SPARQL query results as a graph file.
    """
    try:
        output = execute_sparql_query(rdf_class, limit, count_limit)
        init_result = process_sparql_results(output)
        init_graph = create_init_graph(init_result)
        final_graph = write_graph_format(init_graph)
        return send_file(final_graph, as_attachment=True, download_name="graph.graphml")
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500
