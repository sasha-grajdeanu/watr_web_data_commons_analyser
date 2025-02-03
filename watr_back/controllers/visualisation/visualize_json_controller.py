from flask import Blueprint, request

from auxiliary.visualise_auxiliary.validate_parameters import validate_rdf_class, validate_limit_and_count_limit
from services.visualise.visualize_json_service import visualise_json_ld_service

visualisation_json_ld = Blueprint('visualisation_json_ld', __name__)


@visualisation_json_ld.route('/json_ld', methods=['GET'])
def visualise_json_ld_controller():
    rdf_class = validate_rdf_class(request.args.get('class'))
    limit, count_limit = validate_limit_and_count_limit(request.args.get('limit'), request.args.get('count_limit'))

    results = visualise_json_ld_service(rdf_class, limit=limit, count_limit=count_limit)

    return results, 200
