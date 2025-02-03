from flask import Blueprint, request, abort

from auxiliary.alignment_auxiliary.generate_html_alignment import generate_html_alignment
from auxiliary.alignment_auxiliary.generate_json_ld_alignment import generate_json_ld_alignment
from services.alignment.alignment_data_service import alignment_data_service as service_align

alignment = Blueprint('alignment', __name__)


@alignment.route('/data', methods=['GET'])
def alignment_data_controller():
    target_ontology = request.args.get('target')

    if not target_ontology or not isinstance(target_ontology, str):
        abort(400, description="Invalid or missing 'target' parameter")

    result_path = service_align(target_ontology)

    accepted_types = ['application/json', 'text/html', 'application/ld+json']
    best_match = request.accept_mimetypes.best_match(accepted_types)

    if best_match == "application/json":
        return result_path

    elif best_match == "text/html":
        return generate_html_alignment(result_path, target_ontology)

    elif best_match == "application/ld+json":
        return generate_json_ld_alignment(result_path, target_ontology)

    abort(406, description="The requested format is not supported.")
