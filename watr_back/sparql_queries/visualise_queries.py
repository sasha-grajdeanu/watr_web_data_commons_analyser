VISUALISE_QUERY = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX schema: <http://schema.org/>
SELECT ?entity ?property ?value ?bnodeProperty ?bnodeValue
WHERE {{
  GRAPH ?graph {{ 
    ?entity rdf:type schema:{rdf_class};  # Searching for entities of the specified RDF class
            ?property ?value.            # Entity has some property and value

    # Check if the value is a blank node (bnode) and explore further
    OPTIONAL {{
      ?value ?bnodeProperty ?bnodeValue.  # If value is a bnode, follow its properties
      FILTER(isBlank(?value))            # Ensure that the value is a blank node
    }}
  }}
}}
"""
