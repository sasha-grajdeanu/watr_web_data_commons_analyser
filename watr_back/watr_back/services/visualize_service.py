from SPARQLWrapper import SPARQLWrapper, JSON
from flask import jsonify, send_file
from sparql_queries.visualise_queries import VISUALISE_QUERY
from auxiliary.write_graph_format import write_graph_format
from auxiliary.create_graph_base import create_init_graph
from enviromment.enviromment import SPARQL_ENDPOINT

sparql = SPARQLWrapper(SPARQL_ENDPOINT)


def visualise_service(rdf_class):
    print(rdf_class)
    sparql_query = VISUALISE_QUERY.format(rdf_class=rdf_class)
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)

    try:
        output = sparql.query().convert()
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
                # print(row)
            init_result.append(row)
        init_graph = create_init_graph(init_result)
        print(init_graph)
        final_graph = write_graph_format(init_graph)
        return send_file(final_graph, as_attachment=True, download_name="graph.graphml")
    except Exception as e:
        return jsonify({"error": f"An error occurred {e}"}), 500
