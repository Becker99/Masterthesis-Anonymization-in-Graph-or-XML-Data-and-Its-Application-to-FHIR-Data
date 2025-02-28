import networkx as nx


def calculate_degree_distribution(graph):
    """
    Calculates the degree distribution based on patient nodes.

    Args:
        graph (nx.Graph): The Graph.

    Returns:
        dict: A dictionary with degree as key and frequency as value.
    """
    degree_counts = {}
    patient_nodes = [node for node, data in graph.nodes(data=True) if data.get("resourceType") == "Patient"]

    for node in patient_nodes:
        degree = graph.degree(node)
        if degree not in degree_counts:
            degree_counts[degree] = 0
        degree_counts[degree] += 1  # Count the frequency of each degree

    return degree_counts

def calculate_degree_centrality(graph):
    """
    Calculates the degree centrality based only on patient nodes.

    Args:
        graph (nx.Graph): The undirected graph.

    Returns:
        dict: A dictionary with patient nodes as keys and their degree centrality as values.
    """
    # Filter patient nodes
    patient_nodes = [node for node, data in graph.nodes(data=True) if data.get("resourceType") == "Patient"]
    num_patient_nodes = len(patient_nodes)


    if num_patient_nodes <= 1:
        print("Degree centrality cannot be computed. Not enough patient nodes.")
        return {}

    # Calculate degree centrality
    centrality = {}
    for node in patient_nodes:
        degree = graph.degree(node)  # degree of node
        centrality[node] = degree / (num_patient_nodes - 1)

    return centrality


def calculate_clustering_coefficient(graph):
    """
    Calculates the average clustering coefficient based only on the patient nodes.

    Args:
        graph (nx.Graph): The undirected graph.

    Returns:
        float: The average clustering coefficient based only on patient nodes.
    """
    # Filter the patient nodes
    patient_nodes = [node for node, data in graph.nodes(data=True) if data.get("resourceType") == "Patient"]

    if not patient_nodes:
        print("No patient nodes found. Clustering coefficient cannot be calculated.")
        return 0.0

    # Calculate the clustering coefficient for patient nodes only
    clustering_values = [nx.clustering(graph, node) for node in patient_nodes]

    # Calculate average value
    return sum(clustering_values) / len(clustering_values)




# Function to calculate the Graph Distortion Index
def calculate_graph_distortion_index(original_graph, anonymized_graph):
    """
    Calculates the graph distortion index between the original and anonymized graphs.

    Args:
        original_graph (nx.Graph): The original graph.
        anonymized_graph (nx.Graph): The anonymized graph.

    Returns:
        float: The graph distortion index, based on the number of added/removed edges.
    """
    original_edges = set(original_graph.edges())
    anonymized_edges = set(anonymized_graph.edges())

    added_edges = anonymized_edges - original_edges
    removed_edges = original_edges - anonymized_edges

    if len(original_edges) == 0:
        print("No edges in the original graph. Distortion index is not defined.")
        return 0.0

    distortion_index = (len(added_edges) + len(removed_edges)) / len(original_edges)
    return distortion_index
