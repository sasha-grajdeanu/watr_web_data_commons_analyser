from flask import Blueprint, request, abort, Response

from auxiliary.visualise_auxiliary.validate_parameters import validate_rdf_class, validate_limit_and_count_limit
from services.visualise.visualisation_statistics_service import download_statistics

# Create a Flask Blueprint for visualisation statistics
download_visualisation_statistics = Blueprint('download_visualisation_statistics', __name__)


@download_visualisation_statistics.route('/download_statistics', methods=['GET'])
def download_statistics_controller():
    """
    Controller for handling requests to download statistics.
    """
    # Validate and extract query parameters
    rdf_class = validate_rdf_class(request.args.get('class'))
    limit, count_limit = validate_limit_and_count_limit(request.args.get('limit'), request.args.get('count_limit'))

    # Call the statistics service
    try:
        results = download_statistics(rdf_class, limit=limit, count_limit=count_limit)
        return Response(results, status=200, mimetype="application/ld+json")
    except Exception as e:
        abort(500, description=f"An error occurred while processing the request: {str(e)}")
