from flask import Blueprint, abort, request

from watr_back.services.classification.classification_service import classify as service_classify
from watr_back.services.classification.classification_service import convert_results_to_html as html_converter
from watr_back.services.classification.classification_service import convert_results_to_jsonld as jsonld_converter

classification = Blueprint('classification', __name__)

@classification.route('/classify', methods=['GET'])
def classify():
    data = request.args
    rdf_class = data.get('class')
    rdf_property =data.get('property')

    if not rdf_class or not isinstance(rdf_class, str):
        abort(400, description="Invalid or missing 'class' parameter")

    if not rdf_property or not isinstance(rdf_property, str):
        abort(400, description="Invalid or missing 'property' parameter")


    results = service_classify(rdf_class, rdf_property)

    if request.accept_mimetype == 'application/json':
        return results

    elif request.accept_mimetype == 'text/html':
        html_output = html_converter(results)
        return html_output

    elif request.accept_mimetype == 'application/ld+json':
        ld_json_output = jsonld_converter(results)
        return ld_json_output
    return results

