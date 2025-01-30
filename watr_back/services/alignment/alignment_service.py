import json
import os
import subprocess
import tempfile
import xml.etree.ElementTree as ET

import rdflib
from SPARQLWrapper import SPARQLWrapper, TURTLE

from sparql_queries.alignment_queries import ALIGNMENT_QUERY

sparql = SPARQLWrapper(os.getenv('SPARQL_ENDPOINT'))

NAMESPACES = {
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'alignment': 'http://knowledgeweb.semanticweb.org/heterogeneity/alignment'
}

def align(target_ontology):
    sparql_query = ALIGNMENT_QUERY
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(TURTLE)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".nt")
    output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".nt")

    try:
        results = sparql.query().convert()
        with open(temp_file.name, "wb") as f:
            f.write(results)
    except Exception as e:
        print(f"Error: {e}")

    ontology_path = get_path(target_ontology)

    try:
        # comanda AML pentru aliniere
        aml_command = [
            "java", "-jar", "C:\\AML_v3.2\\AgreementMakerLight.jar",
            "-s", temp_file.name,
            "-t", ontology_path,
            "-o", output_file.name,
            "-a"
        ]

        subprocess.run(aml_command, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error during AML execution: {e}")
        return None

    return output_file.name


def get_path(target_ontology):
    if target_ontology == "schema.org":
        return './ontologies/schemaorg.rdf'
    elif target_ontology == "DBPedia":
        return './ontologies/dbpedia.nt'



def convert_results_to_html(align_data):
    try:
        tree = ET.parse(align_data)
        root = tree.getroot()

        alignment_data = []

        for map_elem in root.findall('.//alignment:map', NAMESPACES):
            for cell_elem in map_elem.findall('alignment:Cell', NAMESPACES):
                entity1 = cell_elem.find('alignment:entity1', NAMESPACES).attrib.get(
                    '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', None)
                entity2 = cell_elem.find('alignment:entity2', NAMESPACES).attrib.get(
                    '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', None)
                measure = cell_elem.find('alignment:measure', NAMESPACES).text if cell_elem.find('alignment:measure',
                                                                                                 NAMESPACES) is not None else None
                relation = cell_elem.find('alignment:relation', NAMESPACES).text if cell_elem.find('alignment:relation',
                                                                                                   NAMESPACES) is not None else None

                alignment_data.append({
                    'originalEntity': entity1,
                    'alignedEntity': entity2,
                    'measure': measure,
                    'relation': relation
                })

        table_rows = ""
        for row in alignment_data:
            table_rows += f"""
                    <tr>
                        <td>{row['originalEntity']}</td>
                        <td>{row['alignedEntity']}</td>
                        <td>{row['measure']}</td>
                        <td>{row['relation']}</td>
                    </tr>
                    """

        html_template = f"""
            <html>
            <body>
                <h1>Alignment Results</h1>
                <table>
                    <thead>
                        <tr>
                            <th>Entity 1</th>
                            <th>Entity 2</th>
                            <th>Measure</th>
                            <th>Relation</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>
            </body>
            </html>
            """

        return html_template

    except ET.ParseError as e:
        print(f"The provided file is not XML: {e}")
        return []
    except Exception as e:
        print(f"Error occurred: {e}")
        return []


def convert_results_to_jsonld(align_data):
    try:
        graph = rdflib.Graph()

        graph.parse(align_data, format="xml")

        jsonld_data = graph.serialize(format='json-ld', indent=4)

        jsonld_dict = json.loads(jsonld_data)

        return jsonld_dict

    except Exception as e:
        print(f"Error occurred while converting to JSON-LD: {e}")
        return {}
