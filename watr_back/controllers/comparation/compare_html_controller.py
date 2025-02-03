import logging

from flask import Blueprint, request, abort, Response

from services.comparation.compare_html_service import compare_html_service

compare_html = Blueprint('compare_html', __name__)

logger = logging.getLogger(__name__)


@compare_html.route('/html', methods=['GET'])
def compare_html_controller():
    class_one = request.args.get('class_one')
    class_two = request.args.get('class_two')
    if not class_one or not class_two:
        abort(400, description="Both 'class_one' and 'class_two' parameters are required.")
    results = compare_html_service(class_one, class_two)
    return Response(results, status=200, mimetype='text/html')
