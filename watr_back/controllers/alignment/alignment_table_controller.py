from flask import Blueprint, request, abort

from services.alignment.alignment_table_service import alignment_table_service

alignmentTable = Blueprint('alignmentTable', __name__)


@alignmentTable.route('/table', methods=['GET'])
def alignment_table_controller():
    target_ontology = request.args.get('target')
    if not target_ontology or not isinstance(target_ontology, str):
        abort(400, description="Invalid or missing 'target' parameter")

    results_path = alignment_table_service(target_ontology)
    return results_path
