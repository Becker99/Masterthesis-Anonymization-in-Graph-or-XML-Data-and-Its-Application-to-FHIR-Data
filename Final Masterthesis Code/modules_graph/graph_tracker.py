import time
import psutil
import os
import networkx as nx

class GraphTracker:
    def __init__(self, graph):
        self.graph = graph
        self.tracking_log = []

    def track_performance(self, operation, func, *args, **kwargs):
        start_time = time.perf_counter_ns()  
        
        
        result = func(*args, **kwargs)

        end_time = time.perf_counter_ns()  
       
        exec_time = (end_time - start_time) / 1_000_000  
        

        self.tracking_log.append({
            "operation": operation,
            "execution_time_ms": exec_time
        })

        print(f"📊 {operation}: time = {exec_time:.6f}ms")

        return result


    def patch_graph_methods(self):

        self.graph.add_edge = lambda u, v, **attr: self.track_performance("add_edge", nx.Graph.add_edge, self.graph, u, v, **attr)
        self.graph.remove_edge = lambda u, v: self.track_performance("remove_edge", nx.Graph.remove_edge, self.graph, u, v)
        self.graph.add_node = lambda node, **attr: self.track_performance("add_node", nx.Graph.add_node, self.graph, node, **attr)
        self.graph.remove_node = lambda node: self.track_performance("remove_node", nx.Graph.remove_node, self.graph, node)

    def save_tracking_log(self, filepath="performance_tracking.csv"):
        import pandas as pd
        df = pd.DataFrame(self.tracking_log)
        df.to_csv(filepath, index=False)
        print(f"Performance Data saved in {filepath}")
