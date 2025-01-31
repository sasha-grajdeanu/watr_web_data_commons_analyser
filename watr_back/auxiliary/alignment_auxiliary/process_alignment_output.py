import os
import subprocess
import tempfile

from flask import abort


def process_alignment_output(output):
    """
    Helper function to process SPARQL results for classification
    and saves it in a temporary file.
    """
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.ttl')
    try:
        with open(temp_file.name, "wb") as file:
            file.write(output)
    except Exception as e:
        abort(500, f"Unable to write file: {e}")

    return temp_file


def process_alignment_operation(my_file, target_ontology_path):
    """
    Function that does the alignment operation
    """
    target_temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".xml")

    try:
        # comanda AML pentru aliniere
        aml_command = [
            "java", "-jar", os.getenv("AML_PATH"),
            "-s", my_file.name,
            "-t", target_ontology_path,
            "-o", target_temp_file.name,
            "-a"
        ]
        subprocess.run(aml_command, check=True)
    except subprocess.CalledProcessError as e:
        abort(500, f"Error during AML execution: {e}")

    return target_temp_file


def get_path(target_ontology):
    """
    Get the path to our target ontology
    """
    if target_ontology == "schema.org":
        return './ontologies/schemaorg.rdf'
    elif target_ontology == "DBPedia":
        return './ontologies/dbpedia.nt'
