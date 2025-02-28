import numpy as np

def calculate_tvd(original_counts, anonymized_counts):
    """
    Calculates the Total Variation Distance (TVD) between two distributions.

    :param original_counts: Dictionary with the original frequencies of the values.
    :param anonymized_counts: Dictionary with the anonymized frequencies of the values.
    :return: TVD value (float), which indicates the deviation between the two distributions.
    """
    # Combine all possible values in both distributions
    all_values = set(original_counts.keys()).union(set(anonymized_counts.keys()))
    
    # Create probability vectors for original and anonymized distribution
    original_probs = np.array([original_counts.get(value, 0) for value in all_values])
    anonymized_probs = np.array([anonymized_counts.get(value, 0) for value in all_values])
    
    # Normalize the probability distributions
    original_probs = original_probs / original_probs.sum() if original_probs.sum() > 0 else original_probs
    anonymized_probs = anonymized_probs / anonymized_probs.sum() if anonymized_probs.sum() > 0 else anonymized_probs
    
    # Calculate the Total Variation Distance
    tvd = 0.5 * np.sum(np.abs(original_probs - anonymized_probs))
    return tvd
