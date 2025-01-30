def process_sparql_results(output):
    """
    Helper function to process SPARQL results into a list of rows.
    """
    init_result = []
    for elements in output['results']['bindings']:
        row = {
            "entity": elements.get('entity', {}).get('value'),
            "property": elements.get('property', {}).get('value'),
            "value": elements.get('value', {}).get('value'),
        }
        if "bnodeProperty" in elements and "bnodeValue" in elements:
            row["bnodeProperty"] = elements['bnodeProperty']['value']
            row["bnodeValue"] = elements['bnodeValue']['value']
        init_result.append(row)
    return init_result