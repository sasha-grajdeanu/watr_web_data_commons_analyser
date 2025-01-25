from flask import Blueprint, request, abort
from services.viusalize.visualize_graph_service import visualise_graph_service

visualisation = Blueprint('visualisation', __name__)

@visualisation.route('/visualise_graph', methods=['GET'])
def visualise_controller():
    rdf_class = request.args.get('class')
    if not rdf_class or not isinstance(rdf_class, str):
        abort(400, 'class parameter is required and must be a string')

    limit = request.args.get('limit')

    if not limit or not isinstance(limit, str):
        abort(400, 'limit parameter is required and must be a string')

    count_limit = request.args.get('count_limit')

    if limit is not None:
        limit = limit.lower() == 'true'

    if limit:
        if count_limit is not None:
            try:
                count_limit = int(count_limit)
            except ValueError:
                abort(400, 'count_limit must be an integer')
        else:
            abort(400, 'count_limit is required when limit is true')

    results = visualise_graph_service(rdf_class, limit=limit, count_limit=count_limit)

    return results