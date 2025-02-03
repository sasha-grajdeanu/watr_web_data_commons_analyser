def generate_json_ld_compare(init_result, class_one, class_two):

    json_ld = {
        "@context": {
            "@vocab": "http://schema.org/",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            class_one: f"http://schema.org/{class_one}",
            class_two: f"http://schema.org/{class_two}",
            f"{class_one}_count": {
                "@id": f"{class_one}:count",
                "@type": "http://www.w3.org/2001/XMLSchema#integer"
            },
            f"{class_two}_count": {
                "@id": f"{class_two}:count",
                "@type": "http://www.w3.org/2001/XMLSchema#integer"
            }
        },
        '@type': 'Compare_results',
        "@graph": []
    }
    for row in init_result:
        node = {
            f"{class_one}_count": row["class_one_count"]["value"],
            f"{class_two}_count": row["class_two_count"]["value"],
            "property": row["property"]["value"],
        }
        json_ld["@graph"].append(node)
    return json_ld
