# /app/controllers/classification_controller.py

from flask import jsonify, render_template, request, Blueprint

testt = Blueprint('testt', __name__)

@testt.route('/testt', methods=['POST'])
def test():
    try:
        # Example data processing
        data = {"message": "Classification successful!"}

        print(request.accept_mimetypes)

        if request.accept_mimetypes['application/json']:
            return jsonify(data)
        elif request.accept_mimetypes['text/html']:
            return "<html><body><h1>Classification Successful!</h1></body></html>"
        elif request.accept_mimetypes['application/ld+json']:
            data = {"message": "ldldld"}
            return jsonify(data), 200


        # If none of the mimetypes match
        return "Unsupported MIME type", 415
    except Exception as e:
        print(f"Error: {e}")  # Log the error to console
        return jsonify({"error": str(e)}), 500