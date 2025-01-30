from flask import Blueprint

from controllers.classification.classification_controller import classify as controller_classify
from services.classification.classification_graph_service import generate_graph_data as service_classify_graph

classificationGraph = Blueprint('classificationGraph', __name__)

@classificationGraph.route('/classify/graph', methods=['GET'])
def classify():
    classify_data = controller_classify()
    results = service_classify_graph(classify_data)
    return results