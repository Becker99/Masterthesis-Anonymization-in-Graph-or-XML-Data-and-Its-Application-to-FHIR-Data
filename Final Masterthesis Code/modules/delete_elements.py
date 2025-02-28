import os
import xml.etree.ElementTree as ET

def delete_elements_by_config(input_folder, output_folder, config):
    """
    Deletes elements from XML files based on the configuration.

    :param input_folder: Folder with the input files.
    :param output_folder: Folder with the edited files.
    :param config: Configuration file with paths of the elements to be deleted.
    """
    os.makedirs(output_folder, exist_ok=True)

    def process_file(file_name, file_config):
        input_file_path = os.path.join(input_folder, file_name)
        output_file_path = os.path.join(output_folder, file_name)

        print(f"Edit file: {input_file_path}")

        try:
            # Load XML
            tree = ET.parse(input_file_path)
            root = tree.getroot()

            # Iterate over the configuration paths
            for record_path in file_config.get("record_paths", []):
                element_path = record_path["path"]

                print(f"Search elements with path: {element_path}")

                # Search for parent nodes and delete the children
                for parent in root.findall(element_path.rsplit("/", 1)[0]):
                    print(f"Found parent node: {ET.tostring(parent, encoding='unicode')}")
                    for element in parent.findall(element_path.split("/")[-1]):
                        print(f"Delete element: {ET.tostring(element, encoding='unicode')}")
                        parent.remove(element)

            # Save the edited file
            tree.write(output_file_path, encoding="utf-8", xml_declaration=True)
            print(f"File saved successfully: {output_file_path}")

        except ET.ParseError as e:
            print(f"Error parsing the file {input_file_path}: {e}")

    # Iterate over the files and configuration prefixes
    for resource_type, file_config in config.items():
        for file_name in os.listdir(input_folder):
            if file_name.startswith(resource_type) and file_name.endswith(".xml"):
                process_file(file_name, file_config)

