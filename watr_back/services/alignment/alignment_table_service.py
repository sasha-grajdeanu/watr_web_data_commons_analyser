import xml.etree.ElementTree as ET

NAMESPACES = {
            'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'alignment': 'http://knowledgeweb.semanticweb.org/heterogeneity/alignment'
        }

def get_alignment_table(align_data):
    try:
        tree = ET.parse(align_data)
        root = tree.getroot()

        alignment_data = []

        for map_elem in root.findall('.//alignment:map', NAMESPACES):
            for cell_elem in map_elem.findall('alignment:Cell', NAMESPACES):
                entity1 = cell_elem.find('alignment:entity1', NAMESPACES).attrib.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', None)
                entity2 = cell_elem.find('alignment:entity2', NAMESPACES).attrib.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', None)
                measure = cell_elem.find('alignment:measure', NAMESPACES).text if cell_elem.find('alignment:measure', NAMESPACES) is not None else None
                relation = cell_elem.find('alignment:relation', NAMESPACES).text if cell_elem.find('alignment:relation', NAMESPACES) is not None else None

                alignment_data.append({
                    'originalEntity': entity1,
                    'alignedEntity': entity2,
                    'measure': measure,
                    'relation': relation
                })

        return alignment_data
    except ET.ParseError as e:
        print(f"The provided file is not XML: {e}")
        return []
    except Exception as e:
        print(f"Error occurred: {e}")
        return []
