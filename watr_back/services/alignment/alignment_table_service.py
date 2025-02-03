from auxiliary.alignment_auxiliary.execute_alignment_query import execute_alignment_query
from auxiliary.alignment_auxiliary.parse_xml_file import parse_xml_file
from auxiliary.alignment_auxiliary.process_alignment_output import process_alignment_output, \
    process_alignment_operation, get_ontology_path


def alignment_table_service(target_ontology):
    output = execute_alignment_query()
    temp_file = process_alignment_output(output)
    ontology_path = get_ontology_path(target_ontology)
    output_file = process_alignment_operation(temp_file, ontology_path)

    return parse_xml_file(output_file)
