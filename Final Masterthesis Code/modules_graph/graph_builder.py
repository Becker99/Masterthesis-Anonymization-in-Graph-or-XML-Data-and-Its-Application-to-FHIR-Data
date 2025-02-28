import os
from lxml import etree as ET  
from collections import defaultdict
import networkx as nx  


G = nx.Graph()  


def extract_reference_types(folder_path, output_config_path):
    """
    Analyze the first 10 entries of each file, record the types of references and create a configuration file.

    Args:
        folder_path (str): Path to the folder with the XML files.
        output_config_path (str): Path to the configuration output file.

    Returns:
        None
    """
    config = defaultdict(set)

    for filename in os.listdir(folder_path):
        if filename.endswith(".xml"):
            resource_type = filename.split(".")[0]
            file_path = os.path.join(folder_path, filename)

            tree = ET.parse(file_path)
            root = tree.getroot()

            for i, record in enumerate(root.findall(".//record")):
                if i >= 10:
                    break

                for ref_tag in record.findall(".//reference"):
                    if ref_tag.text and "/" in ref_tag.text:
                        ref_text = ref_tag.text.strip()
                        ref_resource = ref_text.split("?")[0] if "?" in ref_text else ref_text.split("/")[0]

                        if ref_resource in {"Practitioner", "Organization", "Location"}:
                            config[resource_type].add((ref_resource, ref_resource))
                        else:
                            config[resource_type].add((ref_resource, f"references to {resource_type}"))

    with open(output_config_path, "w") as config_file:
        config_file.write("# Dynamically generated configuration\n")
        config_file.write("graph_config = {\n")
        for resource, references in config.items():
            config_file.write(f"    '{resource}': {{\n")
            for ref, edge in sorted(references):
                config_file.write(f"        '{ref}': '{edge}',\n")
            config_file.write("    },\n")
        config_file.write("}\n")

    print(f"Configuration was successfully created: {output_config_path}")


def load_or_create_config(folder_path, config_path):
    """
    Make sure the configuration file exists. If not, generate it dynamically.

    Args:
        folder_path (str): Path to the XML files.
        config_path (str): Path to the configuration file.

    Returns:
        dict: The loaded configuration.
    """
    if not os.path.exists(config_path):
        print("Configuration file not found. Creating dynamic configuration...")
        extract_reference_types(folder_path, config_path)

    from config.graph_config import graph_config  
    return graph_config


def parse_and_add_nodes_edges(file_path, resource_type, graph_config):
    tree = ET.parse(file_path)
    root = tree.getroot()

    for record in root.findall('.//record'):
        add_record_with_full_xml(record, resource_type)

        # ID of the current record (source)
        src_id = record.find('id').text

        # Search recursively for all <reference> tags, even in nested structures
        for ref_tag in record.findall(".//reference"):
            ref_text = ref_tag.text
            if ref_text:
                # Target: ID and resource type from <reference> tag
                ref_resource = ref_text.split("?")[0] if "?" in ref_text else ref_text.split("/")[0]
                tgt_id = ref_text.split("/")[-1]

                # Check if the reference type is present in the configuration
                if resource_type in graph_config and ref_resource in graph_config[resource_type]:
                    edge_label = f"{resource_type}/{ref_resource} relation"

                    # Case 1: Reference to Organization, Practitioner or Location
                    if ref_resource in {"Organization", "Practitioner", "Location"}:
                        # Hole den <display>-Text
                        parent = ref_tag.getparent()  
                        display_name = None
                        if parent is not None and parent.find("display") is not None:
                            display_name = parent.find("display").text.strip()

                        # Add nodes based on display_name
                        if display_name and not G.has_node(display_name):
                            G.add_node(
                                display_name,
                                resourceType=ref_resource,
                                display_name=display_name
                            )
                        # Add an edge between the ID and the display_name
                        if display_name:
                            add_edge_with_attributes(src_id, display_name, edge_label)

                    # Case 2: All other references (e.g. observation)
                    else:
                        # Add destination node as ID if it does not already exist
                        if not G.has_node(tgt_id):
                            G.add_node(tgt_id, resourceType=ref_resource)
                        # Add the edge based on the ID
                        add_edge_with_attributes(src_id, tgt_id, edge_label)



def add_record_with_full_xml(record, resource_type):
    res_id = record.find('id').text
    attributes = {
        'resourceType': resource_type,
        'full_record': ET.tostring(record, encoding="unicode").strip()  
    }
    G.add_node(res_id, **attributes)  

    for ref_tag in record.findall('.//reference'):
        ref_text = ref_tag.text
        if ref_text:
            ref_resource = ref_text.split("?")[0] if "?" in ref_text else ref_text.split("/")[0]

            if ref_resource in {"Practitioner", "Organization", "Location"}:
                display_name = ref_tag.getparent().find("display").text if ref_tag.getparent() is not None else "Unknown"
                if not G.has_node(display_name):
                    G.add_node(display_name, resourceType=ref_resource, display_name=display_name)

def add_edge_with_attributes(src_id, tgt_id, relationship):
    """
    Add an edge if it does not yet exist and label it with a custom relation.

    Args:
        src_id (str): ID of source.
        tgt_id (str): ID of target.
        relationship (str): Description of the relationship.

    Returns:
        None
    """
    if src_id != tgt_id:
        if not G.has_edge(src_id, tgt_id):
            G.add_edge(src_id, tgt_id, relationship=relationship)
