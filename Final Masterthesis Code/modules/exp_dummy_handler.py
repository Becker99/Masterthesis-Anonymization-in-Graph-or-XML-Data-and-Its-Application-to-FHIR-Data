import math

def calculate_dummy_counter(existing_counts):
    """
    Calculates the counter value for the dummy value based on 50% of the average.

    :param existing_counts: A counter object with the frequencies of the original values.
    :return: A proportional counter value for the dummy value.
    """
    if not existing_counts:
        raise ValueError("The existing distribution must not be empty.")

    # Calculate the sum and the average of the frequencies
    total_count = sum(existing_counts.values())
    avg_count = total_count / len(existing_counts)

    # Set the dummy counter to 50% of the average (rounded up)
    dummy_counter = math.ceil(avg_count * 0.1)
    return dummy_counter


def create_dummy_value_for_attribute(attribute_details):
    """
    Creates a dummy value based on the type of attribute.

    :param attribute_details: Dictionary with details of the attribute from the configuration.
    :return: The dummy value (as a single value, tuple or list depending on the type).
    """
    attr_type = attribute_details.get("type")
    
    if attr_type == "simple":
        # Simple type: Only one value (e.g. gender)
        return "unspecified"
    
    elif attr_type == "combination":
        # Combination: List of values for different paths
        paths = attribute_details.get("paths", [])
        return tuple("unspecified" for _ in paths)
    
    elif attr_type == "nested":
        # Nested: Specific value for the nested path
        return "unspecified"
    
    elif attr_type == "nested_combination":
        # Nested combination: List of values for nested paths
        value_paths = attribute_details.get("filter", {}).get("value_paths", [])
        return tuple("unspecified" for _ in value_paths)
    
    else:
        raise ValueError(f"Unknown attribute type: {attr_type}")


def add_dummy_to_pool(attribute_name, attribute_details, counters):
    """
    Adds dummy values for an attribute to the pool and sets the counter proportionally.

    :param attribute_name: Name of the attribute.
    :param attribute_details: Dictionary with details of the attribute.
    :param counters: Dictionary with frequencies of the values.
    :return: Updated counter dictionary with dummy value.
    """
    dummy_value = create_dummy_value_for_attribute(attribute_details)
    
    if attribute_name not in counters:
        counters[attribute_name] = {}

    # Calculate the dummy counter proportionally (50% of the average)
    existing_counts = counters[attribute_name]
    dummy_counter = calculate_dummy_counter(existing_counts)

    # Add the dummy value
    if dummy_value in existing_counts:
        existing_counts[dummy_value] += dummy_counter
    else:
        existing_counts[dummy_value] = dummy_counter
    
    return counters

