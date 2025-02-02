import os

from SPARQLWrapper import SPARQLWrapper, TURTLE

from sparql_queries.alignment_queries import ALIGNMENT_QUERY

sparql = SPARQLWrapper(os.getenv('SPARQL_ENDPOINT'))


def execute_alignment_query():
    """
    Helper function to execute the SPARQL query
    """
    sparql_query = ALIGNMENT_QUERY
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(TURTLE)
    output = sparql.query().convert()
    return output
