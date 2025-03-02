import os
import logging
import csv
import time
import psutil

import xml.etree.ElementTree as ET
from modules.dates_grouping import anonymize_date_grouping, anonymize_deceased_date_grouping
from modules.lap_gauss_anonymization import anonymize_dates, anonymize_decimal_values
from modules.lap_gauss_adjustment import adjust_parameters, calculate_dynamic_sensitivity




BASE_DIR = os.path.dirname(os.path.abspath(__file__))
evaluation_csv_path = os.path.join(BASE_DIR, "evaluation", "lap_gauss_iterations.csv")
performance_csv_path = os.path.join(BASE_DIR, "evaluation", "algo1_performance_metrics.csv")

# Initialize the CSV file with header
if not os.path.exists(performance_csv_path):
    with open(performance_csv_path, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Iteration", "Attribut", "Execution Time (s)", "RAM Before (MB)", "RAM After (MB)",
                         "Records Processed"])

def track_performance(iteration, attribute, input_file, output_file, start_time, records_processed):
    """ Measures and saves performance metrics for an iteration """
    process = psutil.Process(os.getpid())  
    end_time = time.time()
    execution_time = end_time - start_time 

    memory_before = process.memory_info().rss / (1024 * 1024)  
    memory_after = process.memory_info().rss / (1024 * 1024)  

    

    with open(performance_csv_path, mode="a", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([iteration, attribute, round(execution_time, 4), round(memory_before, 2),
                        round(memory_after, 2), records_processed])


    print(f"[Iteration {iteration} - {attribute}] Execution: {execution_time:.2f}s, "
          f"RAM: {memory_before:.2f}MB → {memory_after:.2f}MB"
          f"Records Processed: {records_processed}")
    

# Initialize the CSV file with the header line
if not os.path.exists(os.path.dirname(evaluation_csv_path)):
    os.makedirs(os.path.dirname(evaluation_csv_path))

if not os.path.exists(evaluation_csv_path):
    with open(evaluation_csv_path, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        # Write the header
        writer.writerow(["Ressource", "Attribut", "Epsilon", "Sensitivity", "Delta", "Iteration", "RMSE"])

def log_iteration_to_csv(resource, attribute, epsilon, sensitivity, delta, iteration, rmse):
    """
    Logs the iteration results directly to the CSV file.
    """
    with open(evaluation_csv_path, mode="a", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([resource, attribute, epsilon, sensitivity, delta, iteration, rmse])

def process_laplace_gaussian_wrapper(filename, original_folder_path, temp_output_folder_path, lap_gauss_config_file, max_iterations):
    """
    Wrapper function for Laplace/Gaussian anonymization.
    """
    input_file_path = os.path.join(original_folder_path, filename)
    temp_output_file_path = os.path.join(temp_output_folder_path, filename)

    logging.info(f"Start Laplace/Gaussian anonymization for file: {filename}")

    try:
        start_time_total = time.time()
        process = psutil.Process(os.getpid())


        memory_before_loading = process.memory_info().rss / (1024 * 1024)  # RAM in MB

        # Load original XML file
        tree = ET.parse(input_file_path)
        root = tree.getroot()

        memory_after_loading = process.memory_info().rss / (1024 * 1024)  # RAM in MB
        
        # Enter number of data records
        records_processed = len(root.findall(".//record"))

        # Initialize the configuration
        # wenn Empfindlichkeit dynamisch: config = calculate_dynamic_sensitivity(root, lap_gauss_config_file, filename)
        config = lap_gauss_config_file
        for resource, attributes in config.items():
            for attribute, settings in attributes.items():
                if "parameters" not in settings:
                    settings["parameters"] = {}
                # Setze die Standardwerte für `parameters`
                settings["parameters"].setdefault("epsilon", 0.5)
                settings["parameters"].setdefault("sensitivity", 1)  # Statische Sensitivity
                if "delta" not in settings["parameters"] and "Gaussian" in settings.get("mechanism", ""):
                    settings["parameters"]["delta"] = 1e-5

        iteration = 0
        all_within_range = False

        while iteration < max_iterations and not all_within_range:
            start_time_iteration = time.time()
            all_within_range = True
            rmse_results = {}
            logging.info(f"--- Iteration {iteration + 1} gestartet für Datei: {filename} ---")

            # Group birthDate and deceasedDateTime
            # for element in root.findall(".//birthDate"):
            #     if element.text:
            #         element.text = anonymize_date_grouping(element.text, grouping_type='decade')
            # for element in root.findall(".//deceasedDateTime"):
            #     if element.text:
            #         element.text = anonymize_deceased_date_grouping(element.text, grouping_type='decade')

            # Processing the attributes
            for resource, attributes in config.items():
                if resource.lower() in filename.lower():
                    for attribute, settings in attributes.items():
                        rmse_range = settings.get("rmse_range", [0, 100])
                        mechanism = settings.get("mechanism", "Laplace")

                        if "path" in settings:
                            rmse = {}
                            if "date" in attribute.lower():
                                rmse = anonymize_dates(root, {resource: {attribute: settings}}, filename)
                            elif "decimal" in attribute.lower():
                                rmse = anonymize_decimal_values(root, {resource: {attribute: settings}}, filename)

                            if rmse and attribute in rmse:
                                current_rmse = rmse[attribute]
                                rmse_results[attribute] = current_rmse
                                logging.info(f"RMSE für '{attribute}' in {filename}: {current_rmse:.4f}")

                                track_performance(
                                    iteration + 1, attribute, input_file_path, temp_output_file_path, start_time_iteration, records_processed
                                )

                                
                                parameters = settings.get("parameters", {})
                                epsilon = parameters.get("epsilon", 0.01)
                                sensitivity = parameters.get("sensitivity", 1)
                                delta = parameters.get("delta", None)

                                log_iteration_to_csv(
                                    resource, attribute, epsilon, sensitivity, delta, iteration + 1, current_rmse
                                )

                                # Check whether the RMSE is within the target range
                                if not (rmse_range[0] <= current_rmse <= rmse_range[1]):
                                    all_within_range = False
                                    adjust_parameters(settings, current_rmse, rmse_range, mechanism)
                                    logging.info(f"Adjusted parameters for '{attribute}': {settings['parameters']}")

            iteration += 1
            logging.info(f"--- Iteration {iteration} completed for file: {filename} ---")


        



        
        # Speichern der anonymisierten Datei
        tree.write(temp_output_file_path, xml_declaration=True, encoding="utf-8", method="xml")
        logging.info(f"Laplace/Gaussian abgeschlossen: {temp_output_file_path}")

    except Exception as e:
        logging.error(f"Fehler bei der Verarbeitung von Datei {filename}: {e}")
