from flask import Blueprint

from watr_back.controllers.classification.classification_controller import classify as controller_classify
from watr_back.services.classification.classification_stats_service import \
    get_classification_stats as service_get_classification_stats

classificationStats = Blueprint('classificationStats', __name__)

@classificationStats.route('/classify/stats', methods=['POST'])
def classify_stats():
    classify_data = controller_classify()
    results = service_get_classification_stats(classify_data)
    return results