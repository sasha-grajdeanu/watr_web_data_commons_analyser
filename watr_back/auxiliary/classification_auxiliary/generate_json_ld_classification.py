def generate_json_ld_classification(init_result):

    jsonld = {
        "@context": "http://schema.org",
        "@type": "ClassificationResults",
        "@graph": []
    }

    for row in init_result:
        result_entry = {
            "initialSubject": {
                "@id": row['initial_subject']['value'],
                "@type": "uri"
            },
            "initialPredicate": {
                "@id": row['initial_predicate']['value'],
                "@type": "uri"
            },
            "blankNode": {
                "@id": row['blankNode']['value'],
                "@type": row['blankNode']['type'] if row['blankNode']['type'] == 'literal' else "uri"
            },
            "level1Predicate": {
                "@id": row.get('level1_predicate', {}).get('value', ''),
                "@type": "uri"
            },
            "level1Object": {
                "@value": row.get('level1_object', {}).get('value', ''),
                "@type": row.get('level1_object', {}).get('type', 'uri') if row.get('level1_object') else 'uri'
            },

            "level2Predicate": {
                "@id": row.get('level2_predicate', {}).get('value', ''),
                "@type": "uri"
            },
            "level2Object": {
                "@value": row.get('level2_object', {}).get('value', ''),
                "@type": row.get('level2_object', {}).get('type', 'uri') if row.get('level2_object') else 'uri'
            },
            "level3Predicate": {
                "@id": row.get('level3_predicate', {}).get('value', ''),
                "@type": "uri"
            },
            "level3Object": {
                "@value": row.get('level3_object', {}).get('value', ''),
                "@type": row.get('level3_object', {}).get('type', 'uri') if row.get('level3_object') else 'uri'
            }
        }
        jsonld["@graph"].append(result_entry)

    return jsonld
