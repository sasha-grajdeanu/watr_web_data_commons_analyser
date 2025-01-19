from SPARQLWrapper import SPARQLWrapper, JSON
from flask import jsonify

from ..sparql_queries.classification_queries import CLASSIFY_QUERY


def classify(rdf_class, rdf_property):

    sparql_query = CLASSIFY_QUERY.format(rdf_class=rdf_class, property=rdf_property)
    sparql = SPARQLWrapper("http://localhost:3030/watr-dataset/sparql")
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        output = []
        for result in results["results"]["bindings"]:
            output.append({
                "subject": result["subject"]["value"],
                "predicate": result["predicate"]["value"],
                "object": result["object"]["value"],
            })
        return jsonify(output)
    except Exception as e:
        return jsonify({"error": str(e)}), 500