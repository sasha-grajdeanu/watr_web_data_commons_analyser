from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD

from auxiliary.visualise_auxiliary.execute_visualise_query import execute_visualise_query


def download_statistics(rdf_class, limit, count_limit):
    init_result = execute_visualise_query(rdf_class, limit, count_limit)
    res = compute_statistics(init_result)
    res = model_statistics_with_qb(res)
    return res


def return_statistics(rdf_class, limit, count_limit):
    init_result = execute_visualise_query(rdf_class, limit, count_limit)
    res = compute_statistics(init_result)
    return res


def compute_statistics(query_results):
    unique_entities = list()
    values = list()
    properties_list = list()
    init_value = None
    for result in query_results['results']['bindings']:
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
    properties_type = dict()
    for property in properties_list:
        if property not in properties_type:
            properties_type[property] = 1
        else:
            properties_type[property] += 1
    value_type = dict()
    for value in values:
        if value['type'] not in value_type:
            value_type[value['type']] = 1
        else:
            value_type[value['type']] += 1

    statistics = {
        'unique_entities': len(unique_entities),
        'type_entity': type_entity,
        'properties_type': properties_type,
        'value_type': value_type
    }

    return statistics


def model_statistics_with_qb(statistics, dataset_uri="http://localhost:5000/watr/dataset/statistics"):
    QB = Namespace("http://purl.org/linked-data/cube#")
    SCHEMA = Namespace("http://schema.org/")
    WATR = Namespace("http://localhost:5000/watr/")

    graph = Graph()

    graph.bind("qb", QB)
    graph.bind("schema", SCHEMA)
    graph.bind("example", WATR)

    dataset = URIRef(dataset_uri)
    graph.add((dataset, RDF.type, QB.DataSet))
    graph.add((dataset, RDFS.label, Literal("Statistics Dataset")))
    graph.add((dataset, QB.structure, URIRef(dataset_uri + "/structure")))

    dsd = URIRef(dataset_uri + "/structure")
    graph.add((dsd, RDF.type, QB.DataStructureDefinition))

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

    graph.add((dsd, QB.component, entity_type_dim))
    graph.add((dsd, QB.component, property_type_dim))
    graph.add((dsd, QB.component, value_type_dim))
    graph.add((dsd, QB.component, count_measure))

    observation_id = 1

    for property_uri, count in statistics["properties_type"].items():
        observation_uri = URIRef(dataset_uri + f"/observation{observation_id}")
        graph.add((observation_uri, RDF.type, QB.Observation))
        graph.add((observation_uri, QB.dataSet, dataset))
        graph.add((observation_uri, entity_type_dim, Literal("uri")))
        graph.add((observation_uri, property_type_dim, Literal(property_uri)))
        graph.add((observation_uri, value_type_dim, Literal("literal")))
        graph.add((observation_uri, count_measure, Literal(count, datatype=XSD.integer)))
        observation_id += 1

    for entity_type, count in statistics["type_entity"].items():
        observation_uri = URIRef(dataset_uri + f"/observation{observation_id}")
        graph.add((observation_uri, RDF.type, QB.Observation))
        graph.add((observation_uri, QB.dataSet, dataset))
        graph.add((observation_uri, entity_type_dim, Literal(entity_type)))
        graph.add((observation_uri, property_type_dim,
                   Literal("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")))
        graph.add((observation_uri, value_type_dim, Literal("uri")))
        graph.add((observation_uri, count_measure, Literal(count, datatype=XSD.integer)))
        observation_id += 1

    for value_type, count in statistics["value_type"].items():
        observation_uri = URIRef(dataset_uri + f"/observation{observation_id}")
        graph.add((observation_uri, RDF.type, QB.Observation))
        graph.add((observation_uri, QB.dataSet, dataset))
        graph.add((observation_uri, entity_type_dim, Literal("uri")))
        graph.add((observation_uri, property_type_dim, Literal("http://schema.org/value")))
        graph.add((observation_uri, value_type_dim, Literal(value_type)))
        graph.add((observation_uri, count_measure, Literal(count, datatype=XSD.integer)))
        observation_id += 1

    json_ld = graph.serialize(format="json-ld", indent=None)
    return json_ld
