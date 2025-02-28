import os
import xml.etree.ElementTree as ET
import json


def analyze_dataset_and_create_node_config(dataset_path, config_path):
    """
    Analyzes the XML files in the data set, extracts the structure of the resource entries,
    and creates a Python file with the configuration.

    Args:
        dataset_path (str): Path to the XML files of the data set.
        config_path (str): Path to the output of the Python configuration file.

    Returns:
        dict: The analyzed structure of the resources.
    """
    resource_config = {}

    # Iterate over all files in the given path
    for filename in os.listdir(dataset_path):
        if filename.endswith(".xml"):
            file_path = os.path.join(dataset_path, filename)
            
            
            try:
                tree = ET.parse(file_path)
                root = tree.getroot()
                
                
                first_record = root.find(".//record")
                if first_record is None:
                    print(f"Keine <record>-Einträge in Datei {filename} gefunden.")
                    continue

                
                resource_type = first_record.findtext("resourceType")
                if not resource_type:
                    print(f"Ressourcentyp fehlt in Datei {filename}.")
                    continue

                
                structure = analyze_resource_structure(first_record)

                
                resource_config[resource_type] = structure

            except ET.ParseError as e:
                print(f"Fehler beim Parsen der Datei {filename}: {e}")
    
    
    save_node_config(resource_config, config_path)

    print(f"Configuration file was successfully created under {config_path}.")
    return resource_config


def analyze_resource_structure(record):
    """
    Analyzes the structure of a <record> entry.

    Args:
        record (xml.etree.ElementTree.Element): The <record> element.

    Returns:
        dict: Nested structure of resource records.
    """
    structure = {}

    
    def analyze_element(element):
        children = list(element)
        if not children:
            return {"is_leaf": True}  
        else:
            return {
                "is_leaf": False,
                "children": {
                    child.tag: analyze_element(child) for child in children
                }
            }

    for child in record:
        structure[child.tag] = analyze_element(child)

    return structure


def save_node_config(resource_config, config_path):
    """
    Saves the analyzed resource configuration as a Python module.

    Args:
        resource_config (dict): The analyzed resource configuration.
        config_path (str): Path to the output of the Python configuration file.
    """
    with open(config_path, "w") as config_file:
        config_file.write("# Dynamically generated configuration file\n")
        config_file.write("NODE_CONFIG = ")
        config_file.write(
            json.dumps(
                resource_config,
                indent=4
            ).replace("true", "True").replace("false", "False")  
        )


