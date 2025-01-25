from SPARQLWrapper import SPARQLWrapper, JSON
from flask import Response
from sparql_queries.visualise_queries import VISUALISE_QUERY
from enviromment.enviromment import SPARQL_ENDPOINT

sparql = SPARQLWrapper(SPARQL_ENDPOINT)


def visualise_html_service(rdf_class, limit, count_limit):
    print(rdf_class)
    print(limit)
    print(count_limit)
    if limit:
        sparql_query = VISUALISE_QUERY.format(rdf_class=rdf_class) + f" LIMIT {count_limit}"
    else:
        sparql_query = VISUALISE_QUERY.format(rdf_class=rdf_class)
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)

    try:
        output = sparql.query().convert()

        # Start building the HTML content
        html_content = """
        <html lang="en">
        <body>
            <h1>SPARQL Query Results</h1>
            <table>
                <thead>
                    <tr>
                        <th>Entity</th>
                        <th>Property</th>
                        <th>Value</th>
                        <th>BNode Property</th>
                        <th>BNode Value</th>
                    </tr>
                </thead>
                <tbody>
        """

        # Populate the HTML table with query results
        for elements in output['results']['bindings']:
            entity = elements.get('entity', {}).get('value', '')
            property = elements.get('property', {}).get('value', '')
            value = elements.get('value', {}).get('value', '')
            bnode_property = elements.get('bnodeProperty', {}).get('value', '') if "bnodeProperty" in elements else ''
            bnode_value = elements.get('bnodeValue', {}).get('value', '') if "bnodeValue" in elements else ''

            html_content += f"""
            <tr>
                <td>{entity}</td>
                <td>{property}</td>
                <td>{value}</td>
                <td>{bnode_property}</td>
                <td>{bnode_value}</td>
            </tr>
            """

        # Close the HTML content
        html_content += """
                </tbody>
            </table>
        </body>
        </html>
        """

        # Return the HTML content as a response
        return Response(html_content, content_type="text/html")

    except Exception as e:
        return Response(f"<h1>Error</h1><p>An error occurred: {e}</p>", content_type="text/html"), 500