from auxiliary.alignment_auxiliary.execute_alignment_query import execute_alignment_query
from auxiliary.alignment_auxiliary.generate_html_alignment import generate_html_alignment
from auxiliary.alignment_auxiliary.process_alignment_output import get_path, process_alignment_operation, \
    process_alignment_output


def alignment_html_service(target_ontology):
    """
    Service function that aligns the ontology to a chosen ontology and
    returns the HTML file
    """
    output = execute_alignment_query()
    temp_file = process_alignment_output(output)
    ontology_path = get_path(target_ontology)
    output_file = process_alignment_operation(temp_file, ontology_path)
    output_html = generate_html_alignment(output_file.name, target_ontology)
    return output_html
