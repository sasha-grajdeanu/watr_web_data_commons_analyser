from flask import Blueprint, request, abort

from watr_back.services.alignment.alignment_service import align as service_align
from watr_back.services.alignment.alignment_service import convert_results_to_html as html_converter
from watr_back.services.alignment.alignment_service import convert_results_to_jsonld as jsonld_converter



alignment = Blueprint('alignment', __name__)

@alignment.route('/align', methods=['GET'])
def align():
    target_ontology = request.args.get('target')

    if not target_ontology or not isinstance(target_ontology, str):
        abort(400, description="Invalid or missing 'target' parameter")

    results = service_align(target_ontology)

    if request.accept_mimetype == "application/json":
        return results

    elif request.accept_mimetype == "text/html":
        html_output = html_converter(results)
        return html_output

    elif request.accept_mimetype == "application/ld+json":
        ld_json_output = jsonld_converter(results)
        return ld_json_output

    return results
