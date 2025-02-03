from flask import Blueprint, request, abort

from services.alignment.alignment_json_ld_service import alignment_json_ld_service

alignment_json_ld = Blueprint('alignment_json_ld', __name__)


@alignment_json_ld.route('/json_ld', methods=['GET'])
def alignment_json_ld_controller():

    target_ontology = request.args.get('target')
    if not target_ontology or not isinstance(target_ontology, str):
        abort(400, description="Invalid or missing 'target' parameter")

    results = alignment_json_ld_service(target_ontology)
    return results
