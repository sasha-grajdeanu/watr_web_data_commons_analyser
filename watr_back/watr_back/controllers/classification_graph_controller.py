from flask import Blueprint, request, abort

from ..services.classification_graph_service import generate_graph_data as service_classify_graph

classificationGraph = Blueprint('classificationGraph', __name__)

@classificationGraph.route('/classify/graph', methods=['POST'])
def classify():
    data = request.json
    rdf_class = data.get('class')
    rdf_property =data.get('property')

    if not rdf_class or not isinstance(rdf_class, str):
        abort(400, description="Invalid or missing 'class' parameter")

    if not rdf_property or not isinstance(rdf_property, str):
        abort(400, description="Invalid or missing 'property' parameter")

    results = service_classify_graph(rdf_class, rdf_property)
    return results