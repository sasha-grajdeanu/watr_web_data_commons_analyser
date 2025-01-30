from flask import Blueprint, request, abort

from services.classification.properties_service import get_properties as service_get_properties

properties = Blueprint('properties', __name__)


@properties.route('/properties', methods=['GET'])
def get_properties():
    """
    Controller function to get properties for classification.
    """
    rdf_class = request.args.get('class')

    if not rdf_class or not isinstance(rdf_class, str):
        abort(400, description="Invalid or missing 'class' parameter")

    results = service_get_properties(rdf_class)
    return results
