import os
import shutil
import logging
import networkx as nx 


from concurrent.futures import ProcessPoolExecutor

from modules.delete_elements import delete_elements_by_config
from config.delete_config import delete_config_file

from config.lap_gauss_config import lap_gauss_config_file
from modules.lap_gauss_processing import process_laplace_gaussian_wrapper

from config.exp_config import exponential_config_file
from modules.exp_processing import process_resource

from modules.id_mapping import build_global_id_mapping, update_references_parallel, global_id_mapping


from modules_graph.graph_builder import (extract_reference_types, load_or_create_config, parse_and_add_nodes_edges, G,  # Der initialisierte Graph
)
from modules_graph.node_config_creation import analyze_dataset_and_create_node_config



def main():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    original_folder_path = os.path.join(BASE_DIR, "data", "original10")
    temp_output_folder_path = os.path.join(BASE_DIR, "data", "temp_anonymized")
    final_output_folder_path = os.path.join(BASE_DIR, "data", "anonymized")
    id_mapping_output_folder_path = os.path.join(BASE_DIR, "data", "id_mapped")
    config_output_path = os.path.join(BASE_DIR, "config", "graph_config.py")
    node_config_output_path = os.path.join(BASE_DIR, "config", "node_config.py")


    max_iterations = 1000

    # ----------------- Step 1: Algorithm 1 -----------------
    print("Start Algorithm 1 Anonymization...")

    os.makedirs(temp_output_folder_path, exist_ok=True)

    files_to_process = [
        filename for filename in os.listdir(original_folder_path) if filename.endswith(".xml")
    ]

    with ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(
                process_laplace_gaussian_wrapper,
                filename,
                original_folder_path,
                temp_output_folder_path,  
                lap_gauss_config_file,
                max_iterations
            )
            for filename in files_to_process
        ]
        for future in futures:
            future.result()

    print("Algorithm 1 completed!")

    # ----------------- Step 2: Algorithm 2 Anonymization -----------------
    print("Start Algorithm 2 Anonymization...")

    os.makedirs(final_output_folder_path, exist_ok=True)

    
    for filename in os.listdir(temp_output_folder_path):
        if filename.endswith('.xml'):
            temp_file_path = os.path.join(temp_output_folder_path, filename)
            final_output_file_path = os.path.join(final_output_folder_path, filename)
            shutil.copy(temp_file_path, final_output_file_path)

    
    with ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(
                process_resource,
                resource,
                attributes,
                final_output_folder_path,  
                final_output_folder_path,  
                max_iterations
            )
            for resource, attributes in exponential_config_file.items()
        ]
        for future in futures:
            future.result()

    # Delete the temporary output
    shutil.rmtree(temp_output_folder_path)

    # ----------------- Step 3: Permanently delete unwanted items -----------------
    print("Start the final deletion of unwanted items...")
    delete_elements_by_config(final_output_folder_path, final_output_folder_path, delete_config_file)
    print("Final deletion completed..")

    logging.info(f"The combined anonymization has been completed. Final output: {final_output_folder_path}")

    # # ----------------- Step 4: ID-Mapping -----------------
    # print("Start ID Mapping...")

    # 
    # os.makedirs(id_mapping_output_folder_path, exist_ok=True)

    # # Step 4.1: Create global ID mapping
    # build_global_id_mapping(final_output_folder_path)

    # # Step 4.2: Process files in parallel
    # args = [
    #     (os.path.join(final_output_folder_path, file_name),
    #     os.path.join(id_mapping_output_folder_path, file_name),
    #     global_id_mapping)
    #     for file_name in os.listdir(final_output_folder_path)
    #     if file_name.endswith(".xml")
    # ]

    # with ProcessPoolExecutor() as executor:
    #     executor.map(update_references_parallel, args)

    
    # for file_name in os.listdir(id_mapping_output_folder_path):
    #     temp_file_path = os.path.join(id_mapping_output_folder_path, file_name)
    #     final_file_path = os.path.join(final_output_folder_path, file_name)
    #     shutil.move(temp_file_path, final_file_path)

    # # Delete the temporary ID mapping folder
    # shutil.rmtree(id_mapping_output_folder_path)

    # print(f"ID mapping completed. Final output: {final_output_folder_path}")

    # logging.info(f"The combined anonymization has been completed. Final output: {final_output_folder_path}")

    # ----------------- Step 5: Graph-Builder -----------------
    print("Start Graph Builder...")

    # Create the graph configuration based on the XML data
    extract_reference_types(final_output_folder_path, config_output_path)

    print(f"Graph configuration complete. Configuration saved in: {config_output_path}")
    logging.info(f"The graph configuration was successfully completed.")

    # ----------------- Step 6: Create a graph -----------------
    print("Create graph based on configuration...")

    
    # Load or create dynamic configuration
    config_path = os.path.join(BASE_DIR, "config", "graph_config.py")
    graph_config = load_or_create_config(final_output_folder_path, config_path)

    # Create graph from XML data
    for filename in os.listdir(final_output_folder_path):
        if filename.endswith(".xml"):
            resource_type = filename.split(".")[0]
            parse_and_add_nodes_edges(os.path.join(final_output_folder_path, filename), resource_type, graph_config)

    # Save graph
    save_path_graph = os.path.join(BASE_DIR, "graph", "graph.graphml")
   
    os.makedirs(os.path.dirname(save_path_graph), exist_ok=True)
    nx.write_graphml(G, save_path_graph)
    
    # Output the number of nodes and edges
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    print(f"The graph contains {num_nodes} nodes and {num_edges} edges.")

    print(f"Graph successfully saved: {save_path_graph}")


    # ----------------- Step 7: Create Node Config -----------------
    print("Create node configuration...")
    analyze_dataset_and_create_node_config(final_output_folder_path, node_config_output_path)
    print(f"Node configuration successfully created and saved under: {node_config_output_path}")


if __name__ == "__main__":
    main()
