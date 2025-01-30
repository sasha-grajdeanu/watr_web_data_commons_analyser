from flask import render_template_string


def generate_html_compare(init_result, class_one, class_two):
    html_template = """
            <!DOCTYPE html>
            <html lang="en">
            <head>

                <title>Comparison Results</title>
            </head>
            <body>
                <h2>Comparison Results: {{ class_one }} vs {{ class_two }}</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Property</th>
                            <th>{{ class_one }} Count</th>
                            <th>{{ class_two }} Count</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for row in data %}
                        <tr>
                            <td>{{ row['property'] }}</td>
                            <td>{{ row['class_one_count'] }}</td>
                            <td>{{ row['class_two_count'] }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </body>
            </html>
            """

    data = [
        {
            "property": row["property"]["value"],
            "class_one_count": row["class_one_count"]["value"],
            "class_two_count": row["class_two_count"]["value"]
        }
        for row in init_result
    ]

    return render_template_string(html_template, class_one=class_one, class_two=class_two, data=data)