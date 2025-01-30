from flask import jsonify

from auxiliary.compare_auxiliary.execute_compare_query import execute_compare_sparql_query
from auxiliary.compare_auxiliary.process_compare_output import process_compare_sparql_results


def compare_brute_data_service(class_one, class_two):
    try:
        output = execute_compare_sparql_query(class_one, class_two)
        result = process_compare_sparql_results(output, class_one, class_two)
        return result
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}, 500)