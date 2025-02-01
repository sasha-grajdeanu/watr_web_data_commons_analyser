def create_graph_base(init_result):
    edges = set()
    for entries in init_result:
        entity = entries.get('entity')
        property = entries.get('property')
        value = entries.get('value')

        edges.add((entity, property, value))

        if entries.get("bnodeProperty") is not None:
            bnodeProperty = entries['bnodeProperty']
            bnodeValue = entries['bnodeValue']
            edges.add((value, bnodeProperty, bnodeValue))
    return edges
