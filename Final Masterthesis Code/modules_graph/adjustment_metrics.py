import numpy as np

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

project_dir = os.path.abspath(os.path.join(BASE_DIR, ".."))
sys.path.append(project_dir)
os.chdir(project_dir)

from graph_metrics import (
    calculate_degree_distribution,
    calculate_clustering_coefficient,
    calculate_degree_centrality,
)


import uuid
from dummy_generator import create_dummy_node_xml
from numpy.random import choice


from config.graph_config import graph_config

from config.graph_metric_config import GRAPH_METRIC_CONFIG

from modules_graph.graph_metrics import calculate_degree_distribution, calculate_degree_centrality, calculate_clustering_coefficient

from lxml.etree import fromstring, tostring, SubElement




def decide_dummy_node_connection(graph, target_node_id):
    """
    Decides which resource type is selected for a dummy node,
    based on the connections in graph_config.

    Args:
        graph (nx.Graph): The existing graph.
        target_node_id (str): ID of the target node to which the dummy node is added.

    Returns:
        tuple: (dummy resource type, target node ID) or None if no connection is possible.
    """
    if not graph.has_node(target_node_id):
        print(f"Target node {target_node_id} does not exist. Skip.")
        return None

    # Determine the resource type of the target node
    target_node_data = graph.nodes[target_node_id]
    target_node_type = target_node_data.get("resourceType")

    if not target_node_type:
        print(f"Target node {target_node_id} has no 'resourceType'.")
        return None

    # Find possible connections for this resource type
    possible_resource_types = set()

    if target_node_type in graph_config:
        possible_resource_types.update(graph_config[target_node_type].keys())

    # Also search for reverse connections
    for resource_type, connections in graph_config.items():
        if target_node_type in connections:
            possible_resource_types.add(resource_type)

    # If no valid connections are available
    if not possible_resource_types:
        print(f"No valid connections for resource type {target_node_type} in graph_config.")
        return None

    # Select a permitted resource type
    for resource_type in possible_resource_types:
        if (
            (target_node_type in graph_config and resource_type in graph_config[target_node_type])
            or (resource_type in graph_config and target_node_type in graph_config[resource_type])
        ):
            print(f"Valid connection found: {resource_type} -> {target_node_type}")
            return resource_type, target_node_id

    print(f"No permitted connection for resource type {target_node_type} found.")
    return None

def add_reference_tag(graph, node1_id, node2_id):
    """
    Adds a reference tag to the node based on `graph_config`.
    The key in `graph_config` always determines where the reference tag is saved.

    Args:
        graph (nx.Graph): The graph with the nodes and resources.
        node1_id (str): ID of the first node.
        node2_id (str): ID of the second node.
    """
    # Check whether both nodes exist
    if not graph.has_node(node1_id) or not graph.has_node(node2_id):
        print(f"Error: At least one node does not exist - node1={node1_id}, node2={node2_id}")
        return

    # Determine resource types
    node1_type = graph.nodes[node1_id].get("resourceType")
    node2_type = graph.nodes[node2_id].get("resourceType")

    if not node1_type or not node2_type:
        print(f"Error: A node has no 'resourceType' - node1={node1_type}, node2={node2_type}")
        return

    # Check whether node1 is the key in `graph_config` (i.e. the reference goes to node1)
    if node1_type in graph_config and node2_type in graph_config[node1_type]:
        target_node_id, source_node_id = node1_id, node2_id
    elif node2_type in graph_config and node1_type in graph_config[node2_type]:
        print(f"direction in `graph_config` prohibits saving in {node2_type}. "
              f"Storage only in {node1_type} possible.")
        return
    else:
        print(f"No valid relationship found in `graph_config`: {node1_type} <-> {node2_type}.")
        return

    # Get XML data of the target node
    reference_text = f"{graph.nodes[source_node_id]['resourceType']}/{source_node_id}"
    reference_tag = graph.nodes.get(target_node_id, {}).get("full_record")

    if not reference_tag:
        print(f"Error: Node {target_node_id} has no `full_record`-XML-data.")
        return

    try:
        # Parse XML structure
        root = fromstring(reference_tag)

        # Check whether the reference already exists
        existing_references = [ref.text for ref in root.findall(".//reference")]
        if reference_text in existing_references:
            print(f"Reference {reference_text} already exists in {target_node_id}.")
            return

        # Add new reference tag
        new_reference_tag = SubElement(root, "reference")
        new_reference_tag.text = reference_text

        # Save updated XML structure
        graph.nodes[target_node_id]["full_record"] = tostring(root, encoding="unicode", method="xml")
        print(f"Reference added: {reference_text} in target resource {graph.nodes[target_node_id]['resourceType']}.")

    except Exception as e:
        print(f"Error when adding the reference tag to {target_node_id}: {e}")



def add_dummy_nodes(graph, xml_root, target_node_id, num_dummy_nodes):
    if not graph.has_node(target_node_id):
        print(f"target node {target_node_id} does not exist. Skip.")
        return

    target_resource_type = graph.nodes[target_node_id]["resourceType"]
    possible_resource_types = set()

    if target_resource_type in graph_config:
        possible_resource_types.update(graph_config[target_resource_type].keys())

    for resource_type, connections in graph_config.items():
        if target_resource_type in connections:
            possible_resource_types.add(resource_type)

    possible_resource_types.discard("Patient")

    if not possible_resource_types:
        print(f"No valid connections for resource type {target_resource_type}.")
        return

    for _ in range(num_dummy_nodes):
        dummy_resource_type = np.random.choice(list(possible_resource_types))
        dummy_node_id = str(uuid.uuid4())
        dummy_node_xml = create_dummy_node_xml(
            resource_type=dummy_resource_type,
            dummy_node_id=dummy_node_id,
        )

        graph.add_node(dummy_node_id, resourceType=dummy_resource_type, full_record=dummy_node_xml)
        if is_valid_connection(graph, dummy_node_id, target_node_id):
            graph.add_edge(dummy_node_id, target_node_id)
            add_reference_tag(graph, dummy_node_id, target_node_id)
            print(f"Dummy node added: ID={dummy_node_id}, Type={dummy_resource_type}, Target node: {target_node_id}")
            return dummy_node_id  
        else:
            print(f"Invalid connection between {dummy_resource_type} and {target_resource_type}. Dummy node is removed.")
            graph.remove_node(dummy_node_id)

    return None




def is_valid_connection(graph, source, target):
    """
    Checks whether a connection between two nodes based on graph_config is permitted.
    Measures the execution time for the check.

    Args:
        graph (nx.Graph): The graph.
        source (str): ID of the source node.
        target (str): ID of the target node.

    Returns:
        bool: True, if the connection is allowed, otherwise False.
    """


    source_type = graph.nodes[source]["resourceType"]
    target_type = graph.nodes[target]["resourceType"]

    
    valid = (
        (source_type in graph_config and target_type in graph_config[source_type]) or
        (target_type in graph_config and source_type in graph_config[target_type])
    )



    return valid






def add_edge_to_xml(xml_root, source_type, target_type, target_id):
    """
    Adds a new edge (reference tag) to an XML structure.

    Args:
        xml_root (element): Root of the XML structure in which the edge is added.
        source_type (str): Type of source (e.g. “AllergyIntolerance”).
        target_type (str): Type of target (e.g. "Patient").
        target_id (str): ID of the target node.

    Returns:
        bool: True if the edge was successfully added, otherwise False.
    """
    # Check whether the connection is allowed in the graph_config
    if source_type not in graph_config or target_type not in graph_config[source_type]:
        print(f"Connection between {source_type} and {target_type} not allowed.")
        return False

    # Search for an existing reference tag
    existing_reference = xml_root.find(".//reference")
    if existing_reference is not None:
        # If a reference tag exists, find the parent element
        parent_element = existing_reference.getparent()
        if parent_element is None:
            parent_element = xml_root
        # Add a new reference tag
        new_reference = SubElement(parent_element, "reference")
        new_reference.text = f"{target_type}/{target_id}"
        print(f"Edge between {source_type} and {target_type} ({target_id}) added (to existing tag).")
    else:
        # If no reference tag exists, add a new reference tag directly to the root
        new_reference = SubElement(xml_root, "reference")
        new_reference.text = f"{target_type}/{target_id}"
        print(f"Edge between {source_type} and {target_type} ({target_id}) added (new tag created).")

    return True




def remove_edge_from_xml(xml_root, target_type, target_id):
    """
    Removes an edge (reference tag) from an XML structure.

    Args:
        xml_root (element): Root of the XML structure from which the edge is removed.
        target_type (str): Type of the target node (e.g. “patient”).
        target_id (str): ID of the target node.

    Returns:
        bool: True if the edge was successfully removed, otherwise False.
    """
    # Search all reference tags in the XML structure
    for reference_element in xml_root.findall(".//reference"):
        if reference_element.text == f"{target_type}/{target_id}":
            # Get the parent element
            parent = reference_element.getparent() if hasattr(reference_element, 'getparent') else None
            if parent is not None:
                # Remove the reference tag from the parent element
                parent.remove(reference_element)
                print(f"Edge to {target_type} ({target_id}) removed.")
                return True
            else:
                print(f"Parent element for reference tag {target_type}/{target_id} not found.")
                return False

    print(f"Edge to {target_type} ({target_id}) not found.")
    return False


def remove_nodes(graph, xml_root, nodes_to_remove):
    nodes = list(graph.nodes)
    removed_nodes = []

    for _ in range(nodes_to_remove):
        if not nodes:
            print("No further nodes available for removal.")
            break

        node_to_remove = choice(nodes)
        if graph.has_node(node_to_remove):
            graph.remove_node(node_to_remove)
            nodes.remove(node_to_remove)
            removed_nodes.append(node_to_remove)
            print(f"Node removed: {node_to_remove}")

            for element in xml_root.findall(".//record"):
                if element.findtext("id") == node_to_remove:
                    xml_root.remove(element)
                    break
        else:
            print(f"Node {node_to_remove} does not exist. Skip.")
    return removed_nodes



def calculate_graph_metrics(graph):
    """
    Calculates the metrics for the entire graph, with Degree Distribution 
    and Clustering Coefficient are calculated specifically for patient nodes.

    Args:
        graph (nx.Graph): The original graph.

    Returns:
        dict: A dictionary with the calculated metrics.
    """
    print("Calculate metrics for the entire graph...")

    # Calculation of the degree distribution specifically for patient nodes
    degree_distribution = calculate_degree_distribution(graph)
    average_degree = sum(degree * count for degree, count in degree_distribution.items()) / sum(degree_distribution.values()) if degree_distribution else 0

    # Clustering coefficient for patient nodes only
    clustering_coefficient = calculate_clustering_coefficient(graph)

    # Degree Centrality for patient nodes only
    degree_centrality = calculate_degree_centrality(graph)

    # Summarize metrics
    metrics = {
        "degree_distribution": average_degree,
        "clustering_coefficient": clustering_coefficient,
        "degree_centrality": sum(degree_centrality.values()) / len(degree_centrality) if degree_centrality else 0,
    }

    print("Graphmetrics calculated:")
    for metric, value in metrics.items():
        print(f"  {metric}: {value:.4f}" if value is not None else f"  {metric}: None")

    return metrics





def update_metric_config(noised_metrics):
    """
    Updates the `GRAPH_METRIC_CONFIG` based on the noisy target values.

    Args:
        noised_metrics (dict): Noisy target metrics.
    """
    for metric, target_value in noised_metrics.items():
        if metric in GRAPH_METRIC_CONFIG:
            tolerance = GRAPH_METRIC_CONFIG[metric]["tolerance"]
            GRAPH_METRIC_CONFIG[metric]["target_value"] = target_value
            GRAPH_METRIC_CONFIG[metric]["min_value"] = target_value - tolerance
            GRAPH_METRIC_CONFIG[metric]["max_value"] = target_value + tolerance
        else:
            print(f"Warning: Metric {metric} is not defined in GRAPH_METRIC_CONFIG.")


def select_metric_to_adjust(current_metrics, config):
    """
    Selects the metric that is furthest away from the target value, 
    taking into account the order between Degree Centrality and Degree Distribution.

    Args:
        current_metrics (dict): Current values of the metrics.
        config (dict): Configuration of the target metrics.

    Returns:
        str: The name of the metric to be customized.
    """
    max_deviation = -1
    selected_metric = None

    # Order of metrics for prioritization
    metric_priority = ["degree_centrality", "degree_distribution", "clustering_coefficient"]

    for metric in metric_priority:
        value = current_metrics.get(metric)
        if metric in config and value is not None:
            target = config[metric]["target_value"]
            min_value = config[metric]["min_value"]
            max_value = config[metric]["max_value"]

            # Calculate deviation from target range
            if value < min_value:
                deviation = min_value - value
            elif value > max_value:
                deviation = value - max_value
            else:
                deviation = 0 

            # Select the metric with the largest deviation
            if deviation > max_deviation:
                max_deviation = deviation
                selected_metric = metric

            # If a higher priority metric is outside the tolerance range, cancel
            if selected_metric == "degree_centrality" and deviation > 0:
                break

    return selected_metric


def calculate_average_degree(degree_distribution):
    total_degree = sum(degree * count for degree, count in degree_distribution.items())
    total_nodes = sum(degree_distribution.values())
    return total_degree / total_nodes if total_nodes > 0 else 0

def adjust_graph_to_target_metrics(graph, xml_root, epsilon, sensitivity):
    """
    Adjusts the graph iteratively to achieve the target metrics.

    Args:
        graph (nx.Graph): The graph to be anonymized.
        xml_root (xml.ElementTree.Element): The XML root of the graph.
        epsilon (float): Privacy parameter.
        sensitivity (float): Sensitivity of the metrics.

    Returns:
        nx.graph: The customized graph.
    """
    iteration = 0

    # Pre-calculation: Initial metrics
    initial_metrics = calculate_graph_metrics(graph)
    current_metrics = initial_metrics.copy()  # Current values start with the initial metrics
    
    print("\nInitiale Metriken vor der Anpassung:")
    for metric, value in initial_metrics.items():
        print(f"{metric}: {value:.4f}")


    while True:
        print(f"\n--- Iteration {iteration + 1} ---")

    
        # Select the metric that needs to be adjusted
        metric_to_adjust = select_metric_to_adjust(current_metrics, GRAPH_METRIC_CONFIG)
        if not metric_to_adjust:
            print("All metrics are within the target range. Adjustment completed.")
            break

        print(f"Adjust the metric {metric_to_adjust}...")

        # Adjustment based on the metric
        if metric_to_adjust == "degree_distribution":
            current_metrics["degree_distribution"] = adjust_degree_distribution(
                graph,
                xml_root,
                GRAPH_METRIC_CONFIG["degree_distribution"]["target_value"],
                current_metrics["degree_distribution"]
            )
        elif metric_to_adjust == "clustering_coefficient":
            current_metrics["clustering_coefficient"] = adjust_clustering_coefficient(
                graph,
                xml_root,
                GRAPH_METRIC_CONFIG["clustering_coefficient"]["target_value"],
                current_metrics["clustering_coefficient"]
            )
        elif metric_to_adjust == "degree_centrality":
            current_metrics["degree_centrality"] = adjust_degree_centrality(
                graph,
                xml_root,
                GRAPH_METRIC_CONFIG["degree_centrality"]["target_value"],
                current_metrics["degree_centrality"]
            )


        # Check whether all values are within the target range
        all_within_tolerance = all(
            abs(current_metrics[metric] - GRAPH_METRIC_CONFIG[metric]["target_value"]) <= GRAPH_METRIC_CONFIG[metric]["tolerance"]
            for metric in current_metrics
        )
        if all_within_tolerance:
            print("All metrics in target range. Adjustment completed.")
            break

        iteration += 1

    final_metrics = calculate_graph_metrics(graph)

    print("\nVergleich der Metriken (Initial vs. Final):")
    for metric in final_metrics.keys():
        print(f"{metric}: Initial = {initial_metrics[metric]:.4f} | Final = {final_metrics[metric]:.4f}")

    print(f"All metrics were recalculated and finally output.")
    
    return graph






def adjust_degree_distribution(graph, xml_root, target_value, current_value):
    """
    Adjusts the degree distribution by removing or adding edges at higher or lower degree nodes.
    removed or added. Contains fallback mechanisms for missing edges or nodes.

    Args:
        graph (nx.Graph): The graph.
        xml_root (xml.ElementTree.Element): The XML root of the graph.
        target_value (float): Target value.
        current_value (float): Current value.

    Returns:
        float: The updated value.
    """
    print(f"Adjustment of the degree distribution: Target value={target_value:.4f}, Current value={current_value:.4f}")

    # Identify patient nodes
    patient_nodes = [node for node, data in graph.nodes(data=True) if data.get("resourceType") == "Patient"]
    total_patient_nodes = len(patient_nodes)

    if total_patient_nodes == 0:
        print("No patient nodes found. Dummy nodes are added.")
        add_dummy_nodes(graph, xml_root, target_node_id=np.random.choice(list(graph.nodes)), num_dummy_nodes=1)
        return current_value
    

    def recalculate_metric():
        """
        Recalculates the degree distribution based on the current graph state.
        """
        degree_distribution = calculate_degree_distribution(graph)
        total_degree = sum(degree * count for degree, count in degree_distribution.items())
        total_nodes = sum(degree_distribution.values())
        avg_degree = total_degree / total_nodes if total_nodes > 0 else 0
        return avg_degree

    iteration = 0 

    while not (target_value - GRAPH_METRIC_CONFIG["degree_distribution"]["tolerance"]
               <= current_value
               <= target_value + GRAPH_METRIC_CONFIG["degree_distribution"]["tolerance"]):
        
        iteration += 1
        adjustments = 0

        # Calculate degree distribution for patient nodes
        current_value = recalculate_metric()
        degree_values = {node: graph.degree(node) for node in patient_nodes}
        avg_degree = sum(degree_values.values()) / len(degree_values)

        # Sort patient nodes only
        sorted_patient_nodes = sorted(patient_nodes, key=lambda node: degree_values[node])


        if current_value < target_value:  # Add edges (prioritize patients with a low degree)
            print(f"Add edges to increase degree distribution")
            # Select all patient nodes with degree < avg_degree
            low_degree_nodes = [node for node in sorted_patient_nodes if graph.degree(node) < avg_degree]
            # print(f"Number of patient nodes: {len(patient_nodes)}")
            # print(f"Average degree: {avg_degree}")
            # print(f"Low-Degree-Node (below the average): {len(low_degree_nodes)}")
            # print(f"List of low-degree nodes: {low_degree_nodes}") 

            #print(f"Low-Degree-Nodes: {low_degree_nodes}")

            max_batch_size = 20
            batch_factor = 0.2
            batch_size = min(max(1, int(batch_factor * len(low_degree_nodes))), max_batch_size)

            # Calculate weights based on difference to avg_degree
            node_weights = np.array([avg_degree - degree_values[node] for node in low_degree_nodes])
            node_weights = np.maximum(node_weights, 1e-6)
            node_weights /= node_weights.sum()
            #print(f"Node Weights (Added): {node_weights}")
            # Select ALL nodes with weighted probability
            selected_nodes = np.random.choice(low_degree_nodes, size=batch_size, replace=False, p=node_weights)
            
            print(f"Degree distribution of the selected nodes: {[degree_values[node] for node in selected_nodes]}")
            print(f"Selected {len(selected_nodes)} Nodes for new edges.")

            for node_to_connect in selected_nodes:
                target_candidates = [node for node in graph.nodes if graph.nodes[node].get("resourceType") != "Patient"]

                if not target_candidates:
                    print("No target candidates available. Dummy nodes are added.")
                    add_dummy_nodes(graph, xml_root, target_node_id=node_to_connect, num_dummy_nodes=1)
                    continue

                target_nodes = np.random.choice(target_candidates, size=min(batch_size, len(target_candidates)), replace=False)

                for target_node in target_nodes:
                    if is_valid_connection(graph, node_to_connect, target_node) and not graph.has_edge(node_to_connect, target_node):
                        graph.add_edge(node_to_connect, target_node)
                        # add_edge_to_xml(
                        #     xml_root,
                        #     source_type=graph.nodes[node_to_connect]["resourceType"],
                        #     target_type=graph.nodes[target_node]["resourceType"],
                        #     target_id=target_node
                        # )
                        adjustments += 1
                        print(f"Edge added: {node_to_connect} -> {target_node}")                          
                    if adjustments >= batch_size:
                        break
                if adjustments >= batch_size:
                    break


            current_value = recalculate_metric()
            print(f"Updated degree distribution by batch: {current_value:.4f}")

        elif current_value > target_value:  # Remove edges
            print(f"Remove edges to reduce degree distribution")
            high_degree_nodes =  [node for node in sorted_patient_nodes if graph.degree(node) >= avg_degree] 
            
            max_batch_size = 20
            batch_factor = 0.8
            batch_size = min(max(1, int(batch_factor * len(high_degree_nodes))), max_batch_size)

            # Calculate weighting
            node_weights = np.array([degree_values[node] - avg_degree for node in high_degree_nodes])
            node_weights = np.maximum(node_weights, 1e-6)  # Prevents division by 0
            node_weights /= node_weights.sum()
            #print(f"Node Weights (Added): {node_weights}")
                                                    
            # Weighted selection of nodes
            selected_nodes = np.random.choice(high_degree_nodes, size=batch_size, replace=False, p=node_weights)

            print(f"Degree distribution of the selected nodes: {[degree_values[node] for node in selected_nodes]}")
            print(f"Selected {len(selected_nodes)} Nodes for new edges.")

            for patient_node in selected_nodes:
                if graph.degree(patient_node) <= avg_degree:  
                    continue              
                

                neighbors = list(graph.neighbors(patient_node))
                target_nodes = []

                if neighbors:
                    target_nodes = np.random.choice(neighbors, size=min(batch_size, len(neighbors)), replace=False)

                    for target_node in target_nodes:
                        graph.remove_edge(patient_node, target_node)
                        adjustments += 1
                        print(f"Edge removed: {patient_node} -> {target_node}")
                        # remove_edge_from_xml(
                        #     xml_root,
                        #     target_type=graph.nodes[target_node]["resourceType"],
                        #     target_id=target_node
                        # )
                        if adjustments >= batch_size:
                            break
                    if adjustments >= batch_size:
                        break

        current_value = recalculate_metric()
        print(f"Updated degree distribution by batch: {current_value:.4f}")

        if adjustments == 0:
            print("No further adjustments possible.")
            break

    print(f"Target value for degree distribution reached: {current_value:.4f}")
    return current_value



def adjust_degree_centrality(graph, xml_root, target_value, current_value):
    """
    Adjusts the degree centrality specifically for patient nodes, with dynamic batch size.
    """
    print(f"Adjustment of degree centrality: target value={target_value:.4f}, Current value={current_value:.4f}")
    patient_nodes = [node for node, data in graph.nodes(data=True) if data.get("resourceType") == "Patient"]
    total_patient_nodes = len(patient_nodes)

    if total_patient_nodes == 0:
        print("No patient nodes found. Dummy nodes are added.")
        add_dummy_nodes(graph, xml_root, target_node_id=np.random.choice(list(graph.nodes)), num_dummy_nodes=1)
        return current_value

    def recalculate_metric():
        """
        Recalculates the degree centrality based on the current graph state.
        """
        centrality_values = calculate_degree_centrality(graph)
        return sum(centrality_values.values()) / len(centrality_values) if centrality_values else 0

    iteration = 0
    max_batch_size = 20

    while not (target_value - GRAPH_METRIC_CONFIG["degree_centrality"]["tolerance"]
               <= current_value
               <= target_value + GRAPH_METRIC_CONFIG["degree_centrality"]["tolerance"]):
        
        iteration += 1
        adjustments = 0

        current_value = recalculate_metric()
        # Recalculate degree centrality and sort nodes by value
        centrality_values = calculate_degree_centrality(graph)
        avg_centrality = sum(centrality_values.values()) / len(centrality_values)

        # Only sort patient nodes, not all nodes
        sorted_patient_nodes = sorted(patient_nodes, key=lambda node: centrality_values[node])

        if current_value < target_value:  # Add edges
            print(f"Kanten hinzufügen, um Degree Centrality zu erhöhen")
            low_centrality_nodes = [node for node in sorted_patient_nodes if centrality_values[node] < avg_centrality]
            #print(f"Low-Centrality-Nodes: {low_centrality_nodes}")

            batch_factor = 0.5
            batch_size = min(max(1, int(batch_factor * len(low_centrality_nodes))), max_batch_size)
            
            # Weighted selection of the nodes that are most below average
            node_weights = np.array([avg_centrality - centrality_values[node] for node in low_centrality_nodes])
            node_weights = np.maximum(node_weights, 1e-6)
            node_weights /= node_weights.sum()

            print(f"Node Weights (Added): {node_weights[:10]} (First 10 of {len(node_weights)})")

            selected_nodes = np.random.choice(low_centrality_nodes, size=batch_size, replace=False, p=node_weights)

            for node_to_connect in selected_nodes:
                target_candidates = [node for node in graph.nodes if graph.nodes[node].get("resourceType") != "Patient"]
                if not target_candidates:
                    print("No target candidates available. Dummy nodes are added.")
                    add_dummy_nodes(graph, target_node_id=node_to_connect, num_dummy_nodes=1)
                    continue

                target_nodes = np.random.choice(target_candidates, size=min(batch_size, len(target_candidates)), replace=False)
                
                for target_node in target_nodes:
                    if is_valid_connection(graph, node_to_connect, target_node) and not graph.has_edge(node_to_connect, target_node):
                        graph.add_edge(node_to_connect, target_node)
                        # add_edge_to_xml(
                        #     xml_root,
                        #     source_type=graph.nodes[node_to_connect]["resourceType"],
                        #     target_type=graph.nodes[target_node]["resourceType"],
                        #     target_id=target_node
                        # )
                        adjustments += 1
                        print(f"Edge added: {node_to_connect} -> {target_node}")

                    if adjustments >= batch_size:
                        break
                if adjustments >= batch_size:
                    break

            current_value = recalculate_metric()
            print(f"Updated degree centrality by batch: {current_value:.4f}")

        elif current_value > target_value:  # Remove edges
            print(f"Remove edges to reduce degree centrality")
            high_centrality_nodes = [node for node in sorted_patient_nodes[::-1] if centrality_values[node] > avg_centrality]
            #print(f"High-Centrality-Nodes: {high_centrality_nodes}")

            batch_factor = 0.5
            batch_size = min(max(1, int(batch_factor * len(high_centrality_nodes))), max_batch_size)

            # Weighted selection of the nodes that are most above average
            
            node_weights = np.array([centrality_values[node] - avg_centrality for node in high_centrality_nodes])
            node_weights = np.maximum(node_weights, 1e-6)
            node_weights /= node_weights.sum()

            print(f"Node Weights (Removed): {node_weights[:10]} (First 10 of {len(node_weights)})")

            selected_nodes = np.random.choice(high_centrality_nodes, size=batch_size, replace=False, p=node_weights)

            for node_to_remove in selected_nodes:
                if graph.degree(node_to_remove) <= avg_centrality:
                    continue

                neighbors = list(graph.neighbors(node_to_remove))
                if not neighbors:
                    print(f"No neighbors for {node_to_remove}, cannot remove an edge.")
                    continue

                target_nodes = np.random.choice(neighbors, size=min(batch_size, len(neighbors)), replace=False)

                for target_node in target_nodes:
                    graph.remove_edge(node_to_remove, target_node)
                    # remove_edge_from_xml(
                    #     xml_root,
                    #     target_type=graph.nodes[target_node]["resourceType"],
                    #     target_id=target_node
                    # )
                    adjustments += 1
                    print(f"Edge removed: {node_to_remove} -> {target_node}")
                    if adjustments >= batch_size:
                        break
                if adjustments >= batch_size:
                    break
        current_value = recalculate_metric()
        print(f"Updated degree centrality by batch: {current_value:.4f}")

        if adjustments == 0:
            print("No further adjustments possible.")
            break

    print(f"Target value for degree centrality achieved: {current_value:.4f} "
          f"(In the range: [{target_value - GRAPH_METRIC_CONFIG['degree_centrality']['tolerance']:.4f}, "
          f"{target_value + GRAPH_METRIC_CONFIG['degree_centrality']['tolerance']:.4f}])")
    return current_value







def adjust_clustering_coefficient(graph, xml_root, target_value, current_value):
    """
    Adjusts the clustering coefficient specifically for patient nodes, with a focus on triangle formation.

    Args:
        graph (nx.Graph): The graph.
        xml_root (xml.ElementTree.Element): The XML root of the graph.
        target_value (float): Target value for the clustering coefficient.
        current_value (float): Current value of the clustering coefficient.

    Returns:
        float: The updated value of the clustering coefficient.
    """
    print(f"Adjustment of the clustering coefficient: target value={target_value:.4f}, Current Value={current_value:.4f}")

    # Identify patient nodes
    patient_nodes = [node for node, data in graph.nodes(data=True) if data.get("resourceType") == "Patient"]

    def recalculate_metric():
        return calculate_clustering_coefficient(graph)

    # Scaling factor for batch size based on very small values
    scale_factor = 1000 if current_value < 0.01 else 100  # Dynamische Skalierung

    while not (target_value - GRAPH_METRIC_CONFIG["clustering_coefficient"]["tolerance"]
               <= current_value
               <= target_value + GRAPH_METRIC_CONFIG["clustering_coefficient"]["tolerance"]):
        adjustments = 0
        deviation = abs(target_value - current_value)

        # Scale the batch size based on the scaling factor
        batch_size = max(1, int(deviation * len(patient_nodes) * scale_factor))
        print(f"Calculated batch size: {batch_size} (Scaling factor: {scale_factor})")

        if current_value < target_value:
            print(f"Add edges to increase clustering coefficient (Batch Size: {batch_size})...")

            for _ in range(batch_size):
                # Choose a patient node at random
                patient_node = np.random.choice(patient_nodes)
                neighbors = list(graph.neighbors(patient_node))

                if len(neighbors) < 2:
                    # If the patient node has less than 2 neighbors, no triangle can be formed
                    print(f"Patient node {patient_node} has too few neighbors to form a triangle.")
                    continue

                # Find pairs of neighbors who are not yet connected
                potential_pairs = [
                    (n1, n2) for i, n1 in enumerate(neighbors)
                    for n2 in neighbors[i + 1:]
                    if not graph.has_edge(n1, n2) and is_valid_connection(graph, n1, n2)
                ]

                if potential_pairs:
                    # Choose a pair that forms a new triangle
                    neighbor1, neighbor2 = potential_pairs[0]  # Select the first pair found
                    graph.add_edge(neighbor1, neighbor2)
                    # add_edge_to_xml(
                    #     xml_root,
                    #     source_type=graph.nodes[neighbor1]["resourceType"],
                    #     target_type=graph.nodes[neighbor2]["resourceType"],
                    #     target_id=neighbor2
                    # )
                    print(f"Edge added (triangle): {neighbor1} -> {neighbor2}")
                    adjustments += 1
                else:
                    # Check whether a dummy node makes sense
                    print(f"No matching neighbor pairs found. Check if dummy nodes can be added.")
                    # Add dummy node only if it can connect at least two neighbors
                    dummy_node_id = add_dummy_nodes(graph, xml_root, target_node_id=patient_node, num_dummy_nodes=1)

                    if dummy_node_id is None:  
                        print("Error: No dummy node was added.")
                        continue

                    # dummy_type = graph.nodes[dummy_node_id].get("resourceType", "Dummy")
                    connected_neighbors = []

                    for other_neighbor in neighbors:
                        if is_valid_connection(graph, dummy_node_id, other_neighbor):
                            graph.add_edge(dummy_node_id, other_neighbor)
                            # add_edge_to_xml(
                            #     xml_root,
                            #     source_type=dummy_type,
                            #     target_type=graph.nodes[other_neighbor]["resourceType"],
                            #     target_id=other_neighbor
                            # )
                            connected_neighbors.append(other_neighbor)
                            print(f"Dummy-node {dummy_node_id} connected with {other_neighbor}.")

                            # Stop when the dummy knot forms a triangle
                            if len(connected_neighbors) >= 2:
                                print(f"Dummy-node {dummy_node_id} forms a triangle with {connected_neighbors}.")
                                break
                    else:
                        # Remove the dummy node if it does not form a triangle
                        print(f"Dummy-node {dummy_node_id} has not formed a triangle and is removed.")
                        graph.remove_node(dummy_node_id)
                        continue

            # Update the metric after the batch
            current_value = recalculate_metric()
            print(f"Updated Clustering Coefficient after Batch: {current_value:.4f}")

        elif current_value > target_value:
            print(f"Remove edges to reduce clustering coefficient (batch size: {batch_size})...")
            for _ in range(batch_size):
                if not patient_nodes:  
                    print("No more patients in the graph. Adjustment completed.")
                    break
            
                patient_node = np.random.choice(patient_nodes)
                if not graph.has_node(patient_node):  
                    patient_nodes.remove(patient_node)
                    continue

                neighbors = list(graph.neighbors(patient_node))

                # Search specifically for edges that close triangles
                potential_edges = [
                    (n1, n2) for n1 in neighbors for n2 in neighbors
                    if n1 != n2 and graph.has_edge(n1, n2) and n2 in graph.neighbors(n1)
                ]

                if not potential_edges:
                    print("No more edges to remove. Adjustment finished.")
                    break 

                if potential_edges:
                    # Select an edge that dissolves an existing triangle
                    edge_to_remove = potential_edges[np.random.randint(len(potential_edges))]
                    # Check whether the node still has edges
                    if graph.degree(edge_to_remove[0]) > 0 and graph.degree(edge_to_remove[1]) > 0:
                        graph.remove_edge(*edge_to_remove)                    
                        # remove_edge_from_xml(
                        #     xml_root,
                        #     target_type=graph.nodes[edge_to_remove[1]]["resourceType"],
                        #     target_id=edge_to_remove[1]
                        # )
                        print(f"Edge removed (triangle): {edge_to_remove[0]} -> {edge_to_remove[1]}")
                        adjustments += 1
                    else:
                        # Remove dummy nodes if no suitable edge exists
                        print(f"No edges found. Dummy nodes are removed.")
                        remove_nodes(graph, xml_root, nodes_to_remove=1)

            # Update the metric
            current_value = recalculate_metric()
            print(f"Updated Clustering Coefficient after Batch: {current_value:.4f}")

        if adjustments == 0:
            print("No further adjustments possible.")
            break

    print(f"Target value for clustering coefficient reached: {current_value:.4f}")
    return current_value




























