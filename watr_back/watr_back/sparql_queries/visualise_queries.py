VISUALISE_QUERY = """
SELECT ?entity ?entityProperty ?entityValue 
       ?property ?value ?bnodeProperty ?bnodeValue
WHERE {
  GRAPH ?graph { 
    # Retrieve entities of type AdministrativeArea
    ?entity a <http://schema.org/AdministrativeArea>;
            ?property ?value.                       # Retrieve properties of the entity

    # If the entity itself is a blank node, explore its deeper properties
    OPTIONAL {
      ?entity ?entityProperty ?entityValue.         # Follow deeper properties of the entity
      FILTER(isBlank(?entity))                     # Ensure ?entity is a blank node
    }

    # If the value is a blank node, explore its deeper properties
    OPTIONAL {
      ?value ?bnodeProperty ?bnodeValue.            # Follow deeper properties of ?value
      FILTER(isBlank(?value))                      # Ensure ?value is a blank node
    }
  }
}

"""