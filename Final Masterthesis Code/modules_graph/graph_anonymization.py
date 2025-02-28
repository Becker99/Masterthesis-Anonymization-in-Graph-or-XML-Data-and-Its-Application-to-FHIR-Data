import numpy as np

import os
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

project_dir = os.path.abspath(os.path.join(BASE_DIR, ".."))
sys.path.append(project_dir)
os.chdir(project_dir)

from config.graph_metric_config import GRAPH_METRIC_CONFIG

from adjustment_metrics import adjust_graph_to_target_metrics, calculate_graph_metrics, update_metric_config


def anonymize_graph(graph, xml_root, epsilon, sensitivity, original_metrics=None):
    """
    Anonymizes the graph based on differential privacy and target metrics.

    Args:
        graph (nx.Graph): The original graph that is directly customized.
        xml_root (xml.ElementTree.Element): The XML root of the graph.
        epsilon (float or dict): The privacy parameter for differential privacy. 
                                 Can be global or specific to each metric.
        sensitivity (float or dict): The sensitivity of the metrics.
                                     Can be global or specific to each metric.
        original_metrics (dict, optional): Already calculated original metrics of the graph. 
                                        If None, they will be recalculated.

    Returns:
        tuple: The adjusted graph and the updated noisy target metrics.
    """
    print("Starting to anonymize the graph...")

    # 1. check or calculate original metrics
    if original_metrics is None:
        print("Calculate original metrics for the graph...")
        original_metrics = calculate_graph_metrics(graph)
    else:
        print("Original metrics have already been calculated and handed .")

    # Output original metrics
    print("\nOriginal metrics:")
    for metric, value in original_metrics.items():
        if value is not None:
            print(f"  {metric}: {value:.4f}")
        else:
            print(f"  {metric}: None")

    # 2. generate noisy target metrics
    noised_metrics = {}
    for metric, value in original_metrics.items():
        if value is not None:  # Only metrics with calculated values
            # Extract specific epsilon and sensitivity values for the metric
            metric_epsilon = epsilon.get(metric, 1.0) if isinstance(epsilon, dict) else epsilon
            metric_sensitivity = sensitivity.get(metric, 1.0) if isinstance(sensitivity, dict) else sensitivity

            if metric == "clustering_coefficient":
                # Special treatment for the clustering coefficient
                scale_factor = 1000  # Scale factor
                scaled_value = value * scale_factor
                noise = np.random.laplace(0, metric_sensitivity / metric_epsilon)
                scaled_noised_value = max(0, scaled_value + noise)  # Avoid negative values
                noised_metrics[metric] = scaled_noised_value / scale_factor
                print(f"Noisy target for {metric}: {noised_metrics[metric]:.4f} "
                      f"(Original: {value:.4f}, Scaled: {scaled_value:.4f}, Noise: {noise:.4f}, "
                      f"Epsilon: {metric_epsilon}, Sensitivity: {metric_sensitivity})")
            elif metric == "degree_centrality":
                scale = metric_sensitivity / metric_epsilon
                max_noise = 5
                noise = np.random.laplace(0, scale)
                noise = max(-max_noise, min(noise, max_noise))  # Limit the noise
                noised_metrics[metric] = max(0, value + noise)  # Avoid negative values
                print(f"Noisy target for {metric}: {noised_metrics[metric]:.4f} "
                    f"(Original: {value:.4f}, Noise: {noise:.4f}, Epsilon: {metric_epsilon}, Sensitivity: {metric_sensitivity})")
            
            else:
                # Standard noise calculation for other metrics
                noise = np.random.laplace(0, metric_sensitivity / metric_epsilon)
                noised_metrics[metric] = max(0, value + noise)  
                print(f"Noisy target for {metric}: {noised_metrics[metric]:.4f} "
                      f"(Original: {value:.4f}, Noise: {noise:.4f}, Epsilon: {metric_epsilon}, Sensitivity: {metric_sensitivity})")

    #3. Aktualisieren Sie die Konfiguration der Diagrammmetriken
    update_metric_config(noised_metrics)
    print("\nGraph metrics configuration updated.:")
    for metric, config in GRAPH_METRIC_CONFIG.items():
        if config["target_value"] is not None:
            print(f"  {metric}: Target value={config['target_value']:.4f}, "
                  f"Tolerance=[{config['min_value']:.4f}, {config['max_value']:.4f}]")
        else:
            print(f"  {metric}: None (no update necessary)")

    #4. Customize the graph to the target metrics
    adjusted_graph = adjust_graph_to_target_metrics(graph, xml_root, epsilon, sensitivity)

    print("Anonymization completed.")
    return adjusted_graph, noised_metrics

