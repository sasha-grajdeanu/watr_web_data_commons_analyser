from flask import Blueprint, request, abort, jsonify
from services.visualise.visualisation_statistics_service import return_statistics

# Create a Flask Blueprint for visualisation statistics
visualisation_statistics = Blueprint('visualisation_statistics', __name__)

from flask import Response

@visualisation_statistics.route('/visualise_statistics', methods=['GET'])
def visualise_statistics_controller():
    """
    Controller for handling requests to visualise statistics.
    """
    # Validate and extract query parameters
    rdf_class = _validate_rdf_class(request.args.get('class'))
    limit, count_limit = _validate_limit_and_count_limit(request.args.get('limit'), request.args.get('count_limit'))

    # Call the statistics service
    try:
        results = return_statistics(rdf_class, limit=limit, count_limit=count_limit)
        return Response(results, status=200, mimetype="application/ld+json")
    except Exception as e:
        abort(500, description=f"An error occurred while processing the request: {str(e)}")


def _validate_rdf_class(rdf_class):
    """
    Validates the 'class' query parameter.
    """
    if not rdf_class or not isinstance(rdf_class, str):
        abort(400, description="The 'class' parameter is required and must be a string.")
    return rdf_class


def _validate_limit_and_count_limit(limit_param, count_limit_param):
    """
    Validates the 'limit' and 'count_limit' query parameters.
    """
    # Validate 'limit' parameter
    if not limit_param or not isinstance(limit_param, str):
        abort(400, description="The 'limit' parameter is required and must be a string ('true' or 'false').")
    limit = limit_param.lower() == 'true'

    # Validate 'count_limit' parameter if 'limit' is True
    count_limit = None
    if limit:
        if not count_limit_param:
            abort(400, description="The 'count_limit' parameter is required when 'limit' is true.")
        try:
            count_limit = int(count_limit_param)
            if count_limit < 1:
                abort(400, description="The 'count_limit' parameter must be a positive integer.")
        except ValueError:
            abort(400, description="The 'count_limit' parameter must be a valid integer.")

    return limit, count_limit