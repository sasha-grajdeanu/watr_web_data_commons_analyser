from flask import Blueprint

from controllers.classification.classification_controller import classify as controller_classify
from services.classification.classification_stats_service import \
    get_classification_stats as service_get_classification_stats

classificationStats = Blueprint('classificationStats', __name__)

@classificationStats.route('/classify/stats', methods=['GET'])
def classify_stats():
    classify_data = controller_classify()
    results = service_get_classification_stats(classify_data)
    return results