from auxiliary.alignment_auxiliary.parse_xml_file import parse_xml_file


def generate_html_alignment(result_path, target_ontology):
    """
    Function that creates the HTML response for classification
    """
    alignment_data = parse_xml_file(result_path)
    table_rows = ""
    for row in alignment_data:
        table_rows += f"""
                <tr>
                    <td>{row['originalEntity']}</td>
                    <td>{row['alignedEntity']}</td>
                    <td>{row['measure']}</td>
                    <td>{row['relation']}</td>
                </tr>
                """
    html_template = f"""
        <!DOCTYPE html>
            <html lang="en">
            <head>
                <title>Alignment Results</title>
            </head>
            <body>
                <h2>Alignment Results</h2>
                <table>
                    <thead>
                        <tr>
                            <th>WATR Ontology Subject</th>
                            <th>{target_ontology} Ontology Subject</th>
                            <th>Measure</th>
                            <th>Relation</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>
            </body>
            </html>
    """

    return html_template
