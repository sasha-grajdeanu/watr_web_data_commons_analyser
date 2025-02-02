import logging

from flask import Blueprint, request, abort

from services.comparation.compare_json_ld_service import compare_json_ld_service

compare_json_ld = Blueprint('compare_json_ld', __name__)

# Set up logging
logger = logging.getLogger(__name__)


@compare_json_ld.route('/json_ld', methods=['GET'])
def compare_json_ld_controller():
    """
    Controller function to comp two JSON-LD classes.
    """
    class_one = request.args.get('class_one')
    class_two = request.args.get('class_two')

    # Validate input parameters
    if not class_one or not class_two:
        abort(400, description="Both 'class_one' and 'class_two' parameters are required.")

    # Call the service function
    results = compare_json_ld_service(class_one, class_two)
    return results
