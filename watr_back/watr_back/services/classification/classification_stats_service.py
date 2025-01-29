import tempfile

from flask import abort, jsonify
from rdflib import Graph, Namespace, URIRef, Literal, BNode, RDFS
from rdflib.namespace import RDF, XSD
from requests import delete

RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
QB = Namespace("http://purl.org/linked-data/cube#")
SCHEMA = Namespace("http://schema.org/")
WATR = Namespace("http://localhost/watr#")

def get_classification_stats(classify_data):
    try:
        graph = create_rdf_graph()
        unique_graph = create_rdf_graph(unique_subjects_graph=True)
        index = 0
        unique_subjects = {}

        for result in classify_data:
            subject = result.get("initial_subject")
            predicate = result.get("initial_predicate")

            if subject.startswith("b"):
                subject_uri = BNode(subject)
            else:
                subject_uri = URIRef(subject)

            levels = []
            level_no = 1
            for level in range(1, 4):
                level_predicate = result.get(f"level{level}_predicate")
                if level_predicate:
                    levels.append(level_predicate)
                    level_no += 1
                else:
                    break

            index += 1

            if subject not in unique_subjects:
                unique_subjects[subject] = 0
            unique_subjects[subject] += 1

            add_observation_to_graph(graph, subject_uri, predicate, level_no, index)

        # Add unique subject observations to a separate graph
        add_unique_subjects_to_graph(unique_graph, unique_subjects)

        json_ld = graph.serialize(format="json-ld", indent=4)
        unique_json_ld = unique_graph.serialize(format="json-ld", indent=4)

        graph_path = create_path_stats(graph)
        unique_graph_path = create_path_stats(unique_graph)

        json = simplify_json_ld(json_ld)
        unique_json = simplify_json_ld(unique_json_ld)

        return jsonify({"data": json,
                "unique_data": unique_json,
                "graph_file": graph_path,
                "unique_graph_file": unique_graph_path}), 200

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
        graph.add((dataset_uri, RDFS.comment, Literal("This dataset contains classification statistics regarding the number of levels of each possible triple.")))

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
        graph.add((dataset_uri, RDFS.comment, Literal("This dataset contains statistics about unique subjects and their occurrences.")))

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

def add_unique_subjects_to_graph(graph, unique_subjects):
    index = 0
    for subject, count in unique_subjects.items():
        index += 1
        subject_uri = URIRef(subject) if not subject.startswith("b") else BNode(subject)
        count_literal = Literal(count, datatype=XSD.integer)

        observation_uri = WATR[f"unique_subject_{index}"]

        graph.add((observation_uri, RDF.type, QB.Observation))
        graph.add((observation_uri, WATR.uniqueSubject, subject_uri))
        graph.add((observation_uri, WATR.numberOfOccurrences, count_literal))

def simplify_json_ld(json_ld_str):
    graph = Graph()
    graph.parse(data=json_ld_str, format='json-ld')

    simplified_data = []

    for observation in graph.subjects(RDF.type, QB.Observation):
        initial_subject = graph.value(observation, SCHEMA.initialSubject)
        initial_predicate = graph.value(observation, WATR.initialPredicate)
        number_of_levels = graph.value(observation, WATR.numberOfLevels)
        unique_subject = graph.value(observation, WATR.uniqueSubject)
        number_of_occurrences = graph.value(observation, WATR.numberOfOccurrences)

        if initial_subject and initial_predicate and number_of_levels:
            simplified_entry = {
                'initialSubject': str(initial_subject),
                'initialPredicate': str(initial_predicate),
                'numberOfLevels': str(number_of_levels),
            }
            simplified_data.append(simplified_entry)

        if unique_subject and number_of_occurrences:
            simplified_entry = {
                'uniqueSubject': str(unique_subject),
                'numberOfOccurrences': str(number_of_occurrences),
            }
            simplified_data.append(simplified_entry)

    return simplified_data

def create_path_stats(graph):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".ttl")

    try:
        with open(temp_file.name, "wb") as f:
            graph.serialize(f, format='turtle')
    except Exception as e:
        print(f"Error: {e}")

    return temp_file.name