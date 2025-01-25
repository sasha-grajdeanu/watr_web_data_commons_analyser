import subprocess
import tempfile

from SPARQLWrapper import SPARQLWrapper, TURTLE

from watr_back.sparql_queries.alignment_queries import ALIGNMENT_QUERY

sparql = SPARQLWrapper("http://localhost:3030/watr-dataset/sparql")

def align(target_ontology):
    sparql_query = ALIGNMENT_QUERY
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(TURTLE)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".nt")
    output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".nt")

    try:
        results = sparql.query().convert()
        with open(temp_file.name, "wb") as f:
            f.write(results)
    except Exception as e:
        print(f"Error: {e}")

    ontology_path = get_path(target_ontology)

    try:
        # comanda AML pentru aliniere
        aml_command = [
            "java", "-jar", "C:\\AML_v3.2\\AgreementMakerLight.jar",
            "-s", temp_file.name,
            "-t", ontology_path,
            "-o", output_file.name,
            "-a"
        ]

        subprocess.run(aml_command, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error during AML execution: {e}")
        return None

    return output_file.name


def get_path(target_ontology):
    if target_ontology == "schema.org":
        return './ontologies/schemaorg.rdf'
    elif target_ontology == "DBPedia":
        return './ontologies/dbpedia.nt'


