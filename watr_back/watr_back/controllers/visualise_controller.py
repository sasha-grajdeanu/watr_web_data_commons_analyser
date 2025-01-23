from flask import Blueprint, request, abort
from services.visualize_service import visualise_service

visualisation = Blueprint('visualisation', __name__)

@visualisation.route('/visualise', methods=['GET'])
def visualise_controller():
    rdf_class = request.args.get('class')

    if not rdf_class or isinstance(rdf_class, str) is False:
        abort(400, 'class is required')
    results = visualise_service(rdf_class)
    return results