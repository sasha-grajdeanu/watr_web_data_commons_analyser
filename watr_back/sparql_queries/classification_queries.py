CLASSIFY_QUERY = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX schema: <http://schema.org/>
SELECT ?initial_subject ?initial_predicate ?blankNode 
       ?level1_predicate ?level1_object 
       ?level2_predicate ?level2_object 
       ?level3_predicate ?level3_object
WHERE {{
    GRAPH ?graph {{
        ?initial_subject rdf:type schema:{rdf_class} .  
        ?initial_subject ?initial_predicate ?blankNode .  
        FILTER (?initial_predicate = {property})
        
        # FILTER (!isBlank(?initial_subject))

        OPTIONAL {{
            ?blankNode ?level1_predicate ?level1_object .

            OPTIONAL {{
                ?level1_object ?level2_predicate ?level2_object .

                OPTIONAL {{
                    ?level2_object ?level3_predicate ?level3_object .
                }}
            }}
        }}
    }}
}}

"""
