from flask import Blueprint, request, abort

from services.alignment.alignment_html_service import alignment_html_service

alignment_html = Blueprint('alignment_html', __name__)


@alignment_html.route('/html', methods=['GET'])
def alignment_html_controller():
    """
    Controller function to align based on a chosen ontology and
    returns a tabular HTML page with the results.
    """
    target_ontology = request.args.get('target')

    if not target_ontology or not isinstance(target_ontology, str):
        abort(400, description="Invalid or missing 'target' parameter")

    results = alignment_html_service(target_ontology)
    return results
