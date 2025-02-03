from flask import request, abort


def content_type_middleware(app):

    @app.before_request
    def choose_content_type():
        accept_header = request.headers.get('Accept')

        app.logger.info(f"Middleware: Accept header is {accept_header}")

        if accept_header:
            if '*/*' in accept_header:
                request.accept_mimetype = 'application/json'
            elif 'text/html' in accept_header:
                request.accept_mimetype = 'text/html'
            elif 'application/ld+json' in accept_header:
                request.accept_mimetype = 'application/ld+json'
            elif 'application/json' in accept_header:
                request.accept_mimetype = 'application/json'
            else:
                app.logger.warning(f"415 Unsupported Content-Type: {accept_header}")
                abort(415, description=f"Accept header is {accept_header}")
        else:
            request.accept_mimetype = 'application/json'
