def process_visualise_results(output):

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
