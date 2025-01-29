from collections import defaultdict

from flask import jsonify

from auxiliary.visualise_auxiliary.execute_visualise_query import execute_sparql_query
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD

def compute_statistics(query_results):
    """
    Compute statistics from the query results.
    """
    # Initialize data structures
    unique_entities = list()
    values = list()
    properties_list = list()
    init_value = None
    # Iterate through the query results
    for result in query_results['results']['bindings']:
        # Extract entity, property, and value
        entity = result['entity']
        property_uri = result['property']['value']
        value = result['value']
        if entity not in unique_entities:
            unique_entities.append(entity)
        if value not in values:
            values.append(value)
        if init_value != value:
            properties_list.append(property_uri)
        init_value = value

    type_entity = dict()
    for entity in unique_entities:
        if entity['type'] not in type_entity:
            type_entity[entity['type']] = 1
        else:
            type_entity[entity['type']] += 1
    # Prepare the statistics
    print(type_entity)
    properties_type = dict()
    for property in properties_list:
        if property not in properties_type:
            properties_type[property] = 1
        else:
            properties_type[property] += 1
    print(properties_type)
    value_type = dict()
    for value in values:
        if value['type'] not in value_type:
            value_type[value['type']] = 1
        else:
            value_type[value['type']] += 1
    print(value_type)

    statistics = {
        'unique_entities': len(unique_entities),
        'type_entity': type_entity,
        'properties_type': properties_type,
        'value_type': value_type
    }

    return statistics

def model_statistics_with_qb(statistics, dataset_uri="http://localhost:5000/watr/dataset/statistics"):
    """
    Model the statistics using the RDF Data Cube Vocabulary (QB) and return the result in JSON-LD format.

    :param statistics: The output of compute_statistics.
    :param dataset_uri: The URI for the dataset (default: "http://localhost:5000/watr/dataset/statistics").
    :return: A JSON-LD representation of the RDF graph.
    """
    # Define namespaces
    QB = Namespace("http://purl.org/linked-data/cube#")
    SCHEMA = Namespace("http://schema.org/")
    WATR = Namespace("http://localhost:5000/watr/")

    # Initialize the RDF graph
    graph = Graph()

    # Bind namespaces
    graph.bind("qb", QB)
    graph.bind("schema", SCHEMA)
    graph.bind("example", WATR)

    # Define dataset
    dataset = URIRef(dataset_uri)
    graph.add((dataset, RDF.type, QB.DataSet))
    graph.add((dataset, RDFS.label, Literal("Statistics Dataset")))
    graph.add((dataset, QB.structure, URIRef(dataset_uri + "/structure")))

    # Define Data Structure Definition (DSD)
    dsd = URIRef(dataset_uri + "/structure")
    graph.add((dsd, RDF.type, QB.DataStructureDefinition))

    # Define dimensions and measures
    entity_type_dim = URIRef(dataset_uri + "/dimension/entityType")
    property_type_dim = URIRef(dataset_uri + "/dimension/propertyType")
    value_type_dim = URIRef(dataset_uri + "/dimension/valueType")
    count_measure = URIRef(dataset_uri + "/measure/count")

    graph.add((entity_type_dim, RDF.type, QB.DimensionProperty))
    graph.add((entity_type_dim, RDFS.label, Literal("Entity Type")))
    graph.add((entity_type_dim, RDFS.range, XSD.string))

    graph.add((property_type_dim, RDF.type, QB.DimensionProperty))
    graph.add((property_type_dim, RDFS.label, Literal("Property Type")))
    graph.add((property_type_dim, RDFS.range, XSD.string))

    graph.add((value_type_dim, RDF.type, QB.DimensionProperty))
    graph.add((value_type_dim, RDFS.label, Literal("Value Type")))
    graph.add((value_type_dim, RDFS.range, XSD.string))

    graph.add((count_measure, RDF.type, QB.MeasureProperty))
    graph.add((count_measure, RDFS.label, Literal("Count")))
    graph.add((count_measure, RDFS.range, XSD.integer))

    # Add components to DSD
    graph.add((dsd, QB.component, entity_type_dim))
    graph.add((dsd, QB.component, property_type_dim))
    graph.add((dsd, QB.component, value_type_dim))
    graph.add((dsd, QB.component, count_measure))

    # Create observations
    observation_id = 1

    # Iterate over properties_type
    for property_uri, count in statistics["properties_type"].items():
        observation_uri = URIRef(dataset_uri + f"/observation{observation_id}")
        graph.add((observation_uri, RDF.type, QB.Observation))
        graph.add((observation_uri, QB.dataSet, dataset))
        graph.add((observation_uri, entity_type_dim, Literal("uri")))  # Default entity type
        graph.add((observation_uri, property_type_dim, Literal(property_uri)))
        graph.add((observation_uri, value_type_dim, Literal("literal")))  # Default value type
        graph.add((observation_uri, count_measure, Literal(count, datatype=XSD.integer)))
        observation_id += 1

    # Iterate over type_entity
    for entity_type, count in statistics["type_entity"].items():
        observation_uri = URIRef(dataset_uri + f"/observation{observation_id}")
        graph.add((observation_uri, RDF.type, QB.Observation))
        graph.add((observation_uri, QB.dataSet, dataset))
        graph.add((observation_uri, entity_type_dim, Literal(entity_type)))
        graph.add((observation_uri, property_type_dim, Literal("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")))  # Default property
        graph.add((observation_uri, value_type_dim, Literal("uri")))  # Default value type
        graph.add((observation_uri, count_measure, Literal(count, datatype=XSD.integer)))
        observation_id += 1

    # Iterate over value_type
    for value_type, count in statistics["value_type"].items():
        observation_uri = URIRef(dataset_uri + f"/observation{observation_id}")
        graph.add((observation_uri, RDF.type, QB.Observation))
        graph.add((observation_uri, QB.dataSet, dataset))
        graph.add((observation_uri, entity_type_dim, Literal("uri")))  # Default entity type
        graph.add((observation_uri, property_type_dim, Literal("http://schema.org/value")))  # Default property
        graph.add((observation_uri, value_type_dim, Literal(value_type)))
        graph.add((observation_uri, count_measure, Literal(count, datatype=XSD.integer)))
        observation_id += 1

    # Serialize the graph to JSON-LD
    json_ld = graph.serialize(format="json-ld", indent=None)
    return json_ld


def return_statistics(rdf_class, limit, count_limit):
    init_result = execute_sparql_query(rdf_class, limit, count_limit)
    res = compute_statistics(init_result)
    print(res)
    return res


def download_statistics(rdf_class, limit, count_limit):
    """
    Controller for handling requests to visualise statistics.
    """
    # Validate and extract query parameters
    init_result = execute_sparql_query(rdf_class, limit, count_limit)
    res = compute_statistics(init_result)
    res = model_statistics_with_qb(res)
    print(res)
    return res