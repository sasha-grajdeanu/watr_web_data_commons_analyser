import os
import tempfile

import networkx as nx


def write_graph_format(init_graph):
    graph = nx.DiGraph()
    for edge in init_graph:
        graph.add_edge(edge[0], edge[2], label=edge[1])
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".graphml")
    try:
        nx.write_graphml(graph, temp_file.name)
    except Exception as e:
        temp_file.close()
        os.unlink(temp_file.name)
        raise e
    return temp_file.name
