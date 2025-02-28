import os
import xml.etree.ElementTree as ET
from collections import Counter

def extract_attributes_modular(folder_path, config):
    """
    Extracts attributes based on the configuration and counts their values.

    :param folder_path: Path to the folder with the XML files.
    :param config: Configuration of the attributes.
    :return: A dictionary with attribute names as keys and their counted values as 'counters'.
    """
    # Validation of the input parameters
    if not isinstance(config, dict):
        raise ValueError("The configuration must be a dictionary (dict).")
    if not os.path.isdir(folder_path):
        raise ValueError("The transferred folder path is invalid or does not exist.")
    
    # Initialize the result dictionary
    attribute_counts = {attr: Counter() for resource in config.values() for attr in resource.keys()}

    # Iterate over the files in the folder
    for filename in os.listdir(folder_path):
        resource = filename.split('.')[0]  # Derive resource from the file name
        if resource not in config:
            continue  # Skip files that are not included in the configuration
        
        file_path = os.path.join(folder_path, filename)
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Iteriere über die Attribute der Ressource
            for attr, details in config[resource].items():
                if details["type"] == "simple":
                    path = details["path"]
                    for element in root.findall(path):
                        if element.text:
                            attribute_counts[attr][element.text.strip()] += 1

                elif details["type"] == "combination":
                    paths = details["paths"]
                    for group in zip(*(root.findall(path) for path in paths)):
                        combination = tuple(e.text.strip() for e in group if e is not None)
                        if len(combination) == len(paths):
                            attribute_counts[attr][combination] += 1

                elif details["type"] == "nested":
                    path = details["path"]
                    filter_url = details["filter"]["url"]
                    value_path = details["filter"]["value_path"]
                    for item in root.findall(path):
                        url_element = item.find(".//url")
                        if url_element is not None and url_element.text == filter_url:
                            value_element = item.find(value_path)
                            if value_element is not None and value_element.text:
                                attribute_counts[attr][value_element.text.strip()] += 1

                elif details["type"] == "nested_combination":
                    path = details["path"]
                    filter_url = details["filter"]["url"]
                    value_paths = details["filter"]["value_paths"]
                    for item in root.findall(path):
                        url_element = item.find(".//url")
                        if url_element is not None and url_element.text == filter_url:
                            combination = []
                            for value_path in value_paths:
                                value_element = item.find(value_path)
                                if value_element is not None and value_element.text:
                                    combination.append(value_element.text.strip())
                            if len(combination) == len(value_paths):
                                attribute_counts[attr][tuple(combination)] += 1
        except ET.ParseError:
            print(f"Error parsing the file: {filename}")
            continue

    return attribute_counts
