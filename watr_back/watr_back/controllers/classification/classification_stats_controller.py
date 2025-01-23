from flask import Blueprint, request, abort

from watr_back.services.classification.classification_stats_service import get_classification_stats as service_get_classification_stats
from watr_back.services.classification.classification_service import classify as service_classify

classificationStats = Blueprint('classificationStats', __name__)

@classificationStats.route('/classify/stats', methods=['POST'])
def classify_stats():
    data = request.json
    rdf_class = data.get('class')
    rdf_property = data.get('property')

    if not rdf_class or not isinstance(rdf_class, str):
        abort(400, description="Invalid or missing 'class' parameter")

    if not rdf_property or not isinstance(rdf_property, str):
        abort(400, description="Invalid or missing 'property' parameter")

    classify_data = service_classify(rdf_class, rdf_property)
    results = service_get_classification_stats(classify_data)
    return results