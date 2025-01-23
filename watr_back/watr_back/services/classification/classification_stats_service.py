from flask import abort
from rdflib import Graph, Namespace, URIRef, Literal, BNode
from rdflib.namespace import RDF, XSD

RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
QB = Namespace("http://purl.org/linked-data/cube#")
SCHEMA = Namespace("http://schema.org/")
EX = Namespace("http://example.org/ns#")

def get_classification_stats(classify_data):
    try:
        graph = create_rdf_graph()
        index = 0

        for result in classify_data:
            subject = result.get("initial_subject")
            predicate = result.get("initial_predicate")

            if subject.startswith("b"):
                subject_uri = BNode(subject)
            else:
                subject_uri = URIRef(subject)

            levels=[]
            level_no = 1
            for level in range(1, 4):
                level_predicate = result.get(f"level{level}_predicate")
                if level_predicate:
                    levels.append(level_predicate)
                    level_no += 1
                else:
                    break


            index += 1

            add_observation_to_graph(graph, subject_uri, predicate, level_no, index)

        json_ld = graph.serialize(format="json-ld", indent=4)
        json = simplify_json_ld(json_ld)
        return json, 200

    except Exception as e:
        return abort(500, f"An error occurred: {e}")


def create_rdf_graph():
    graph = Graph()
    graph.bind("qb", QB)
    graph.bind("rdf", RDF)
    graph.bind("schema", SCHEMA)
    graph.bind("ex", EX)

    dataset_uri = EX.classificationDataset
    graph.add((dataset_uri, RDF.type, QB.Dataset))

    structure_uri = EX.classificationStructure
    graph.add((structure_uri, RDF.type, QB.DataStructureDefinition))

    subject_dimension = EX.initialSubject
    predicate_dimension = EX.initialPredicate
    levels_no_dimension = EX.numberOfLevels
    graph.add((structure_uri, QB.component, subject_dimension))
    graph.add((structure_uri, QB.component, predicate_dimension))
    graph.add((structure_uri, QB.component, levels_no_dimension))

    return graph


def add_observation_to_graph(graph, subject_uri, predicate, level_no, index):

    predicate_uri = URIRef(predicate)
    level_no_literal = Literal(level_no, datatype=XSD.integer)

    observation_uri = EX[f"observation_{index}"]

    graph.add((observation_uri, RDF.type, QB.Observation))
    graph.add((observation_uri, SCHEMA.initialSubject, subject_uri))
    graph.add((observation_uri, EX.initialPredicate, predicate_uri))
    graph.add((observation_uri, EX.numberOfLevels, level_no_literal))


def simplify_json_ld(json_ld_str):
    graph = Graph()
    graph.parse(data=json_ld_str, format='json-ld')

    simplified_data = []

    for observation in graph.subjects(RDF.type, QB.Observation):
        initial_subject = str(graph.value(observation, SCHEMA.initialSubject))
        initial_predicate = str(graph.value(observation, EX.initialPredicate))
        number_of_levels = str(graph.value(observation, EX.numberOfLevels))

        simplified_entry = {
            'initialSubject': initial_subject,
            'initialPredicate': initial_predicate,
            'numberOfLevels': number_of_levels,
        }
        simplified_data.append(simplified_entry)

    return simplified_data

