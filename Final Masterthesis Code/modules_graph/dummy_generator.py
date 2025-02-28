from lxml.etree import Element, SubElement, tostring, fromstring
import os
import sys


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

project_dir = os.path.abspath(os.path.join(BASE_DIR, ".."))
sys.path.append(project_dir)
os.chdir(project_dir)

from config.node_config import NODE_CONFIG


def create_dummy_node_xml(resource_type, dummy_node_id, connected_node_id=None, connected_node_type=None):
    """
    Creates a dummy node based on the structure in NODE_CONFIG.

    Args:
        resource_type (str): The resource type (e.g. “Encounter”, “Condition”).
        dummy_node_id (str): The ID of the dummy node.
        connected_node_id (str): The ID of the connected node (optional).
        connected_node_type (str): The type of the connected node (optional).

    Returns:
        str: An XML string representation of the dummy node.
    """
    if resource_type not in NODE_CONFIG:
        raise ValueError(f"Resource type {resource_type} not in NODE_CONFIG defined.")

    # Get the structure for the resource type
    resource_structure = NODE_CONFIG[resource_type]

    # Create the root
    root = Element("record")

    # Add `resourceType` and `id` (these must always be filled in correctly)
    SubElement(root, "resourceType").text = resource_type
    SubElement(root, "id").text = dummy_node_id

    # Recursive function to create the structure
    def add_children(parent, structure):
        for tag, details in structure.items():
            if tag in ["resourceType", "id", "reference"]:
                # Skip `resourceType`, `id`, and `reference` tags
                continue

            child = SubElement(parent, tag)

            if details["is_leaf"]:
                # Fill sheets with “unspecified”
                child.text = "unspecified"
            else:
                # Add children recursively
                for child_tag, child_details in details["children"].items():
                    add_children(child, {child_tag: child_details})

    # Add children based on structure
    add_children(root, resource_structure)

    # Optionally add reference tags (for later connections if needed)
    if connected_node_id and connected_node_type:
        reference = SubElement(root, "reference")
        reference.text = f"{connected_node_type}/{connected_node_id}"

    # Return as XML string
    return tostring(root, encoding="unicode", pretty_print=True)



