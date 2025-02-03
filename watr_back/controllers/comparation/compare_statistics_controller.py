from flask import Blueprint, request, abort, jsonify

from services.comparation.compare_statistics_service import compare_statistics_service

compare_statistics = Blueprint('compare_statistics', __name__)


@compare_statistics.route('/statistics', methods=['GET'])
def compare_statistics_controller():
    class_one = request.args.get('class_one')
    class_two = request.args.get('class_two')
    if not class_one or not class_two:
        abort(400, description="Both 'class_one' and 'class_two' parameters are required.")

    results = compare_statistics_service(class_one, class_two)
    return jsonify(results), 200, {"Content-Type": "application/json"}
