from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(415)
    def unsupported_media_type(error):
        response = jsonify({"error": "Unsupported Media Type", "message":str(error)})
        response.status_code = 415
        return response

    @app.errorhandler(400)
    def bad_request(error):
        response = jsonify({"error": "Bad Request", "message":str(error)})
        response.status_code = 400
        return response