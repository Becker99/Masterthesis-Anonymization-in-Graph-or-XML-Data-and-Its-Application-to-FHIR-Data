import numpy as np
from datetime import datetime, timezone
import logging

def calculate_rmse_date(original_values, anonymized_values):
    """
    Calculates the aggregated RMSE (mean value across all entries) for date values of an attribute in days.

    :param original_values: Dictionary with original date values
    :param anonymized_values: Dictionary with anonymized date values
    :return: Dictionary with attribute names and aggregated RMSE values
    """
    if set(original_values.keys()) != set(anonymized_values.keys()):
        print("Original and anonymized values have different keys.")
        return {}

    rmse_results = {}
    attribute_differences = {}

    # Function to parse dates flexibly
    def parse_date(date_str):
        try:
            if "T" in date_str:  # ISO-Format 
                return datetime.fromisoformat(date_str)
            else:  # Format YYYY-MM-DD 
                return datetime.strptime(date_str, "%Y-%m-%d")
        except Exception as e:
            print(f"Error parsing date {date_str}: {e}")
            return None

    # Iterate through all keys and values in original_values
    for tag, original_value in original_values.items():
        try:
            original_date = parse_date(original_value)
            anonymized_date = parse_date(anonymized_values[tag])

            if original_date and anonymized_date:
                # Calculate the difference in days
                difference = (original_date - anonymized_date).total_seconds() / 86400

                # Extract the attribute name
                attribute_name = tag.split("_")[0]
                if attribute_name not in attribute_differences:
                    attribute_differences[attribute_name] = []
                attribute_differences[attribute_name].append(difference)
        except Exception as e:
            print(f"Errors in the processing of {tag}: {e}")
            continue

    # Calculate the RMSE for each attribute
    for attribute_name, differences in attribute_differences.items():
        if differences:
            squared_sum = sum(diff ** 2 for diff in differences)
            count = len(differences)
            rmse = np.sqrt(squared_sum / count)
            rmse_results[attribute_name] = round(rmse, 4)

    logging.info(f"Calculated RMSE values: {rmse_results}")
    return rmse_results


def calculate_rmse_decimal(original_values, anonymized_values):
    """
    Calculates the aggregated RMSE (mean value across all entries) for anonymized decimal values.

    :param original_values: Dictionary with the original decimal values
    :param anonymized_values: Dictionary with the anonymized decimal values
    :return: Dictionary with attribute names and aggregated RMSE values
    """
    if set(original_values.keys()) != set(anonymized_values.keys()):
        print("Original and anonymized values have different keys.")
        return {}

    rmse_results = {}
    attribute_differences = {}

    # Iterate through all attributes
    for attribute, original_value in original_values.items():
        try:
            difference = original_value - anonymized_values[attribute]

            # Group differences by attribute name
            attribute_name = attribute.split("_")[0]
            if attribute_name not in attribute_differences:
                attribute_differences[attribute_name] = []
            attribute_differences[attribute_name].append(difference)
        except Exception as e:
            print(f"Errors in the processing of {attribute}: {e}")
            continue

    # Calculate the RMSE for each attribute
    for attribute_name, differences in attribute_differences.items():
        if differences:
            squared_sum = sum(diff ** 2 for diff in differences)
            count = len(differences)
            rmse = np.sqrt(squared_sum / count)
            rmse_results[attribute_name] = round(rmse, 4)

    logging.info(f"Calculated RMSE values: {rmse_results}")
    return rmse_results
