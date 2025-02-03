from flask import Blueprint, request, abort

from auxiliary.visualise_auxiliary.validate_parameters import validate_rdf_class, validate_limit_and_count_limit
from services.visualise.visualise_data_service import visualise_data_service
from services.visualise.visualize_html_service import visualise_html_service
from services.visualise.visualize_json_service import visualise_json_ld_service

visualisation_data = Blueprint('visualisation_data', __name__)


@visualisation_data.route('/data', methods=['GET'])
def visualise_brute_data_controller():
    rdf_class = validate_rdf_class(request.args.get('class'))
    limit, count_limit = validate_limit_and_count_limit(request.args.get('limit'), request.args.get('count_limit'))

    results = visualise_data_service(rdf_class, limit=limit, count_limit=count_limit)

    accepted_types = ['application/json', 'text/html', 'application/ld+json']
    best_match = request.accept_mimetypes.best_match(accepted_types)

    if best_match == 'application/json':
        return results

    elif best_match == 'text/html':
        return visualise_html_service(rdf_class, limit=limit, count_limit=count_limit)

    elif best_match == 'application/ld+json':
        return visualise_json_ld_service(rdf_class, limit=limit, count_limit=count_limit)

    abort(406, description="The requested format is not supported.")
