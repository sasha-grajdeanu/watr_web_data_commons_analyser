from flask import abort

from auxiliary.classification_auxiliary.execute_classification_query import execute_classification_query
from auxiliary.classification_auxiliary.process_classification_output import process_classification_output


def classify(rdf_class, rdf_property):
    """
    Service function that returns the results for classification
    """
    try:
        output = execute_classification_query(rdf_class, rdf_property)
        result = process_classification_output(output)
        return result
    except Exception as e:
        return abort(500, f"An error occurred: {e}")
