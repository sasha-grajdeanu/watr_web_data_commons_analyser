from flask import request, Blueprint, abort

from services.comparation.compare_brute_data_service import compare_brute_data_service
from services.comparation.compare_html_service import compare_html_service
from services.comparation.compare_json_ld_service import compare_json_ld_service

compare_data = Blueprint('compare_data', __name__)


@compare_data.route('/data', methods=['GET'])
def compare_brute_data_controller():
    """
    Controller function to comp two classes of data.
    """
    class_one = request.args.get('class_one')
    class_two = request.args.get('class_two')

    # Validate input parameters
    if not class_one or not class_two:
        abort(400, description="Both 'class_one' and 'class_two' parameters are required.")

    results = compare_brute_data_service(class_one, class_two)

    accepted_types = ['application/json', 'text/html', 'application/ld+json']
    best_match = request.accept_mimetypes.best_match(accepted_types)

    if best_match == 'application/json':
        return results

    elif best_match == 'text/html':
        return compare_html_service(class_one, class_two)

    elif best_match == 'application/ld+json':
        return compare_json_ld_service(class_one, class_two)

    abort(406, description="The requested format is not supported.")
