import xml.etree.ElementTree as ET

from flask import abort

NAMESPACES = {
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'alignment': 'http://knowledgeweb.semanticweb.org/heterogeneity/alignment'
}


def parse_xml_file(result_path):

    try:
        tree = ET.parse(result_path)
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
    except ET.ParseError as e:
        abort(500, f"The provided file is not XML: {e}")
    except Exception as e:
        abort(500, f"Error occurred: {e}")

    return alignment_data
