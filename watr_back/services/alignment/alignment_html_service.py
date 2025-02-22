from auxiliary.alignment_auxiliary.execute_alignment_query import execute_alignment_query
from auxiliary.alignment_auxiliary.generate_html_alignment import generate_html_alignment
from auxiliary.alignment_auxiliary.process_alignment_output import process_alignment_operation, \
    process_alignment_output, get_ontology_path


def alignment_html_service(target_ontology):
    output = execute_alignment_query()
    temp_file = process_alignment_output(output)
    ontology_path = get_ontology_path(target_ontology)
    output_file = process_alignment_operation(temp_file, ontology_path)
    output_html = generate_html_alignment(output_file.name, target_ontology)
    return output_html
