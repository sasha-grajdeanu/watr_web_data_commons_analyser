from flask import Response

from auxiliary.visualise_auxiliary.execute_visualise_query import execute_sparql_query
from auxiliary.visualise_auxiliary.process_sparql_results import process_sparql_results


def visualise_html_service(rdf_class, limit, count_limit):
    """
    Returns the SPARQL query results as an HTML table.
    """
    try:
        output = execute_sparql_query(rdf_class, limit, count_limit)
        # init_result = process_sparql_results(output)

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
        for row in init_result:
            html_content += f"""
            <tr>
                <td>{row['entity']}</td>
                <td>{row['property']}</td>
                <td>{row['value']}</td>
                <td>{row.get('bnodeProperty', '')}</td>
                <td>{row.get('bnodeValue', '')}</td>
            </tr>
            """
        html_content += """
                </tbody>
            </table>
        </body>
        </html>
        """
        return Response(html_content, content_type="text/html")

    except Exception as e:
        return Response(f"<h1>Error</h1><p>An error occurred: {e}</p>", content_type="text/html"), 500