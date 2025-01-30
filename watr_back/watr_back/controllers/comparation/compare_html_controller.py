import json

from flask import Blueprint, request, abort, jsonify, Response
import logging

from services.comparation.compare_html_service import compare_html_service

compare_html = Blueprint('compare_html', __name__)

# Set up logging
logger = logging.getLogger(__name__)

@compare_html.route('/html', methods=['GET'])
def compare_html_controller():
    """
    Controller function to compare two JSON-LD classes.
    """
    class_one = request.args.get('class_one')
    class_two = request.args.get('class_two')

    # Validate input parameters
    if not class_one or not class_two:
        abort(400, description="Both 'class_one' and 'class_two' parameters are required.")
    try:
        # Call the service function
        results = compare_html_service(class_one, class_two)
        print(results)
        return Response(results, status=200, mimetype='text/html')

    except Exception as e:
        logger.error(f"Error in compare_json_ld_controller: {str(e)}")
        abort(500, description="An internal error occurred while processing the request.")
