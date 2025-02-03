from flask import Blueprint, request, abort

from services.classification.classification_html_service import classification_html_service

classification_html = Blueprint('classification_html', __name__)


@classification_html.route('/html', methods=['GET'])
def classification_html_controller():
    rdf_class = request.args.get('class')
    rdf_property = request.args.get('property')

    if not rdf_class or not isinstance(rdf_class, str):
        abort(400, description="Invalid or missing 'class' parameter")

    if not rdf_property or not isinstance(rdf_property, str):
        abort(400, description="Invalid or missing 'property' parameter")

    results = classification_html_service(rdf_class, rdf_property)

    return results
