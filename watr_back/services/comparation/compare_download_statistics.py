from flask import abort
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, XSD

from services.comparation.compare_statistics_service import compare_statistics_service

QB = Namespace("http://purl.org/linked-data/cube#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
DCT = Namespace("http://purl.org/dc/terms/")
SCHEMA = Namespace("http://schema.org/")
WATR = Namespace("http://localhost:5000/watr#")


def compare_download_statistics_service(class_one, class_two):
    try:
        statistics = compare_statistics_service(class_one, class_two)
        g = Graph()
        g.bind("qb", QB)
        g.bind("rdfs", RDFS)
        g.bind("dct", DCT)
        g.bind("watr", WATR)
        g.bind("schema", SCHEMA)

        dataset = URIRef("http://localhost:5000/watr/dataset/compare_statistics")
        g.add((dataset, RDF.type, QB.DataSet))

        property_dimension = URIRef("http://localhost:5000/watr/dimension/property")
        count_measure = URIRef("http://localhost:5000/watr/measure/count")
        class_dimension = URIRef("http://localhost:5000/watr/dimension/class")

        g.add((property_dimension, RDF.type, QB.DimensionProperty))
        g.add((count_measure, RDF.type, QB.MeasureProperty))
        g.add((class_dimension, RDF.type, QB.DimensionProperty))
        for class_name, stats in statistics.items():
            if class_name == "common_properties":
                continue

            for prop in stats["properties"]:
                observation = URIRef(f"http://localhost:5000/watr/observation/{class_name}_{prop.split('/')[-1]}")
                g.add((observation, RDF.type, QB.Observation))
                g.add((observation, QB.dataSet, dataset))
                g.add((observation, property_dimension, URIRef(prop)))
                g.add((observation, class_dimension, Literal(class_name)))
                g.add((observation, count_measure, Literal(1, datatype=XSD.integer)))

            if stats["most_used"]:
                observation_most_used = URIRef(f"http://localhost:5000/watr/observation/{class_name}_most_used")
                g.add((observation_most_used, RDF.type, QB.Observation))
                g.add((observation_most_used, QB.dataSet, dataset))
                g.add((observation_most_used, property_dimension, URIRef(stats["most_used"])))
                g.add((observation_most_used, class_dimension, Literal(class_name)))
                g.add((observation_most_used, count_measure, Literal(stats["total_count"], datatype=XSD.integer)))
            if stats["least_used"]:
                observation_least_used = URIRef(f"http://localhost:5000/watr/observation/{class_name}_least_used")
                g.add((observation_least_used, RDF.type, QB.Observation))
                g.add((observation_least_used, QB.dataSet, dataset))
                g.add((observation_least_used, property_dimension, URIRef(stats["least_used"])))
                g.add((observation_least_used, class_dimension, Literal(class_name)))
                g.add(
                    (observation_least_used, count_measure, Literal(1, datatype=XSD.integer)))

        for prop in statistics["common_properties"]:
            observation_common = URIRef(f"http://localhost:5000/watr/observation/common_{prop.split('/')[-1]}")
            g.add((observation_common, RDF.type, QB.Observation))
            g.add((observation_common, QB.dataSet, dataset))
            g.add((observation_common, property_dimension, URIRef(prop)))
            g.add((observation_common, class_dimension, Literal("common")))
            g.add((observation_common, count_measure,
                   Literal(2, datatype=XSD.integer)))

        return g.serialize(format="json-ld", indent=None)
    except Exception as e:
        return abort(500, description=f"An error occurred: {e}")
