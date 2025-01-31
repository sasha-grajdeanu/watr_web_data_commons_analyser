from auxiliary.alignment_auxiliary.execute_alignment_query import execute_alignment_query
from auxiliary.alignment_auxiliary.generate_json_ld_alignment import generate_json_ld_alignment
from auxiliary.alignment_auxiliary.process_alignment_output import process_alignment_output, get_path, \
    process_alignment_operation


def alignment_stats_service(target_ontology):
    """
    Function that processes alignment statistics.
    """
    output = execute_alignment_query()
    temp_file = process_alignment_output(output)
    ontology_path = get_path(target_ontology)
    output_file = process_alignment_operation(temp_file, ontology_path)
    jsonld_response = generate_json_ld_alignment(output_file, target_ontology)

    alignment_data = jsonld_response["@graph"]

    total_cells = 0
    total_measure = 0.0

    for cell in alignment_data:
        total_cells += 1

        measure_value = float(cell["measure"]["@value"])
        total_measure += measure_value

    average_measure = total_measure / total_cells if total_cells > 0 else 0.0

    return average_measure
