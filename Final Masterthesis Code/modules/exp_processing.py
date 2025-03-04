import os
import csv
import xml.etree.ElementTree as ET
import logging
import time
import psutil
from modules.tvd import calculate_tvd
from modules.exp_extract_attributes import extract_attributes_modular
from modules.exp_anonymization import anonymize_elements_modular
from modules.exp_adjustment import calculate_utility_scores, add_laplace_noise_to_counters, adjust_epsilon_based_on_tvd
from modules.exp_dummy_handler import add_dummy_to_pool, create_dummy_value_for_attribute


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
evaluation_csv_path = os.path.join(BASE_DIR, "evaluation", "exp_iterations.csv")
performance_csv_path = os.path.join(BASE_DIR, "evaluation", "algo2_performance_metrics.csv")

# Initialize the CSV file with header
if not os.path.exists(performance_csv_path):
    with open(performance_csv_path, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Iteration", "Attribut", "Execution Time (s)", "RAM Before (MB)", "RAM After (MB)", "Records Processed"])

def track_performance(iteration, attribute, start_time, memory_before, memory_after, records_processed):
    """ Measures and saves performance metrics for an iteration """
    end_time = time.time()
    execution_time = end_time - start_time  

    with open(performance_csv_path, mode="a", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([iteration, attribute, round(execution_time, 4), round(memory_before, 2),
                         round(memory_after, 2), records_processed])

    print(f"[Iteration {iteration} - {attribute}] Execution: {execution_time:.2f}s, "
          f"RAM: {memory_before:.2f}MB → {memory_after:.2f}MB, "
          f"Records Processed: {records_processed}")

# Initialize the CSV file with the header line
if not os.path.exists(os.path.dirname(evaluation_csv_path)):
    os.makedirs(os.path.dirname(evaluation_csv_path))

if not os.path.exists(evaluation_csv_path):
    with open(evaluation_csv_path, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Ressource", "Attribut", "Epsilon", "Sensitivity", "Iteration", "TVD"])

def log_iteration_to_csv(resource, attribute, epsilon, sensitivity, iteration, tvd):
    """
    Logs the iteration results directly to the CSV file.
    """
    with open(evaluation_csv_path, mode="a", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([resource, attribute, epsilon, sensitivity, iteration, tvd])

def process_resource(resource, attributes, input_folder, output_folder, max_iterations):
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logging.info(f"Edited resource: {resource}")

    # Count original values and calculate initial utility scores
    resource_original_counts = extract_attributes_modular(output_folder, {resource: attributes})
    utility_scores = {
        attr: calculate_utility_scores(counts) if counts else {}
        for attr, counts in resource_original_counts.items()
    }

    active_attributes = {attr: True for attr in attributes.keys()}
    tvd_targets = {attr: details["tvd_range"] for attr, details in attributes.items()}
    dynamic_epsilon = {attr: {"epsilon": 0.5} for attr in attributes.keys()}
    dummy_added = {attr: False for attr in attributes.keys()}

    for iteration in range(1, max_iterations + 1):
        logging.info(f"--- Iteration {iteration} für Ressource {resource} ---")

        start_time_iteration = time.time()
        process = psutil.Process(os.getpid())  
        memory_before = process.memory_info().rss / (1024 * 1024)  

        # Update counter with noise
        counters = {
            attr: add_laplace_noise_to_counters(counts, dynamic_epsilon[attr]["epsilon"]) if counts else {}
            for attr, counts in resource_original_counts.items()
        }

        # Calculate number of processed data records
        records_processed = sum(len(counts) for counts in resource_original_counts.values())

        for attr in attributes.keys():
            # Add dummy value when ε_min is reached
            if dynamic_epsilon[attr]["epsilon"] <= 0.0002:
                if not dummy_added[attr]:
                    logging.warning(f"ε_min achieved for '{attr}'. Add dummy value.")
                    resource_original_counts = add_dummy_to_pool(attr, attributes[attr], resource_original_counts)
                    utility_scores[attr] = calculate_utility_scores(resource_original_counts[attr])
                    dynamic_epsilon[attr]["epsilon"] = 0.5
                    dummy_added[attr] = True
                    logging.info(f"Dummy value added and ε set to 0.5 for '{attr}'.")
                else:
                    logging.warning(f"ε_min achieved for '{attr}' again. Double dummy value counter.")
                    dummy_value = create_dummy_value_for_attribute(attributes[attr])
                    resource_original_counts[attr][dummy_value] *= 4
                    utility_scores[attr] = calculate_utility_scores(resource_original_counts[attr])
                    dynamic_epsilon[attr]["epsilon"] = 0.5
                    logging.info(f"Dummy value doubled and ε set to 0.5 for '{attr}'.")

        # Anonymisierung der Dateien
        for filename in os.listdir(input_folder):
            if filename.startswith(resource) and filename.endswith(".xml"):
                input_file_path = os.path.join(input_folder, filename)
                output_file_path = os.path.join(output_folder, filename)

                try:
                    tree = ET.parse(input_file_path)
                    anonymize_elements_modular(
                        tree, utility_scores, counters, dynamic_epsilon,
                        active_attributes, {resource: attributes}
                    )
                    tree.write(output_file_path, xml_declaration=True, encoding='utf-8')
                    logging.info(f"File {filename} successfully anonymized.")
                except ET.ParseError as e:
                    logging.warning(f"Error parsing the file {filename}: {e}")
                    continue

        memory_after = process.memory_info().rss / (1024 * 1024)  

        for attr in attributes.keys():
            track_performance(iteration, attr, start_time_iteration, memory_before, memory_after, records_processed)
        
        # TVD calculation and ε-adjustment
        anonymized_counts = extract_attributes_modular(output_folder, {resource: attributes})
        stop_iteration = True

        for attr in attributes.keys():
            if not active_attributes[attr] or not resource_original_counts[attr]:
                continue

            tvd = calculate_tvd(resource_original_counts[attr], anonymized_counts[attr])
            logging.info(f"TVD for '{attr}' after iteration {iteration}: {tvd:.4f}")

            sensitivity = attributes[attr].get("sensitivity", "N/A")
            epsilon = dynamic_epsilon[attr]["epsilon"]
            log_iteration_to_csv(resource, attr, epsilon, sensitivity, iteration, tvd)

            tvd_min, tvd_max = tvd_targets[attr]
            if tvd_min <= tvd <= tvd_max:
                logging.info(f"TVD target range for '{attr}' achieved.")
                active_attributes[attr] = False
            else:
                dynamic_epsilon[attr] = adjust_epsilon_based_on_tvd(
                    dynamic_epsilon[attr], tvd, (tvd_min, tvd_max), attr
                )
                stop_iteration = False

        if stop_iteration:
            logging.info(f"All attributes for resource '{resource}' have reached the TVD target range.")
            break
    else:
        logging.warning(f"Maximum number of iterations ({max_iterations}) for resource '{resource}' achieved.")
