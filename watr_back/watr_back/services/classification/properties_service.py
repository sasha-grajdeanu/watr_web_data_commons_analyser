import os

from SPARQLWrapper import SPARQLWrapper, JSON
from flask import jsonify

from enviromment.enviromment import SPARQL_ENDPOINT
from sparql_queries.properties_queries import GET_DISTINCT_PROPERTIES

sparql = SPARQLWrapper(SPARQL_ENDPOINT)

def get_properties(rdf_class):
    sparql_query = GET_DISTINCT_PROPERTIES.format(rdf_class=rdf_class)
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        properties = [result["property"]["value"] for result in results["results"]["bindings"]]

        cleaned_properties = []
        for prop in properties:
            if "#" in prop:
                cleaned_properties.append("rdf:" + prop.split('/')[-1].split('#')[-1])
            else:
                cleaned_properties.append("schema:" + prop.split('/')[-1])
        return cleaned_properties

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500