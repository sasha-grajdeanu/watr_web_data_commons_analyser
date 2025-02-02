from flask import abort

from auxiliary.compare_auxiliary.execute_compare_query import execute_compare_query
from auxiliary.compare_auxiliary.generate_json_ld_compare import generate_json_ld_compare


def compare_json_ld_service(class_one, class_two):
    """
    Service class that returns the JSON-LD response of the comparison
    """
    try:
        output = execute_compare_query(class_one, class_two)
        init_result = output['results']['bindings']
        return generate_json_ld_compare(init_result, class_one, class_two)
    except Exception as e:
        return abort(500, description=f"An error occured: {e}")
