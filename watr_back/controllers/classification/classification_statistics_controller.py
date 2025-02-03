from flask import Blueprint, request, abort

from services.classification.classification_statistics_service import classification_statistics_service

classificationStats = Blueprint('classificationStats', __name__)


@classificationStats.route('/statistics', methods=['GET'])
def classification_stats_controller():
    """
    Controller function for creating statistics for classification.
    """
    rdf_class = request.args.get('class')
    rdf_property = request.args.get('property')

    if not rdf_class or not isinstance(rdf_class, str):
        abort(400, description="Invalid or missing 'class' parameter")

    if not rdf_property or not isinstance(rdf_property, str):
        abort(400, description="Invalid or missing 'property' parameter")

    results = classification_statistics_service(rdf_class, rdf_property)
    return results
