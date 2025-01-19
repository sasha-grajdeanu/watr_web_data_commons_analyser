

CLASSIFY_QUERY = """
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
