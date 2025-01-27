from flask import Blueprint, request, abort

from watr_back.services.alignment.alignment_service import align as service_align

alignment = Blueprint('alignment', __name__)

@alignment.route('/align', methods=['POST'])
def align():
    data = request.json
    target_ontology = data.get('target')

    if not target_ontology or not isinstance(target_ontology, str):
        abort(400, description="Invalid or missing 'target' parameter")

    results = service_align(target_ontology)

    return results
