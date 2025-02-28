import numpy as np
import logging


# Min-max normalization function for calculating utility scores
def calculate_utility_scores(counter):
    """
    Calculates the utility scores based on the relative frequencies.

    :param counter: Dictionary or counter with frequencies of the values.
    :return: Dictionary with the relative frequencies (utility scores).
    """
    if not counter:
        logging.error("The counter object is empty. There are no values for processing.")
        raise ValueError("The counter object is empty. There are no values for processing.")

    # Calculate total sum of frequencies
    total_count = sum(counter.values())
    if total_count == 0:
        logging.error("The total number of entries is 0. Utility scores cannot be calculated.")
        raise ValueError("The total number of entries is 0.")

    # Relative proportion (probability) for each value
    utility_scores = {key: value / total_count for key, value in counter.items()}
    return utility_scores




# Function for adding Laplace noise to counters
def add_laplace_noise_to_counters(original_counters, epsilon):
    noisy_counters = {}
    sensitivity = 1
    scale = sensitivity / epsilon
    total_original = sum(original_counters.values())
    
    # 1. Add Laplace noise
    for key, count in original_counters.items():
        noise = np.random.laplace(0, scale)
        noisy_counters[key] = max(1, count + noise)

    # 2. Proportional adjustment of the difference
    total_noisy = sum(noisy_counters.values())
    if total_noisy < total_original:
        diff = total_original - total_noisy
        total_weights = sum(original_counters.values())
        for key in noisy_counters.keys():
            weight = original_counters[key] / total_weights
            noisy_counters[key] += diff * weight

    # 3. Ensure integerity
    noisy_counters = {key: int(round(value)) for key, value in noisy_counters.items()}
    return noisy_counters




# Dynamic adjustment of Epsilon based on the TVD
def adjust_epsilon_based_on_tvd(settings, tvd, tvd_range, attribute_name):
    min_tvd, max_tvd = tvd_range
    target_tvd = (min_tvd + max_tvd) / 2
    epsilon = settings.get("epsilon", 0.1)
    momentum = settings.setdefault("momentum", 0.9)
    last_adjustment = settings.setdefault("last_adjustment", 0.0)

    # Control parameters
    epsilon_min = 0.0001
    epsilon_max_change = 2.0

    # Calculate deviation
    if tvd < min_tvd:
        deviation = min_tvd - tvd
        direction = "low"
    elif tvd > max_tvd:
        deviation = tvd - max_tvd
        direction = "high"
    else:
        deviation = 0
        direction = "optimal"

    # Dynamic adjustment
    dynamic_rate = deviation / abs(target_tvd)
    dynamic_rate = min(dynamic_rate, epsilon_max_change)
    adaptive_weight = 1 + (deviation / abs(target_tvd)) if deviation > abs(target_tvd) * 0.5 else 1
    adjustment_factor = momentum * last_adjustment + (1 - momentum) * dynamic_rate * adaptive_weight
    settings["last_adjustment"] = adjustment_factor

    if direction == "high":
        epsilon *= 1 + adjustment_factor
        logging.info(f"TVD too high ({tvd:.4f}). Increase Epsilon to {epsilon:.4f} für '{attribute_name}'.")
    elif direction == "low":
        epsilon *= max(1 - adjustment_factor, 0.5)
        epsilon = max(epsilon, epsilon_min)
        logging.info(f"TVD too low ({tvd:.4f}). Reduce Epsilon to {epsilon:.4f} for '{attribute_name}'.")
    elif direction == "optimal":
        logging.info(f"TVD in the target area ({tvd:.4f}). No adjustment for '{attribute_name}'.")

    epsilon = max(min(epsilon, 1.0), epsilon_min)
    settings["epsilon"] = round(epsilon, 4)
    return settings