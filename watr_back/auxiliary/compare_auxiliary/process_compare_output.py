def process_compare_sparql_results(output, class_one, class_two):
    """
    Helper function to process SPARQL results for comparison into a list of rows.
    """
    init_result = []
    for elements in output['results']['bindings']:
        row = {
            "property": elements.get('property', {}).get('value'),
            class_one: elements.get('class_one_count', {}).get('value'),
            class_two: elements.get('class_two_count', {}).get('value'),
        }
        init_result.append(row)
    return init_result
