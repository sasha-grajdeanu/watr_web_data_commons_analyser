from flask import abort

from auxiliary.alignment_auxiliary.parse_xml_file import parse_xml_file


def generate_json_ld_alignment(result_path, target_ontology):

    try:
        alignment_data = parse_xml_file(result_path)

        jsonld = {
            "@context": {
                "schema": "http://schema.org/",
                "alignment": "http://knowledgeweb.semanticweb.org/heterogeneity/alignment#",
                "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                "xsd": "http://www.w3.org/2001/XMLSchema#"
            },
            "@type": "alignment:Alignment",
            "@graph": []
        }

        for entry in alignment_data:
            alignment_entry = {
                "@type": "alignment:Cell",
                "WATROntologySubj": {
                    "@value": entry['originalEntity']
                },
                f"{target_ontology}OntologySubj": {
                    "@value": entry['alignedEntity']
                },
                "measure": {
                    "@value": entry['measure'],
                    "@type": "xsd:float"
                },
                "relation": {
                    "@value": entry['relation']
                }
            }
            jsonld["@graph"].append(alignment_entry)

        return jsonld
    except Exception as e:
        abort(500, description=f"Error occurred while converting to JSON-LD: {str(e)}")
