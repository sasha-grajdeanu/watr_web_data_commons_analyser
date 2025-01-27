from flask import Blueprint, request, abort

from watr_back.services.download_stats_service import download_stats as service_get_graph_file


downloadStats = Blueprint('download-stats', __name__)

@downloadStats.route('/download-stats', methods=['GET'])
def download_stats():
    graph_file_path = request.args.get('graph_file')

    if not graph_file_path:
        abort(400, description="No file path provided")

    return service_get_graph_file(graph_file_path)