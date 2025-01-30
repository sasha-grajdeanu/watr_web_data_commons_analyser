from flask import request, Blueprint, jsonify, abort, Response

from services.comparation.compare_brute_data_service import compare_brute_data_service

compare_data = Blueprint('compare_data', __name__)

@compare_data.route('/data', methods=['GET'])
def compare_brute_data_controller():
    """
    Controller function to compare two classes of data.
    """
    class_one = request.args.get('class_one')
    class_two = request.args.get('class_two')

    # Validate input parameters
    if not class_one or not class_two:
        abort(400, description="Both 'class_one' and 'class_two' parameters are required.")
    try:
        results = compare_brute_data_service(class_one, class_two)
        return jsonify(results), 200, {"Content-Type": "application/json"}
    except Exception as e:
        abort(500, description=f"An error occurred while processing the request: {str(e)}")