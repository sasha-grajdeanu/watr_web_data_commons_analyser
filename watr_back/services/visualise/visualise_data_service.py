from auxiliary.visualise_auxiliary.execute_visualise_query import execute_visualise_query
from auxiliary.visualise_auxiliary.process_visualise_results import process_visualise_results


def visualise_data_service(rdf_class, limit, count_limit):
    try:
        output = execute_visualise_query(rdf_class, limit, count_limit)
        init_results = process_visualise_results(output)

        return init_results
    except Exception as e:
        return e
