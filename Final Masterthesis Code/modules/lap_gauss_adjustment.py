import logging
from datetime import datetime, timezone
from dateutil import parser 

def adjust_parameters(settings, rmse, rmse_range, mechanism):
    """
    Dynamic and adaptive adjustment of the parameters (epsilon, delta, sensitivity) based on the RMSE.
    
    Improvements:
        - Use of momentum to stabilize the learning rate.
        - Dynamic adjustment of the learning rate based on the RMSE deviation.
    
    Goal:
        - To reach the RMSE range as efficiently as possible.
    """
    min_rmse, max_rmse = min(rmse_range), max(rmse_range)

    # Load parameters
    parameters = settings.get("parameters", {})
    epsilon = parameters.get("epsilon", 0.1)
    sensitivity = parameters.get("sensitivity", 1)
    delta = parameters.get("delta", 1e-5) if mechanism == "Gaussian" else None

    # Initialize momentum
    settings.setdefault("momentum", 0.9)
    settings.setdefault("last_adjustment", 0)
    momentum = settings["momentum"]

    # Calculate RMSE deviation
    if rmse < min_rmse:
        deviation = min_rmse - rmse
        direction = "low"
    elif rmse > max_rmse:
        deviation = rmse - max_rmse
        direction = "high"
    else:
        deviation = 0
        direction = "optimal"

    # Dynamic learning rate
    dynamic_rate = deviation / (max_rmse if direction == "high" else min_rmse)
    dynamic_rate = min(dynamic_rate, 2)

    # Combination of momentum and learning rate
    adjustment_factor = momentum * settings["last_adjustment"] + (1 - momentum) * dynamic_rate
    settings["last_adjustment"] = adjustment_factor

    # Parameter adjustment
    if direction == "high":
        epsilon *= 1 + adjustment_factor
        logging.info(f"RMSE ({rmse}) > target range ({min_rmse}, {max_rmse}). Increase epsilon: {epsilon:.4f}")
    elif direction == "low":
        epsilon *= max(1 - adjustment_factor, 0.5)
        epsilon = max(epsilon, 0.0001)
        logging.info(f"RMSE ({rmse}) < target range ({min_rmse}, {max_rmse}). Decrease epsilon: {epsilon:.4f}")

    if epsilon >= sensitivity:
        sensitivity *= 1 + min(dynamic_rate, 0.5)
        logging.info(f"Epsilon >= Sensitivity recognized. Increase sensitivity: {sensitivity:.4f}")

    if mechanism == "Gaussian":
        if direction == "high":
            delta *= 1 + min(dynamic_rate, 0.5)
        elif direction == "low":
            delta *= max(1 - dynamic_rate, 0.5)
        logging.info(f"Update delta: {delta:.7f}")

    if direction == "optimal":
        logging.info(f"RMSE ({rmse}) in target range ({min_rmse}, {max_rmse}). No adjustment necessary.")

    settings["parameters"] = {
        "epsilon": round(epsilon, 4),
        "sensitivity": round(sensitivity, 4),
        "delta": round(delta, 7) if mechanism == "Gaussian" else None
    }
    logging.info(f"Updated Parameter: {settings['parameters']}")

def calculate_dynamic_sensitivity(root, config, filename):
    """
    Dynamically calculates the sensitivity for each attribute in the configuration,
    based on the minimum and maximum values in the data set.

    :param root: Root element of the XML document.
    :param config: Configuration with attributes.
    :param filename: Name of the file being processed.
    :return: Updated configuration with calculated sensitivity.
    """

    def normalize_sensitivity(value, min_value, max_value):
        """
        Normalizes a value to the range [1, 5].
        :param value: The value to be normalized.
        :param min_value: Minimum value of the range.
        :param max_value: Maximum value of the range.
        :return: Normalized value between 1 and 5.
        """
        if max_value == min_value:
            return 1  
        return 1 + 4 * ((value - min_value) / (max_value - min_value))

    for resource, attributes in config.items():
        if resource.lower() in filename.lower():
            for attribute, settings in attributes.items():
                if "path" in settings:
                    path = settings["path"]
                    values = []

                    for element in root.findall(path):
                        value = element.text
                        if value:
                            try:
                                # Check whether the attribute is a date field
                                if any(kw in attribute.lower() for kw in ["date", "start", "end", "issued"]):
                                    # Convert date to number of days since Unix epoch
                                    date_value = datetime.fromisoformat(value)
                                    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
                                    days_since_epoch = (date_value - epoch).total_seconds() / 86400  # Umrechnung in Tage
                                    values.append(days_since_epoch)
                                else:
                                    # For other numerical values
                                    values.append(float(value))
                            except Exception as e:
                                logging.warning(f"Errors when processing {attribute}: {e}")

                    if values:
                        # Calculate the sensitivity
                        raw_sensitivity = max(values) - min(values)

                        # Normalize the sensitivity to the range [1, 5]
                        normalized_sensitivity = normalize_sensitivity(raw_sensitivity, min(values), max(values))

                        if "parameters" not in settings:
                            settings["parameters"] = {"epsilon": 0.01, "sensitivity": 1, "delta": 1e-5}
                        settings["parameters"]["sensitivity"] = normalized_sensitivity
                        logging.info(f"Sensitivity for {attribute} in {filename}: {normalized_sensitivity:.4f}")

    return config

