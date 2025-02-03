from flask import Blueprint, request, abort

from services.classification.classification_json_ld_service import classification_json_ld_service

classification_json_ld = Blueprint('classification_json_ld', __name__)


@classification_json_ld.route('/json_ld', methods=['GET'])
def classification_json_ld_controller():
    rdf_class = request.args.get('class')
    rdf_property = request.args.get('property')

    if not rdf_class or not isinstance(rdf_class, str):
        abort(400, description="Invalid or missing 'class' parameter")

    if not rdf_property or not isinstance(rdf_property, str):
        abort(400, description="Invalid or missing 'property' parameter")

    results = classification_json_ld_service(rdf_class, rdf_property)

    return results
