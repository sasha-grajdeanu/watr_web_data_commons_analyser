from flask import Blueprint, request, abort

from services.viusalize.visualisation_statistics_service import statistics_classification

visualisation_statistics = Blueprint('visualisation_statistics', __name__)

@visualisation_statistics.route('/visualise_statistics', methods=['GET'])
def visualise_statistics_controller():
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

    results = statistics_classification(rdf_class, limit=limit, count_limit=count_limit)

    return results