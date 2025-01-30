from auxiliary.classification_auxiliary.execute_classification_query import execute_classification_query
from auxiliary.classification_auxiliary.generate_html_classification import generate_html_classification


def classification_html_service(rdf_class, rdf_property):
    """
    Service function that returns the HTML results for classification
    """
    try:
        output = execute_classification_query(rdf_class, rdf_property)
        init_result = output['results']['bindings']
        return generate_html_classification(init_result)
    except Exception as e:
        return f"<h3>Error: {e}</h3>", 500
