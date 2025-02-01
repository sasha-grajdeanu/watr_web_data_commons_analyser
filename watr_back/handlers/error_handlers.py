from flask import jsonify


def error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        response = jsonify({"error": "Bad Request", "message": str(error)})
        response.status_code = 400
        return response

    @app.errorhandler(401)
    def unauthorized(error):
        response = jsonify({"error": "Unauthorized", "message": str(error)})
        response.status_code = 401
        return response

    @app.errorhandler(403)
    def forbidden(error):
        response = jsonify({"error": "Forbidden", "message": str(error)})
        response.status_code = 403
        return response

    @app.errorhandler(404)
    def not_found(error):
        response = jsonify({"error": "Not Found", "message": str(error)})
        response.status_code = 404
        return response

    @app.errorhandler(405)
    def method_not_allowed(error):
        response = jsonify({"error": "Method Not Allowed", "message": str(error)})
        response.status_code = 405
        return response

    @app.errorhandler(415)
    def unsupported_media_type(error):
        response = jsonify({"error": "Unsupported Media Type", "message": str(error)})
        response.status_code = 415
        return response

    @app.errorhandler(500)
    def internal_error(error):
        response = jsonify({"error": "Internal Server Error", "message": str(error)})
        response.status_code = 500
        return response
