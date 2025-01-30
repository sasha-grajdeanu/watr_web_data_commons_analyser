from flask import Blueprint, request, abort, jsonify, Response

from auxiliary.visualise_auxiliary.validate_parameters import validate_rdf_class, validate_limit_and_count_limit
from services.visualise.visualisation_statistics_service import return_statistics, download_statistics

# Create a Flask Blueprint for visualisation statistics
visualisation_statistics = Blueprint('visualisation_statistics', __name__)

@visualisation_statistics.route('/statistics', methods=['GET'])
def visualise_statistics_controller():
    """
    Controller for handling requests to visualise statistics.
    """
    # Validate and extract query parameters
    rdf_class = validate_rdf_class(request.args.get('class'))
    limit, count_limit = validate_limit_and_count_limit(request.args.get('limit'), request.args.get('count_limit'))

    # Call the statistics service
    try:
        results = return_statistics(rdf_class, limit=limit, count_limit=count_limit)
        return jsonify(results), 200
    except Exception as e:
        abort(500, description=f"An error occurred while processing the request: {str(e)}")

