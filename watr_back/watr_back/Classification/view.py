from flask import Blueprint, request, jsonify, abort
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib.namespace import Namespace

classification = Blueprint('classification', __name__)


@classification.route('/classify', methods=['POST'])
def classify():
    data = request.json
    rdf_class = data.get('class')
    property = data.get('property')

    if not rdf_class or not isinstance(rdf_class, str):
        abort(400, description="Invalid or missing \'class\' parameter.")

    if not property or not isinstance(property, str):
        abort(400, description="Invalid or missing \'property\' parameter.")


    # select all N-Quads of subject rdf_class (ex.: AdministrativeArea)
    # check if the predicate is rdf:type and object matches the schema:rdf_class
    # check if the predicate is schema:property (ex.: containsPlace)

    sparql_query = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX schema: <http://schema.org/>
    SELECT ?subject ?predicate ?object
    WHERE {{
        GRAPH ?graph {{
            ?subject rdf:type schema:{rdf_class} .
            ?subject ?predicate ?object .
            FILTER ((?predicate = rdf:type && ?object = schema:{rdf_class}) || ?predicate = schema:{property}) 
        }}
    }}
    """

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