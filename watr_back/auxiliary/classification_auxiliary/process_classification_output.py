def process_classification_output(output):

    result = []
    for elements in output["results"]["bindings"]:
        row = {
            "initial_subject": elements.get("initial_subject", {}).get("value", None),
            "initial_predicate": elements.get("initial_predicate", {}).get("value", None),
            "blankNode": elements.get("blankNode", {}).get("value", None),
        }

        if "level1_predicate" in elements and "level1_object" in elements:
            row["level1_predicate"] = elements["level1_predicate"]["value"]
            row["level1_object"] = elements["level1_object"]["value"]

        if "level2_predicate" in elements and "level2_object" in elements:
            row["level2_predicate"] = elements["level2_predicate"]["value"]
            row["level2_object"] = elements["level2_object"]["value"]

        if "level3_predicate" in elements and "level3_object" in elements:
            row["level3_predicate"] = elements["level3_predicate"]["value"]
            row["level3_object"] = elements["level3_object"]["value"]

        result.append(row)
    return result
