import networkx as nx
from graph_anonymization import anonymize_graph
from lxml import etree as ET

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.graph_config import graph_config
from graph_tracker import GraphTracker
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to GraphML file
graph_path = os.path.join(BASE_DIR, "graph", "graph.graphml")

# Path to the directory in which the anonymized XML files are stored
output_folder = os.path.join(BASE_DIR, "anonymized_resources")

# Parameters for differential privacy (individual for each metric)
epsilon_config = {
    "degree_distribution": 0.1,
    "clustering_coefficient": 0.1,
    "degree_centrality": 0.1,
}

sensitivity_config = {
    "degree_distribution": 100,
    "clustering_coefficient": 1,
    "degree_centrality": 1,
}


def update_references_in_graph(graph):
    """
    Update the references in the anonymized graph:
    - Removes references if the associated edge no longer exists.
    - Removes the associated 'display' values when the reference is deleted.
    - Removes empty XML tags that do not contain any further information.
    - Add missing references if a relationship exists according to the graph.
    
    Args:
        graph (nx.Graph): The anonymized graph.
    """
    from lxml import etree as ET
    from config.graph_config import graph_config

    for node, data in graph.nodes(data=True):
        if "full_record" not in data:
            continue

        full_record = data["full_record"]
        resource_type = data["resourceType"]

        try:
            root = ET.fromstring(full_record)
        except Exception as e:
            print(f"Error parsing XML for node {node}: {e}")
            continue

        # 1. extract existing references (as dictionary: text -> element)
        existing_refs = {}
        for ref in root.findall(".//reference"):
            if ref.text:
                ref_text = ref.text.strip()
                existing_refs[ref_text] = ref

        # 2. Determine valid references: Based on the neighbors in the graph and the graph_config
        valid_refs = set()
        for neighbor in graph.neighbors(node):
            neighbor_data = graph.nodes[neighbor]
            neighbor_type = neighbor_data.get("resourceType")
            if resource_type in graph_config and neighbor_type in graph_config[resource_type]:
                valid_refs.add(f"{neighbor_type}/{neighbor}")

        # 3. remove outdated references (not included in valid_refs)
        for ref_text, ref_element in list(existing_refs.items()):
            if ref_text not in valid_refs:
                parent = ref_element.getparent()
                if parent is not None:
                    parent.remove(ref_element)

                    display_elem = parent.find("display")
                    if display_elem is not None:
                        parent.remove(display_elem)
            

        #4. Recursively remove empty XML tags
        def remove_empty_elements(element):
            for child in list(element):
                remove_empty_elements(child)
                if (child.text is None or child.text.strip() == "") and len(child) == 0:
                    element.remove(child)
        remove_empty_elements(root)

        #5. Add missing references (only if they don't already exist)
        for ref_text in valid_refs:
            if ref_text not in existing_refs:
                try:
                    target_type, target_id = ref_text.split("/", 1)
                except ValueError:
                    print(f"Invalid reference format: {ref_text}. skip.")
                    continue

                
                new_ref = ET.Element("reference")
                new_ref.text = ref_text
                new_ref.tail = "\n    "  

                
                last_occurrence = None
                for ref in root.iter("reference"):
                    if ref.text and ref.text.strip().startswith(target_type + "/"):
                        last_occurrence = ref

                if last_occurrence is not None:
                    parent = last_occurrence.getparent()
                    if parent is not None:
                        index = parent.index(last_occurrence)
                        parent.insert(index + 1, new_ref)
                        
                    else:
                        root.append(new_ref)
                        
                else:
                    
                    root.append(new_ref)
                    

        # 6. Update the node's “full_record”
        graph.nodes[node]["full_record"] = ET.tostring(root, encoding="unicode", pretty_print=True)

def save_records_by_resource_type(graph, output_dir):
    """
    Saves the anonymized records from the graph in separate XML files
    based on the resource type.

    Args:
        graph (nx.Graph): The anonymized graph.
        output_dir (str): The directory in which the files are stored.
    """
    
    os.makedirs(output_dir, exist_ok=True)

  
    resource_records = {}

    for node, data in graph.nodes(data=True):
        if "resourceType" in data and "full_record" in data:
            resource_type = data["resourceType"]
            if resource_type not in resource_records:
                resource_records[resource_type] = []
            try:
                record_xml = ET.fromstring(data["full_record"])
                resource_records[resource_type].append(record_xml)
            except ET.XMLSyntaxError as e:
                print(f"failed to parse {node}: {e}")

    # Write each group in a separate XML file
    for resource_type, records in resource_records.items():
        resource_file_path = os.path.join(output_dir, f"{resource_type}.xml")
        root = ET.Element("records")  
        root.extend(records)  
        tree = ET.ElementTree(root)
        tree.write(resource_file_path, pretty_print=True, encoding="utf-8", xml_declaration=True)
        print(f"Resources of type {resource_type} saved in: {resource_file_path}")


def extract_xml_root_from_graph(graph):
    """
    Extracts the XML root from the 'full_record' attributes of the nodes in the graph.

    Args:
        graph (nx.Graph): The graph with the XML records in the nodes.

    Returns:
        xml.etree.ElementTree.Element: The combined XML root.
    """
    root = ET.Element("records") 
    for node, data in graph.nodes(data=True):
        if "full_record" in data:
            record_xml = ET.fromstring(data["full_record"])
            root.append(record_xml)
    return root

def remove_isolated_nodes(graph):
    """
    Removes all isolated nodes (with degree 0) from the graph.
    
    Args:
        graph (nx.Graph): The graph in which isolated nodes are to be removed.
    """
    
    isolated_nodes = [node for node, degree in graph.degree() if degree == 0]
    for node in isolated_nodes:
        graph.remove_node(node)
        print(f"isolated node {node} removed.")

def main():
    try:
        
        print("Load graph...")
        graph = nx.read_graphml(graph_path)
        print("loaded successfully.")

        
        tracker = GraphTracker(graph)
        tracker.patch_graph_methods()

        
        print("Extract XML data from the graph nodes...")
        xml_root = extract_xml_root_from_graph(graph)
        print("successfully extracted.")

        
        print("\nStart anonymization...")
        anonymized_graph, noised_metrics = anonymize_graph(
            graph, 
            xml_root, 
            epsilon_config, 
            sensitivity_config
        )

      
        print("\nNoisy metrics:")
        for metric, value in noised_metrics.items():
            print(f"  {metric}: {value:.4f}")

        for node, attrs in anonymized_graph.nodes(data=True):
            for key, value in attrs.items():
                if isinstance(value, np.str_):  
                    anonymized_graph.nodes[node][key] = str(value)  

        for u, v, attrs in anonymized_graph.edges(data=True):
            for key, value in attrs.items():
                if isinstance(value, np.str_):  
                    anonymized_graph.edges[u, v][key] = str(value)  

        # Save anonymized graph
        anonymized_graph_path = r"C:\Users\Nutzer\Desktop\Master_FHIR_Anonymizer\graph\anonymized_graph.graphml"
        nx.write_graphml(anonymized_graph, anonymized_graph_path)
        print(f"\nAnonymized graph stored under: {anonymized_graph_path}")

        # Reload the anonymized graph
        print("Reload the anonymized graph...")
        anonymized_graph = nx.read_graphml(anonymized_graph_path)
        print("Anonymized graph successfully loaded.")

        tracker.save_tracking_log("performance_tracking.csv")

        
        print("\nRemove isolated nodes from the graph...")
        remove_isolated_nodes(anonymized_graph)
        print("done.")

        
        print("\nUpdate the references in the anonymized graph...")
        update_references_in_graph(anonymized_graph)
        print("done.")

       
        print("\nSave anonymized resources in separate files...")
        save_records_by_resource_type(anonymized_graph, output_folder)
        print("done.")


    except Exception as e:
        print(f"Fehler: {e}")

if __name__ == "__main__":
    main()
