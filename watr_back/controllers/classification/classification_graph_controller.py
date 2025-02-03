from flask import Blueprint, request, abort

from services.classification.classification_graph_service import classification_graph_service as service_classify_graph

classificationGraph = Blueprint('classificationGraph', __name__)


@classificationGraph.route('/graph', methods=['GET'])
def classification_graph_controller():
    rdf_class = request.args.get('class')
    rdf_property = request.args.get('property')

    if not rdf_class or not isinstance(rdf_class, str):
        abort(400, description="Invalid or missing 'class' parameter")

    if not rdf_property or not isinstance(rdf_property, str):
        abort(400, description="Invalid or missing 'property' parameter")

    results = service_classify_graph(rdf_class, rdf_property)
    return results
