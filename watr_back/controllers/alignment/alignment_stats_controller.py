from flask import Blueprint, request, abort

from services.alignment.alignment_stats_service import \
    alignment_stats_service

alignmentStats = Blueprint('alignmentStats', __name__)


@alignmentStats.route('/statistics', methods=['GET'])
def alignment_stats():
    """
    Controller function to create statistics for alignment in
    RDF Data Cube vocabulary.
    """
    target_ontology = request.args.get('target')

    if not target_ontology or not isinstance(target_ontology, str):
        abort(400, description="Invalid or missing 'target' parameter")

    result = alignment_stats_service(target_ontology)

    return result
