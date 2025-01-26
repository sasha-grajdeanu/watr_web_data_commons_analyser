from collections import defaultdict

from auxiliary.visualise_auxiliary.execute_visualise_query import execute_sparql_query


def compute_statistics(query_results):
    """
    Compute statistics from the query results.
    """
    # Initialize data structures
    unique_entities = set()
    entity_types = defaultdict(int)  # To count URI, bnode, or literal types for entities
    property_frequency = defaultdict(int)  # To count frequency of properties
    value_types = defaultdict(int)  # To count URI, bnode, or literal types for values

    # Iterate through the query results
    for result in query_results['results']['bindings']:
        # Extract entity, property, and value
        entity = result['entity']['value']
        property_uri = result['property']['value']
        value = result['value']['value']

        # Count unique entities
        unique_entities.add(entity)

        # Determine the type of the entity (URI, bnode, or literal)
        if result['entity']['type'] == 'uri':
            entity_types['uri'] += 1
        elif result['entity']['type'] == 'bnode':
            entity_types['bnode'] += 1
        else:
            entity_types['literal'] += 1

        # Count property frequency
        property_frequency[property_uri] += 1

        # Determine the type of the value (URI, bnode, or literal)
        if result['value']['type'] == 'uri':
            value_types['uri'] += 1
        elif result['value']['type'] == 'bnode':
            value_types['bnode'] += 1
        else:
            value_types['literal'] += 1

    # Prepare the statistics
    statistics = {
        'unique_entities': len(unique_entities),
        'entity_types': dict(entity_types),
        'property_frequency': dict(property_frequency),
        'value_types': dict(value_types),
    }

    return statistics

def return_statistics(rdf_class, limit, count_limit):
    init_result = execute_sparql_query(rdf_class, limit, count_limit)
    res = compute_statistics(init_result)
    print(res)
    return res