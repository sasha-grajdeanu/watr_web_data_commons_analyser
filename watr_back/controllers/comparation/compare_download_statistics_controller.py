from flask import Blueprint, request, abort, Response

from services.comparation.compare_download_statistics import compare_download_statistics_service

compare_download_statistics = Blueprint('compare_download_statistics', __name__)


@compare_download_statistics.route('/download_statistics', methods=['GET'])
def compare_download_statistics_controller():
    """
    Controller function to comp two classes of statistics.
    """
    class_one = request.args.get('class_one')
    class_two = request.args.get('class_two')

    # Validate input parameters
    if not class_one or not class_two:
        abort(400, description="Both 'class_one' and 'class_two' parameters are required.")

    results = compare_download_statistics_service(class_one, class_two)
    return Response(results, status=200, mimetype="application/ld+json")
