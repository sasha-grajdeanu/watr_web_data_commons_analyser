import tempfile

from flask import jsonify, abort
from rdflib import Namespace, BNode, URIRef, Graph, RDF, RDFS, Literal, XSD

from services.classification.classification_statistics_service import classification_statistics_service

QB = Namespace("http://purl.org/linked-data/cube#")
SCHEMA = Namespace("http://schema.org/")
WATR = Namespace("http://localhost/watr#")


def classification_statistics_graph_service(rdf_class, rdf_property):
    try:
        statistics = classification_statistics_service(rdf_class, rdf_property)

        graph = create_rdf_graph()
        unique_graph = create_rdf_graph(unique_subjects_graph=True)

        index = 0
        for observation in statistics["observations"]:
            index += 1
            subject = observation["initialSubject"]
            predicate = observation["initialPredicate"]
            level_no = observation["numberOfLevels"]

            subject_uri = BNode(subject) if subject.startswith("b") else URIRef(subject)
            add_observation_to_graph(graph, subject_uri, predicate, level_no, index)

        add_unique_subjects_to_graph(unique_graph, statistics)

        graph_path = create_path_stats(graph)
        unique_graph_path = create_path_stats(unique_graph)

        return jsonify({
            "graph_file": graph_path,
            "unique_graph_file": unique_graph_path
        }), 200

    except Exception as e:
        return abort(500, f"An error occurred: {e}")


def create_rdf_graph(unique_subjects_graph=False):
    graph = Graph()
    graph.bind("qb", QB)
    graph.bind("rdf", RDF)
    graph.bind("schema", SCHEMA)
    graph.bind("watr", WATR)

    if not unique_subjects_graph:
        dataset_uri = WATR.classificationDataset
        graph.add((dataset_uri, RDF.type, QB.Dataset))
        graph.add((dataset_uri, RDFS.label, Literal("Classification Dataset")))
        graph.add((dataset_uri, RDFS.comment, Literal(
            "This dataset contains classification statistics regarding the number of levels of each possible triple.")))

        structure_uri = WATR.classificationStructure
        graph.add((structure_uri, RDF.type, QB.DataStructureDefinition))

        subject_dimension = WATR.initialSubject
        predicate_dimension = WATR.initialPredicate
        levels_no_dimension = WATR.numberOfLevels
        graph.add((structure_uri, QB.component, subject_dimension))
        graph.add((structure_uri, QB.component, predicate_dimension))
        graph.add((structure_uri, QB.component, levels_no_dimension))
    else:
        dataset_uri = WATR.uniqueSubjectsDataset
        graph.add((dataset_uri, RDF.type, QB.Dataset))
        graph.add((dataset_uri, RDFS.label, Literal("Unique Subjects Dataset")))
        graph.add((dataset_uri, RDFS.comment,
                   Literal("This dataset contains statistics about unique subjects and their occurrences.")))

        structure_uri = WATR.uniqueSubjectsStructure
        graph.add((structure_uri, RDF.type, QB.DataStructureDefinition))

        subject_dimension = WATR.uniqueSubject
        occurrences_measure = WATR.numberOfOccurrences
        graph.add((structure_uri, QB.component, subject_dimension))
        graph.add((structure_uri, QB.component, occurrences_measure))

    return graph


def add_observation_to_graph(graph, subject_uri, predicate, level_no, index):
    predicate_uri = URIRef(predicate)
    level_no_literal = Literal(level_no, datatype=XSD.integer)

    observation_uri = WATR[f"observation_{index}"]

    graph.add((observation_uri, RDF.type, QB.Observation))
    graph.add((observation_uri, SCHEMA.initialSubject, subject_uri))
    graph.add((observation_uri, WATR.initialPredicate, predicate_uri))
    graph.add((observation_uri, WATR.numberOfLevels, level_no_literal))


def add_unique_subjects_to_graph(graph, statistics):
    index = 0
    for subject, count in statistics["unique_subjects"].items():
        index += 1
        subject_uri = URIRef(subject) if not subject.startswith("b") else BNode(subject)
        count_literal = Literal(count, datatype=XSD.integer)

        observation_uri = WATR[f"unique_subject_{index}"]

        graph.add((observation_uri, RDF.type, QB.Observation))
        graph.add((observation_uri, WATR.uniqueSubject, subject_uri))
        graph.add((observation_uri, WATR.numberOfOccurrences, count_literal))

    statistics_uri = WATR.statisticsDataset
    try:
        graph.add((statistics_uri, RDF.type, QB.Dataset))
        graph.add((statistics_uri, WATR.depthAverage, Literal(statistics["depth_average"], datatype=XSD.float)))
        graph.add((statistics_uri, WATR.minLevel, Literal(statistics["min_level"], datatype=XSD.integer)))
        graph.add((statistics_uri, WATR.maxLevel, Literal(statistics["max_level"], datatype=XSD.integer)))
        graph.add((statistics_uri, WATR.levelDistribution0,
                   Literal(statistics["level_distribution"].get("0_level", 0), datatype=XSD.integer)))
        graph.add((statistics_uri, WATR.levelDistribution1,
                   Literal(statistics["level_distribution"].get("1_level", 0), datatype=XSD.integer)))
        graph.add((statistics_uri, WATR.levelDistribution2,
                   Literal(statistics["level_distribution"].get("2_level", 0), datatype=XSD.integer)))
        graph.add((statistics_uri, WATR.levelDistribution3,
                   Literal(statistics["level_distribution"].get("3_level", 0), datatype=XSD.integer)))
    except KeyError as e:
        raise KeyError(f"Missing key in statistics: {e}")

def create_path_stats(graph):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".ttl")

    try:
        with open(temp_file.name, "wb") as f:
            graph.serialize(f, format='turtle')
    except Exception as e:
        abort(500, f"Error: {e}")

    return temp_file.name
