from auxiliary.alignment_auxiliary.execute_alignment_query import execute_alignment_query
from auxiliary.alignment_auxiliary.process_alignment_output import process_alignment_output, \
    process_alignment_operation, get_path


def align(target_ontology):
    output = execute_alignment_query()
    temp_file = process_alignment_output(output)
    ontology_path = get_path(target_ontology)
    output_file = process_alignment_operation(temp_file, ontology_path)

    return output_file.name
