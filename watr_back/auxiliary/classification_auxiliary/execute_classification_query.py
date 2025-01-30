import os

from SPARQLWrapper import SPARQLWrapper, JSON

from sparql_queries.classification_queries import CLASSIFY_QUERY

sparql = SPARQLWrapper(os.environ['SPARQL_ENDPOINT'])


def execute_classification_query(rdf_class, rdf_property):
    """
    Helper function to execute the SPARQL query and return results.
    """
    sparql_query = CLASSIFY_QUERY.format(rdf_class=rdf_class, property=rdf_property)
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    output = sparql.query().convert()
    return output
