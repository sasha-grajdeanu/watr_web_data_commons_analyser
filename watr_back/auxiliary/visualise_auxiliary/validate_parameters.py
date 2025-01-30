from flask import abort


def validate_rdf_class(rdf_class):
    """
    Validates the 'class' query parameter.
    """
    if not rdf_class or not isinstance(rdf_class, str):
        abort(400, description="The 'class' parameter is required and must be a string.")
    return rdf_class

def validate_limit_and_count_limit(limit_param, count_limit_param):
    """
    Validates the 'limit' and 'count_limit' query parameters.
    """
    # Validate 'limit' parameter
    if not limit_param or not isinstance(limit_param, str):
        abort(400, description="The 'limit' parameter is required and must be a string ('true' or 'false').")
    limit = limit_param.lower() == 'true'

    # Validate 'count_limit' parameter if 'limit' is True
    count_limit = None
    if limit:
        if not count_limit_param:
            abort(400, description="The 'count_limit' parameter is required when 'limit' is true.")
        try:
            count_limit = int(count_limit_param)
            if count_limit < 1:
                abort(400, description="The 'count_limit' parameter must be a positive integer.")
        except ValueError:
            abort(400, description="The 'count_limit' parameter must be a valid integer.")

    return limit, count_limit