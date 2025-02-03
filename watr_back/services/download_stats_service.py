from flask import send_file, abort


def download_stats_service(file_path):
    try:
        return send_file(file_path, as_attachment=True, download_name="graph_data.ttl",
                         mimetype='application/turtle')
    except Exception as e:
        abort(500, description=f"An error occurred: {e}")
