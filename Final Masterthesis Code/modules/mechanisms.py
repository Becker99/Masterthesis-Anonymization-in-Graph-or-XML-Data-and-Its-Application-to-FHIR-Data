import numpy as np
import random

def laplace_mechanism(value, epsilon, sensitivity):
    """
    Applies the Laplace mechanism to anonymize a value.

    :param value: Original value
    :param epsilon: Data protection parameter ε
    :param sensitivity: Sensitivity of the function
    :return: Anonymized value
    """
    noise = np.random.laplace(0, sensitivity / epsilon)
    return value + noise


def gaussian_mechanism(value, epsilon, sensitivity, delta):
    """
    Applies the Gaussian mechanism to anonymize a value.

    :param value: Original value
    :param epsilon: Data protection parameter ε
    :param sensitivity: Sensitivity of the function
    :param delta: Parameter δ for error control
    :return: Anonymized value
    """
    sigma = sensitivity * np.sqrt(2 * np.log(1.25 / delta)) / epsilon
    noise = np.random.normal(0, sigma)
    return value + noise


def exponential_mechanism_with_noisy_counters(utility_scores, counters, epsilon, root, attribute_name):
    """
    Exponential mechanism for selecting a value from a discrete set with utility scores.

    :param utility_scores: Dictionary of utility scores {key: score}
    :param counters: Dictionary of available values {key: count}
    :param epsilon: Data protection parameter ε
    :param root: Root element of the XML structure (for future extensions)
    :param attribute_name: Name of the attribute
    :return: Selected value
    """
    sensitivity = 1 
    
    while True:
        valid_counters = {key: count for key, count in counters.items() if count > 0}
        if not valid_counters:
            raise ValueError("No more valid values to select.")
        
        # Calculate exponential probabilities
        valid_utility_scores = {key: utility_scores[key] for key in valid_counters.keys()}
        exp_scores = {key: np.exp((epsilon * score) / (2 * sensitivity)) for key, score in valid_utility_scores.items()}
        total_sum = sum(exp_scores.values())
        probabilities = {key: score / total_sum for key, score in exp_scores.items()}

        # Selection of the value
        chosen_value = random.choices(list(probabilities.keys()), weights=probabilities.values(), k=1)[0]

        # Update the counter
        counters[chosen_value] -= 1
        if counters[chosen_value] == 0:
            del counters[chosen_value]  # Remove values with 0 as numerator

        return chosen_value
