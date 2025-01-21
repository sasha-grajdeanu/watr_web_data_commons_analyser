from SPARQLWrapper import SPARQLWrapper, JSON
from flask import jsonify

from ..sparql_queries.classification_queries import CLASSIFY_NEW

sparql = SPARQLWrapper("http://localhost:3030/watr-dataset/sparql")

def classify(rdf_class, rdf_property):
    sparql_query = CLASSIFY_NEW.format(rdf_class=rdf_class, property=rdf_property)
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        output = []

        for result in results["results"]["bindings"]:
            row = {
                "initial_subject": result.get("initial_subject", {}).get("value", None),
                "initial_predicate": result.get("initial_predicate", {}).get("value", None),
                "blankNode": result.get("blankNode", {}).get("value", None),
            }

            # Check for level 1 data
            if "level1_predicate" in result and "level1_object" in result:
                row["level1_predicate"] = result["level1_predicate"]["value"]
                row["level1_object"] = result["level1_object"]["value"]


            # Check for level 2 data
            if "level2_predicate" in result and "level2_object" in result:
                row["level2_predicate"] = result["level2_predicate"]["value"]
                row["level2_object"] = result["level2_object"]["value"]


            # Check for level 3 data
            if "level3_predicate" in result and "level3_object" in result:
                row["level3_predicate"] = result["level3_predicate"]["value"]
                row["level3_object"] = result["level3_object"]["value"]


            output.append(row)

        return output
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
