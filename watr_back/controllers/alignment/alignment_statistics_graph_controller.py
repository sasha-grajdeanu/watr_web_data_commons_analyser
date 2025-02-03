from flask import Blueprint, request, abort

from services.alignment.alignment_stats_graph_service import alignment_stats_graph_service

alignmentStatsGraph = Blueprint('alignmentStatsGraph', __name__)


@alignmentStatsGraph.route('/statistics/graph', methods=['GET'])
def alignment_statistics_graph_controller():

    target_ontology = request.args.get('target')

    if not target_ontology or not isinstance(target_ontology, str):
        abort(400, description="Invalid or missing 'target' parameter")

    result_path = alignment_stats_graph_service(target_ontology)

    return result_path
