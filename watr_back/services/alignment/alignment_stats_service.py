import tempfile
import xml.etree.ElementTree as ET

from flask import jsonify
from rdflib import Graph, Namespace, RDFS, Literal, XSD, URIRef


NAMESPACES = {
            'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'alignment': 'http://knowledgeweb.semanticweb.org/heterogeneity/alignment'
        }

RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
QB = Namespace("http://purl.org/linked-data/cube#")
SCHEMA = Namespace("http://schema.org/")
WATR = Namespace("http://localhost/watr#")

def get_alignment_stats(align_file):
    graph = create_rdf_graph()

    tree = ET.parse(align_file)
    root = tree.getroot()

    total_cells = 0
    total_measure = 0.0
    relations = set()

    index = 0

    for map_element in root.findall(".//alignment:map", NAMESPACES):
        for cell in map_element.findall("alignment:Cell", NAMESPACES):
            total_cells += 1

            measure = cell.find("alignment:measure", NAMESPACES)
            measure_value = float(measure.text)
            total_measure += measure_value


            relation = cell.find("alignment:relation", NAMESPACES)
            relations.add(relation.text)

            add_observation_to_graph(graph, measure_value, relation.text, index)
            index +=1


    average_measure = total_measure / total_cells if total_cells > 0 else 0.0
    add_average_measure_to_graph(graph, average_measure)

    json_ld = graph.serialize(format="json-ld", indent=4)
    json = simplify_json_ld(json_ld)

    stats_path = create_path_stats(graph)
    return jsonify({"stats": average_measure, "graph_file":stats_path})


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

    structure_uri = WATR.alignmentStructure
    graph.add((structure_uri, RDF.type, QB.DataStructureDefinition))

    alignment_cell = WATR.alignmentCell
    alignment_measure = WATR.measure
    alignment_relation = WATR.relation
    graph.add((structure_uri, QB.component, alignment_cell))
    graph.add((structure_uri, QB.component, alignment_measure))
    graph.add((structure_uri, QB.component, alignment_relation))

    return graph

def add_observation_to_graph(graph, measure_value, relation, index):
    observation_uri = WATR[f"observation_{index}"]
    graph.add((observation_uri, RDF.type, QB.Observation))
    graph.add((observation_uri, WATR.measure, Literal(measure_value, datatype=XSD.float)))
    if relation == "=":
        relation_uri = WATR.equalsRelation
    elif relation == "<":
        relation_uri = WATR.lessRelation
    elif relation == ">":
        relation_uri = WATR.greaterRelation
    else:
        relation_uri = URIRef(relation)
    graph.add((observation_uri, WATR.relation, relation_uri))

def add_average_measure_to_graph(graph, average_measure):
    average_observation_uri = WATR.averageObservation
    graph.add((average_observation_uri, RDF.type, QB.Observation))
    graph.add((average_observation_uri, WATR.measure, Literal(average_measure, datatype=XSD.float)))
    graph.add((average_observation_uri, RDFS.label, Literal("Average Measure")))

def simplify_json_ld(json_ld_str):
    graph = Graph()
    graph.parse(data=json_ld_str, format='json-ld')

    simplified_data = []

    for observation in graph.subjects(RDF.type, QB.Observation):
        measure = graph.value(observation, WATR.measure)
        relation = graph.value(observation, WATR.relation)

        simplified_data.append({
            "measure": measure.toPython() if measure else None,
            "relation": relation.toPython() if relation else None
        })

    return simplified_data

def create_path_stats(graph):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".ttl")

    try:
        with open(temp_file.name, "wb") as f:
            graph.serialize(f, format='turtle')
    except Exception as e:
        print(f"Error: {e}")

    return temp_file.name