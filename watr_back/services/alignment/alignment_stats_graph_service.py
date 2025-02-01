import tempfile

from flask import abort
from rdflib import Namespace, Graph, RDFS, Literal, URIRef, XSD

from services.alignment.alignment_stats_service import alignment_stats_service
from services.alignment.alignment_table_service import alignment_table_service

RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
QB = Namespace("http://purl.org/linked-data/cube#")
SCHEMA = Namespace("http://schema.org/")
WATR = Namespace("http://localhost/watr#")


def alignment_stats_graph_service(target_ontology):
    """
    Function that creates RDF graphs for alignment statistics.
    """
    average_measure = alignment_stats_service(target_ontology)
    relations = alignment_table_service(target_ontology)

    graph = create_rdf_graph()

    for index, relation_data in enumerate(relations):
        add_relation_to_graph(graph, relation_data, index)

    add_average_measure_to_graph(graph, average_measure)

    graph_path = create_path_stats(graph)

    return graph_path


def create_rdf_graph():
    graph = Graph()
    graph.bind("qb", QB)
    graph.bind("rdf", RDF)
    graph.bind("schema", SCHEMA)
    graph.bind("watr", WATR)

    dataset_uri = WATR.alignmentDataset
    graph.add((dataset_uri, RDF.type, QB.Dataset))
    graph.add((dataset_uri, RDFS.label, Literal("Alignment Dataset")))
    graph.add((dataset_uri, RDFS.comment, Literal("This dataset contains a few alignment statistics.")))

    return graph


def add_relation_to_graph(graph, relation_data, index):
    original_uri = URIRef(relation_data["originalEntity"])
    aligned_uri = URIRef(relation_data["alignedEntity"])
    relation = relation_data["relation"]

    observation_uri = WATR[f"observation_{index}"]
    graph.add((observation_uri, RDF.type, QB.Observation))

    if relation == "=":
        relation_uri = WATR.equalsRelation
    elif relation == "<":
        relation_uri = WATR.lessRelation
    elif relation == ">":
        relation_uri = WATR.greaterRelation
    else:
        relation_uri = URIRef(relation)

    graph.add((observation_uri, relation_uri, original_uri))
    graph.add((observation_uri, relation_uri, aligned_uri))


def add_average_measure_to_graph(graph, average_measure):
    average_observation_uri = WATR.averageObservation
    graph.add((average_observation_uri, RDF.type, QB.Observation))
    graph.add((average_observation_uri, WATR.measure, Literal(average_measure, datatype=XSD.float)))
    graph.add((average_observation_uri, RDFS.label, Literal("Average Measure")))


def create_path_stats(graph):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".ttl")

    try:
        with open(temp_file.name, "wb") as f:
            graph.serialize(f, format='turtle')
    except Exception as e:
        abort(500,f"Error: {e}")

    return temp_file.name
