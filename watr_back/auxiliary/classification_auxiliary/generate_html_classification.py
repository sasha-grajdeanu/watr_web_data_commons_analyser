from flask import render_template_string


def generate_html_classification(results):

    html_template = """
        <!DOCTYPE html>
            <html lang="en">
            <head>
                <title>Classification Results</title>
            </head>
            <body>
                <h2>Classification Results</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Initial Subject</th>
                            <th>Initial Predicate</th>
                            <th>Blank Node</th>
                            <th>Level 1 Predicate</th>
                            <th>Level 1 Object</th>
                            <th>Level 2 Predicate</th>
                            <th>Level 2 Object</th>
                            <th>Level 3 Predicate</th>
                            <th>Level 3 Object</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for row in data %}
                        <tr>
                            <td>{{ row['iSubject'] }}</td>
                            <td>{{ row['iPredicate'] }}</td>
                            <td>{{ row['bNode'] }}</td>
                            <td>{{ row['l1Predicate'] }}</td>
                            <td>{{ row['l1Object'] }}</td>
                            <td>{{ row['l2Predicate'] }}</td>
                            <td>{{ row['l2Object'] }}</td>
                            <td>{{ row['l3Predicate'] }}</td>
                            <td>{{ row['l3Object'] }}</td>
                        </tr>
                        {% endfor %}
                    <tbody>
                </table>
            </body>
        </html>
    """

    data = [
        {
            "iSubject": row.get("initial_subject", {}).get("value", ""),
            "iPredicate": row.get("initial_predicate", {}).get("value", ""),
            "bNode": row.get("blankNode", {}).get("value", ""),
            "l1Predicate": row.get("level1_predicate", {}).get("value", ""),
            "l1Object": row.get("level1_object", {}).get("value", ""),
            "l2Predicate": row.get("level2_predicate", {}).get("value", ""),
            "l2Object": row.get("level2_object", {}).get("value", ""),
            "l3Predicate": row.get("level3_predicate", {}).get("value", ""),
            "l3Object": row.get("level3_object", {}).get("value", ""),
        }
        for row in results
    ]

    return render_template_string(html_template, data=data)
