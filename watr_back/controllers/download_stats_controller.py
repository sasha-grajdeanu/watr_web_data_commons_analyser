from flask import Blueprint, request, abort

from services.download_stats_service import download_stats_service

downloadStats = Blueprint('download-stats', __name__)


@downloadStats.route('/download-stats', methods=['GET'])
def download_stats_controller():
    graph_file_path = request.args.get('graph_file')

    if not graph_file_path:
        abort(400, description="No file path provided")

    return download_stats_service(graph_file_path)
