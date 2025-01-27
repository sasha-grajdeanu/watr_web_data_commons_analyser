
from rdflib import URIRef, Literal, Graph, RDF

DCUBE = URIRef("http://purl.org/statistics/ontology#")
EX = URIRef("http://example.org/watr/")
ALIGNMENT = URIRef("http://example.org/ontology/alignment/")

def get_alignment_stats(align_file):
    try:
        with open(align_file, 'r', encoding='utf-8') as file:
            content = file.read()

        # Remove the XML declaration if present
        if content.startswith("<?xml"):
            content = content.split("?>", 1)[1].strip()

            # Load the alignment results from the file
        graph = Graph()
        graph.parse(data=content, format='xml')

        # Initialize statistics counters
        total_alignments = 0
        aligned_subjects = set()
        aligned_predicates = set()
        aligned_objects = set()

        # Iterate through the triples in the graph
        for subject, predicate, obj in graph:
            total_alignments += 1
            aligned_subjects.add(str(subject))
            aligned_predicates.add(str(predicate))
            aligned_objects.add(str(obj))

        # Return the statistics in a structured format
        stats = {
            "total_alignments": total_alignments,
            "unique_subjects": len(aligned_subjects),
            "unique_predicates": len(aligned_predicates),
            "unique_objects": len(aligned_objects),
        }

        # Optional: Return the alignment results as a simplified JSON
        alignment_data = simplify_alignment_graph(graph)

        return {
            "alignment_data": alignment_data,
            "stats": stats
        }, 200

    except Exception as e:
        return {"error": f"An error occurred: {e}"}, 500


def simplify_alignment_graph(graph):
    alignment_data = []
    for subject, predicate, obj in graph:
        alignment_data.append({
            "subject": str(subject),
            "predicate": str(predicate),
            "object": str(obj),
        })
    return alignment_data