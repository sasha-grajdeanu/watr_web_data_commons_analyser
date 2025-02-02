from flask import jsonify

from auxiliary.visualise_auxiliary.execute_visualise_query import execute_visualise_query
from auxiliary.visualise_auxiliary.process_visualise_results import process_visualise_results


def visualise_json_ld_service(rdf_class, limit, count_limit):
    """
    Returns the SPARQL query results as JSON-LD.
    """
    try:
        output = execute_visualise_query(rdf_class, limit, count_limit)
        init_result = process_visualise_results(output)
        json_ld = {
            "@context": "http://schema.org",
            '@type': 'Visualisation_results',
            "@graph": []
        }
        for row in init_result:
            node = {
                "entity": row["entity"],
                "property": row["property"],
                "value": row["value"],
            }
            if "bnodeProperty" in row and "bnodeValue" in row:
                node["bnodeProperty"] = row["bnodeProperty"]
                node["bnodeValue"] = row["bnodeValue"]
            json_ld["@graph"].append(node)
        return jsonify(json_ld)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500
