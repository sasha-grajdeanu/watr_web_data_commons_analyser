COMPARATION_QUERY = """
PREFIX schema: <http://schema.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT ?property (COUNT(DISTINCT ?class_one) AS ?class_one_count) (COUNT(DISTINCT ?class_two) AS ?class_two_count)
WHERE {{
  GRAPH ?g {{
    {{ ?class_one a schema:{class_one} ; ?property [] }}
    UNION
    {{ ?class_two a schema:{class_two} ; ?property [] }}
  }}
}}
GROUP BY ?property
"""