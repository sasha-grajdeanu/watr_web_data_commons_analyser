from SPARQLWrapper import SPARQLWrapper, JSON
from flask import jsonify
from sparql_queries.visualise_queries import VISUALISE_QUERY
from enviromment.enviromment import SPARQL_ENDPOINT

sparql = SPARQLWrapper(SPARQL_ENDPOINT)

def visualise_service_json_ld(rdf_class, limit, count_limit):
    print(rdf_class)
    print(limit)
    print(count_limit)
    if limit:
        sparql_query = VISUALISE_QUERY.format(rdf_class=rdf_class) + f" LIMIT {count_limit}"
    else:
        sparql_query = VISUALISE_QUERY.format(rdf_class=rdf_class)
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)

    try:
        output = sparql.query().convert()
        json_ld = {
            "@context": {
                "entity": "http://example.org/entity",
                "property": "http://example.org/property",
                "value": "http://example.org/value",
                "bnodeProperty": "http://example.org/bnodeProperty",
                "bnodeValue": "http://example.org/bnodeValue"
            },
            "@graph": []
        }

        for elements in output['results']['bindings']:
            node = {
                "@id": elements.get('entity', {}).get('value'),
                "property": elements.get('property', {}).get('value'),
                "value": elements.get('value', {}).get('value'),
            }
            if "bnodeProperty" in elements and "bnodeValue" in elements:
                node["bnodeProperty"] = elements['bnodeProperty']['value']
                node["bnodeValue"] = elements['bnodeValue']['value']
            json_ld["@graph"].append(node)

        return jsonify(json_ld)
    except Exception as e:
        return jsonify({"error": f"An error occurred {e}"}), 500