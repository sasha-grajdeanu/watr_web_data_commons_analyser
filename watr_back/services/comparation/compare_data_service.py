from flask import abort

from auxiliary.compare_auxiliary.execute_compare_query import execute_compare_query
from auxiliary.compare_auxiliary.process_compare_output import process_compare_output


def compare_data_service(class_one, class_two):
    """
    Service function that returns the results of comparison
    """
    try:
        output = execute_compare_query(class_one, class_two)
        result = process_compare_output(output, class_one, class_two)
        return result
    except Exception as e:
        return abort(500, f"An error occurred: {e}")
