from auxiliary.compare_auxiliary.execute_compare_query import execute_compare_query
from auxiliary.compare_auxiliary.generate_html_compare import generate_html_compare


def compare_html_service(class_one, class_two):
    try:
        output = execute_compare_query(class_one, class_two)
        init_result = output['results']['bindings']
        return generate_html_compare(init_result, class_one, class_two)

    except Exception as e:
        return f"<h3>Error: {e}</h3>", 500
