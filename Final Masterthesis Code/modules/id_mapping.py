import xml.etree.ElementTree as ET
import uuid
import os

# Dictionary for central assignment of original IDs to new IDs
global_id_mapping = {}

def generate_unique_id():
    """
    Generates a new unique ID in UUID format and ensures that no duplicates are created.
    :return: Unique ID as a string
    """
    while True:
        new_id = str(uuid.uuid4())
        if new_id not in global_id_mapping.values():
            return new_id

def map_id(original_id):
    """
    Creates a new ID for an original ID or returns the existing assignment.
    :param original_id: Original ID
    :return: Newly assigned ID
    """
    if original_id not in global_id_mapping:
        new_id = generate_unique_id()
        global_id_mapping[original_id] = new_id
    return global_id_mapping[original_id]

def replace_id_in_record(record, original_id, new_id):
    """
    Searches an entire record and replaces all occurrences of the original ID with the new ID.
    :param record: XML element of the record
    :param original_id: Original ID
    :param new_id: Newly assigned ID
    """
    for element in record.iter():
        if element.text == original_id:
            element.text = new_id

def build_global_id_mapping(input_dir):
    """
    Runs through all files and creates a global mapping from original IDs to new IDs.
    :param input_dir: Directory with the input files
    """
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.xml'): 
            file_path = os.path.join(input_dir, file_name)
            tree = ET.parse(file_path)
            root = tree.getroot()
            for record in root.findall(".//record"):
                id_element = record.find("id")
                if id_element is not None and id_element.text:
                    original_id = id_element.text
                    map_id(original_id)

def update_references_parallel(args):
    """
    Parallel processing of a file to update the references.
    :param args: Tuple with (file_path, output_path, global_id_mapping)
    """
    file_path, output_path, global_id_mapping = args
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Update IDs and references within each record
    for record in root.findall(".//record"):
        id_element = record.find("id")
        if id_element is not None and id_element.text:
            original_id = id_element.text
            if original_id in global_id_mapping:
                new_id = global_id_mapping[original_id]
                id_element.text = new_id
                replace_id_in_record(record, original_id, new_id)

    # Update references outside the records
    for ref_element in root.findall(".//reference"):
        if ref_element.text and "/" in ref_element.text:
            resource_type, original_id = ref_element.text.split("/", 1)
            if original_id in global_id_mapping:
                new_id = global_id_mapping[original_id]
                ref_element.text = f"{resource_type}/{new_id}"

    # Write the updated file
    tree.write(output_path, encoding='utf-8', xml_declaration=True)


def process_files(input_dir, output_dir):
    """
    Performs the entire ID anonymization and reference update.
    :param input_dir: Directory with the input files
    :param output_dir: Directory for the output files
    """
    os.makedirs(output_dir, exist_ok=True)

    # Step 1:  Create global ID mapping
    build_global_id_mapping(input_dir)

    # Step 2: Update references
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.xml'): 
            input_file_path = os.path.join(input_dir, file_name)
            output_file_path = os.path.join(output_dir, file_name)
            update_references_parallel(input_file_path, output_file_path)
