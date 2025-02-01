from flask import request, abort


def content_type_middleware(app):
    """
    Middleware function that sets the corresponding 'accept_mimetype' on the request.
    It runs before each request.
    """

    @app.before_request  # it will run before each request
    def choose_content_type():
        # Get the 'Accept' header for response format
        accept_header = request.headers.get('Accept')

        app.logger.info(f"Middleware: Accept header is {accept_header}")

        if accept_header:
            if '*/*' in accept_header:
                request.accept_mimetype = 'application/json'
            elif 'text/html' in accept_header:
                request.accept_mimetype = 'text/html'
            elif 'application/ld+json' in accept_header:
                request.accept_mimetype = 'application/ld+json'
            else:
                app.logger.warning(f"415 Unsupported Content-Type: {accept_header}")
                abort(415, description=f"Accept header is {accept_header}")
        else:
            request.accept_mimetype = 'application/json'  # Default if nothing is provided
