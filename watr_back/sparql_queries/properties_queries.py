GET_DISTINCT_PROPERTIES = """
PREFIX schema: <http://schema.org/>
 SELECT DISTINCT ?property
    WHERE {{
        GRAPH ?graph{{
            ?subject a schema:{rdf_class} ;
                 ?property ?object .
        }}
    }}
"""
