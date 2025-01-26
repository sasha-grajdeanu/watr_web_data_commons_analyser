from flask import Blueprint, request, abort
from services.visualise.visualize_json_service import visualise_service_json_ld

visualisation_json_ld = Blueprint('visualisation_json_ld', __name__)

@visualisation_json_ld.route('/visualise_json_ld', methods=['GET'])
def visualise_json_ld_controller():
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

    results = visualise_service_json_ld(rdf_class, limit=limit, count_limit=count_limit)

    return results