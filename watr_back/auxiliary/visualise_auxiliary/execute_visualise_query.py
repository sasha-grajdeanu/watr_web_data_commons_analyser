import os

from SPARQLWrapper import SPARQLWrapper, JSON

from sparql_queries.visualise_queries import VISUALISE_QUERY

sparql = SPARQLWrapper(os.getenv('SPARQL_ENDPOINT'))


def execute_sparql_query(rdf_class, limit, count_limit):
    """
    Helper function to execute the SPARQL query and return the results.
    """
    if limit:
        sparql_query = VISUALISE_QUERY.format(rdf_class=rdf_class) + f" LIMIT {count_limit}"
    else:
        sparql_query = VISUALISE_QUERY.format(rdf_class=rdf_class)
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    output = sparql.query().convert()
    return output
