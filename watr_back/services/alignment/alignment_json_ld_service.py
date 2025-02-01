from flask import abort

from auxiliary.alignment_auxiliary.execute_alignment_query import execute_alignment_query
from auxiliary.alignment_auxiliary.generate_json_ld_alignment import generate_json_ld_alignment
from auxiliary.alignment_auxiliary.process_alignment_output import process_alignment_output, \
    process_alignment_operation, get_ontology_path


def alignment_json_ld_service(target_ontology):
    """
    Service function that returns JSON-LD response of the alignment
    """
    try:
        output = execute_alignment_query()
        temp_file = process_alignment_output(output)
        ontology_path = get_ontology_path(target_ontology)
        output_file = process_alignment_operation(temp_file, ontology_path)
        return generate_json_ld_alignment(output_file, target_ontology)
    except Exception as e:
        return abort(500, description=f"An error occurred: {e}")
