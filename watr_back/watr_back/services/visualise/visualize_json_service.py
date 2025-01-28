import uuid

from flask import jsonify

from auxiliary.visualise_auxiliary.execute_visualise_query import execute_sparql_query
from auxiliary.visualise_auxiliary.process_sparql_results import process_sparql_results


def visualise_service_json_ld(rdf_class, limit, count_limit):
    """
    Returns the SPARQL query results as JSON-LD.
    """
    try:
        output = execute_sparql_query(rdf_class, limit, count_limit)
        init_result = process_sparql_results(output)
        json_ld = {
            "@context": {
                "entity": "http://example.org/entity",
                "property": "http://example.org/property",
                "value": "http://example.org/value",
                "bnodeProperty": "http://example.org/bnodeProperty",
                "bnodeValue": "http://example.org/bnodeValue"
            },
            "@graph": []
        }
        for row in init_result:
            node = {
                "@id": f"urn:uuid:{uuid.uuid4()}",
                "entity" : row["entity"],
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