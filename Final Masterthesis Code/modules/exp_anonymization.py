from modules.mechanisms import exponential_mechanism_with_noisy_counters

def anonymize_elements_modular(tree, utility_scores, counters, dynamic_epsilon, active_attributes, config):
    """
    Anonymizes the relevant elements based on the extended exponential mechanism and the configuration.

    Args:
        tree: XML tree structure.
        utility_scores (dict): Utility scores for all relevant attributes.
        counters (dict): Counter for the remaining values.
        dynamic_epsilon (dict): Dynamic \(\epsilon\)-value for each attribute.
        active_attributes (dict): Status-tracking for each attribute (True, when active).
        config (dict): Configuration file with attribute definitions.
    """
    root = tree.getroot()

    # Iterate over the configuration to anonymize all defined attributes
    for resource, attributes in config.items():
        for attr, details in attributes.items():
            if not active_attributes.get(attr, False) or not counters.get(attr):
                continue  # Skip inactive attributes or those without a counter

            # Extract the specific \(\epsilon\) value for the attribute
            epsilon = dynamic_epsilon[attr]["epsilon"]

            # Anonymization based on the attribute type
            if details["type"] == "simple":
                path = details["path"]
                for element in root.findall(path):
                    if element.text and counters[attr]:
                        new_value = exponential_mechanism_with_noisy_counters(
                            utility_scores[attr], counters[attr], epsilon, root, attr
                        )
                        element.text = str(new_value)

            elif details["type"] == "combination":
                paths = details["paths"]
                for elements in zip(*(root.findall(path) for path in paths)):
                    if all(e is not None and e.text for e in elements) and counters[attr]:
                        new_values = exponential_mechanism_with_noisy_counters(
                            utility_scores[attr], counters[attr], epsilon, root, attr
                        )
                        for elem, new_value in zip(elements, new_values):
                            elem.text = str(new_value)

            elif details["type"] == "nested":
                path = details["path"]
                filter_url = details["filter"]["url"]
                value_path = details["filter"]["value_path"]
                for item in root.findall(path):
                    url_element = item.find(".//url")
                    if url_element is not None and url_element.text == filter_url:
                        value_element = item.find(value_path)
                        if value_element is not None and value_element.text and counters[attr]:
                            new_value = exponential_mechanism_with_noisy_counters(
                                utility_scores[attr], counters[attr], epsilon, root, attr
                            )
                            value_element.text = str(new_value)

            elif details["type"] == "nested_combination":
                path = details["path"]
                filter_url = details["filter"]["url"]
                value_paths = details["filter"]["value_paths"]

                for item in root.findall(path):
                    # Apply filter
                    url_element = item.find(".//url")
                    if url_element is not None and url_element.text == filter_url:
                        # Extract the combination of values
                        combination_elements = []
                        for value_path in value_paths:
                            value_element = item.find(value_path)
                            if value_element is not None and value_element.text:
                                combination_elements.append(value_element)
                        if len(combination_elements) == len(value_paths) and counters[attr]:
                            # Calculate new values
                            new_values = exponential_mechanism_with_noisy_counters(
                                utility_scores[attr], counters[attr], epsilon, root, attr
                            )
                            for elem, new_value in zip(combination_elements, new_values):
                                elem.text = str(new_value)
