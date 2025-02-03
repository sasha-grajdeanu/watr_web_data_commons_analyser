from flask import Blueprint, request

from auxiliary.visualise_auxiliary.validate_parameters import validate_rdf_class, validate_limit_and_count_limit
from services.visualise.visualize_html_service import visualise_html_service

visualisation_html = Blueprint('visualisation_html', __name__)


@visualisation_html.route('/html', methods=['GET'])
def visualise_html_controller():
    rdf_class = validate_rdf_class(request.args.get('class'))
    limit, count_limit = validate_limit_and_count_limit(request.args.get('limit'), request.args.get('count_limit'))

    results = visualise_html_service(rdf_class, limit=limit, count_limit=count_limit)

    return results
