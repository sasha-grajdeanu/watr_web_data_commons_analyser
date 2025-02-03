import os

from SPARQLWrapper import SPARQLWrapper, JSON

from sparql_queries.comparation_queries import COMPARATION_QUERY

sparql = SPARQLWrapper(os.getenv('SPARQL_ENDPOINT'))


def execute_compare_query(class_one, class_two):

    sparql_query = COMPARATION_QUERY.format(class_one=class_one, class_two=class_two)
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    output = sparql.query().convert()
    return output
