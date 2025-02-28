from datetime import datetime, timezone, timedelta
from modules.mechanisms import laplace_mechanism, gaussian_mechanism
from modules.rmse import calculate_rmse_date, calculate_rmse_decimal

def anonymize_decimal_values(root, config, filename):
    """
    Anonymizes decimal values (e.g. 'valueDecimal') in an XML document based on the configuration.
    :param root: Root element of the XML tree
    :param config: Configuration with attributes whose anonymization is adjusted
    :param filename: Name of the file that is anonymized
    :return: RMSE results for the anonymized decimal values
    """
    original_values = {}
    anonymized_values = {}

    # Iterate through all resources and their attributes in the configuration
    for resource, attributes in config.items():
        if resource.lower() in filename.lower():
            for attribute, settings in attributes.items():
                if 'path' in settings and "decimal" in attribute.lower():
                    path = settings["path"]
                    mechanism = settings.get("mechanism")
                    parameters = settings.get("parameters", {"epsilon": 0.01, "sensitivity": 1, "delta": 1e-5})

                    epsilon = parameters.get("epsilon", 0.01)
                    sensitivity = parameters.get("sensitivity", 1)
                    delta = parameters.get("delta", 1e-5)

                    if mechanism is None:
                        raise ValueError(f"No mechanism {attribute} specified in the configuration")

                    for i, element in enumerate(root.findall(path)):
                        original_value = element.text
                        if original_value:
                            try:
                                original_value_float = float(original_value)

                                # Anonymisierung basierend auf Mechanismus
                                if mechanism == "Laplace":
                                    anonymized_value = laplace_mechanism(original_value_float, epsilon, sensitivity)
                                elif mechanism == "Gaussian":
                                    anonymized_value = gaussian_mechanism(original_value_float, epsilon, sensitivity, delta)
                                else:
                                    raise ValueError(f"Unknown mechanism: {mechanism}")

                                element.text = str(anonymized_value)

                                # Save values for RMSE calculation
                                attribute_key = f"{attribute}_{i}"
                                original_values[attribute_key] = original_value_float
                                anonymized_values[attribute_key] = anonymized_value
                            except ValueError as e:
                                print(f"Errors in the anonymization of {attribute}: {e}")
                                continue
                            except Exception as e:
                                print(f"Unknown error in the anonymization of {attribute}: {e}")
                                continue

    # Calculate RMSE
    if original_values and anonymized_values:
        rmse_results = calculate_rmse_decimal(original_values, anonymized_values)
    else:
        rmse_results = {}

    if rmse_results:
        print(f"RMSE results for {filename}: {rmse_results}")
    return rmse_results


def anonymize_dates(root, config, filename):
    """
    Anonymizes all relevant date fields in an XML document based on the configuration.

    :param root: Root element of the XML tree
    :param config: Configuration with attributes whose anonymization is adjusted
    :param filename: Name of the file that is anonymized
    :return: Dictionary with RMSE values of the anonymized attributes.
    """
    original_values = {}
    anonymized_values = {}

    for resource, attributes in config.items():
        if resource.lower() in filename.lower():
            for attribute, settings in attributes.items():
                if 'path' in settings and any(x in attribute.lower() for x in ['date', 'start', 'end', 'issued']):
                    path = settings["path"]
                    mechanism = settings["mechanism"]
                    parameters = settings.get("parameters", {"epsilon": 0.01, "sensitivity": 1, "delta": 1e-7})

                    if mechanism is None:
                        raise ValueError(f"No mechanism for {attribute} specified in the configuration")

                    for element in root.findall(path):
                        original_value = element.text
                        if original_value:
                            try:
                                original_value_datetime = datetime.fromisoformat(original_value)

                                # Anonymization of date values
                                epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
                                days_since_epoch = (original_value_datetime - epoch).days

                                if mechanism == "Laplace":
                                    anonymized_days = laplace_mechanism(days_since_epoch, parameters["epsilon"], parameters["sensitivity"])
                                elif mechanism == "Gaussian":
                                    anonymized_days = gaussian_mechanism(days_since_epoch, parameters["epsilon"], parameters["sensitivity"], parameters["delta"])
                                else:
                                    raise ValueError(f"Unknown mechanism: {mechanism}")

                                anonymized_datetime = epoch + timedelta(days=anonymized_days)

                                if original_value_datetime.tzinfo:
                                    anonymized_datetime = anonymized_datetime.replace(tzinfo=original_value_datetime.tzinfo)
                                else:
                                    anonymized_datetime = anonymized_datetime.replace(tzinfo=timezone.utc)

                                element.text = anonymized_datetime.replace(microsecond=0).isoformat()

                                # Collect values for RMSE
                                if attribute not in original_values:
                                    original_values[attribute] = []
                                    anonymized_values[attribute] = []

                                original_values[attribute].append(original_value)
                                anonymized_values[attribute].append(element.text)
                            except Exception as e:
                                print(f"Errors in the anonymization of {attribute}: {e}")
                                continue

    # Calculate RMSE
    rmse_results = {}
    for attribute, original_list in original_values.items():
        anonymized_list = anonymized_values[attribute]
        if original_list and anonymized_list:
            rmse = calculate_rmse_date(
                {f"{attribute}_{i}": original for i, original in enumerate(original_list)},
                {f"{attribute}_{i}": anonymized for i, anonymized in enumerate(anonymized_list)},
            )
            if rmse and attribute in rmse:
                rmse_results[attribute] = rmse[attribute]
                print(f"RMSE for {attribute} in {filename}: {rmse}")

    return rmse_results
