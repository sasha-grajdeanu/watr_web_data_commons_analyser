from flask import abort

from auxiliary.classification_auxiliary.execute_classification_query import execute_classification_query
from auxiliary.classification_auxiliary.generate_json_ld_classification import generate_json_ld_classification


def classification_json_ld_service(rdf_class, rdf_property):
    try:
        output = execute_classification_query(rdf_class, rdf_property)
        init_result = output['results']['bindings']
        return generate_json_ld_classification(init_result)
    except Exception as e:
        return abort(500, description=f"An error occurred: {e}")
