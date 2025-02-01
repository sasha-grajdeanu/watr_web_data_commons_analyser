ALIGNMENT_QUERY = """
CONSTRUCT{
    ?s ?p ?o
}
WHERE{
    GRAPH ?g{
        ?s ?p ?o .
    }
}
"""
