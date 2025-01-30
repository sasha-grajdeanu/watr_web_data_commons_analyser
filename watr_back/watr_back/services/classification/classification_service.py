import os

from SPARQLWrapper import SPARQLWrapper, JSON
from flask import abort

from enviromment.enviromment import SPARQL_ENDPOINT
from sparql_queries.classification_queries import CLASSIFY_QUERY

sparql = SPARQLWrapper(SPARQL_ENDPOINT)


def classify(rdf_class, rdf_property):
    sparql_query = CLASSIFY_QUERY.format(rdf_class=rdf_class, property=rdf_property)
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
        return abort(500, f"An error occurred: {e}")

def convert_results_to_html(results):
    html_output = "<html><body><h1>Classification Results</h1><table>"
    html_output += ("<tr>"
                        "<th>Initial Subject</th>"
                        "<th>Initial Predicate</th>"
                        "<th>Blank Node</th>"
                        "<th>Level 1 Predicate</th>"
                        "<th>Level 1 Object</th>"
                        "<th>Level 2 Predicate</th>"
                        "<th>Level 2 Object</th>"
                        "<th>Level 3 Predicate</th>"
                        "<th>Level 3 Object</th>"
                    "</tr>")
    for row in results:
        html_output += f"<tr><td>{row.get('initial_subject', '')}</td><td>{row.get('initial_predicate', '')}</td><td>{row.get('blankNode', '')}</td>"
        html_output += f"<td>{row.get('level1_predicate', '')}</td><td>{row.get('level1_object', '')}</td>"
        html_output += f"<td>{row.get('level2_predicate', '')}</td><td>{row.get('level2_object', '')}</td>"
        html_output += f"<td>{row.get('level3_predicate', '')}</td><td>{row.get('level3_object', '')}</td></tr>"
    html_output += "</table></body></html>"
    return html_output


def convert_results_to_jsonld(results):
    jsonld_output = {
        "@context": "http://schema.org",
        "@type": "ClassificationResults",
        "results": []
    }

    for row in results:
        result_entry = {
            "initialSubject": row.get("initial_subject", ""),
            "initialPredicate": row.get("initial_predicate", ""),
            "blankNode": row.get("blankNode", ""),
            "level1Predicate": row.get("level1_predicate", ""),
            "level1Object": row.get("level1_object", ""),
            "level2Predicate": row.get("level2_predicate", ""),
            "level2Object": row.get("level2_object", ""),
            "level3Predicate": row.get("level3_predicate", ""),
            "level3Object": row.get("level3_object", ""),
        }
        jsonld_output["results"].append(result_entry)

    return jsonld_output