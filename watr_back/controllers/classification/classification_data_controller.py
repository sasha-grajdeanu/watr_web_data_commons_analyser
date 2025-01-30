from flask import Blueprint, abort, request

from services.classification.classification_brute_data_service import classify as service_classify
from services.classification.classification_html_service import classification_html_service
from services.classification.classification_json_ld_service import classification_json_ld_service

classification = Blueprint('classification', __name__)


@classification.route('/data', methods=['GET'])
def classify_brute_data_controller():
    """
    Controller function to classify based on class and property.
    """
    rdf_class = request.args.get('class')
    rdf_property = request.args.get('property')

    if not rdf_class or not isinstance(rdf_class, str):
        abort(400, description="Invalid or missing 'class' parameter")

    if not rdf_property or not isinstance(rdf_property, str):
        abort(400, description="Invalid or missing 'property' parameter")

    results = service_classify(rdf_class, rdf_property)

    accepted_types = ['application/json', 'text/html', 'application/ld+json']
    best_match = request.accept_mimetypes.best_match(accepted_types)

    if best_match == 'application/json':
        return results

    elif best_match == 'text/html':
        return classification_html_service(rdf_class, rdf_property)

    elif best_match == 'application/ld+json':
        return classification_json_ld_service(rdf_class, rdf_property)

    abort(406, description="The requested format is not supported.")
