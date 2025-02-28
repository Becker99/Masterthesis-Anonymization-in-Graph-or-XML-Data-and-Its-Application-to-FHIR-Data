# Masterproject_Anonymization_of_XML_Graph_FHIR_Data


**Anonymization in Graph or XML Data and Its Application to FHIR Data**  
This Master's Thesis investigates the application of Differential Privacy (DP) techniques to FHIR data, focusing on both XML-based and graph-based data structures. The study develops and evaluates three specialized anonymization algorithms:  
- A numerical approach employing Laplace/Gaussian mechanisms with an iterative adjustment of privacy parameters based on the Root Mean Square Error (RMSE).  
- A categorical approach that utilizes the exponential mechanism, with dynamic parameter adaptation guided by the Total Variation Distance (TVD) to preserve the original data distribution.  
- A graph-based approach in which Laplace noise is applied to key graph metrics, with subsequent iterative modifications ensuring that the structural integrity of the network is maintained.

## Installation and Setup

This project has been developed using Python 3.11.4. To ensure a reproducible and isolated environment, it is recommended to use a virtual environment. Follow these steps to set up the project:

1. **Clone the Repository**  
   Clone the project repository to your local machine.

2. **Install Dependencies**  
   pip install -r requirements.txt



### Key Components

- **`main.py`**  
  This script runs Algorithms 1 and 2, which focus on numerical and categorical data anonymization.  
  - **Algorithm 1 (Laplace/Gaussian Mechanism)**: Anonymizes numerical attributes (e.g., dates, measurement values) with iterative feedback based on RMSE.  
  - **Algorithm 2 (Exponential Mechanism)**: Anonymizes categorical attributes (e.g., gender, marital status) with iterative feedback using TVD.

- **`modules_graph/main_graph.py`**  
  This script runs Algorithm 3, which handles the graph-based anonymization. It takes the output from `main.py` (i.e., the anonymized dataset) and applies Laplace noise to key graph metrics, subsequently adjusting the graph structure to preserve essential properties (e.g., degree distribution, clustering coefficients).

- **`config/`**  
  Contains configuration files (e.g., `exp_config.py`, `lap_gauss_config.py`, `graph_metric_config.py`, etc.) that define parameters for the respective algorithms, such as target ranges for RMSE or TVD, attributes (path etc.), tolerance values for graph metrics.

- **`modules_graph/`**  
  Holds Python modules specific to the graph anonymization approach. This includes helper functions for building, tracking, and anonymizing graph structures, as well as generating dummy values for nodes or edges.

- **`data/`**  
  Intended to store input datasets (FHIR XML/JSON files) and possibly intermediate outputs. Due to storage limits only the small dataset of 10 Patients is here.
  To get access to the bigger datasets use: https://github.com/smart-on-fhir/sample-bulk-fhir-datasets


### Execution Flow

1. **Run `main.py`**  
   - Executes Algorithms 1 and 2 for anonymizing numerical and categorical FHIR data.  
   - Produces an anonymized dataset in XML format.

2. **Run `modules_graph/main_graph.py`**  
   - Uses the anonymized output from `main.py` to construct and anonymize a graph representation (Algorithm 3).  
   - Generates a final anonymized graph and updated XML data, reflecting any changes in references or relationships.

This modular design facilitates incremental anonymization: first at the attribute level (numerical and categorical), followed by the structural level (graph). It ensures that each stage can be verified and evaluated independently before proceeding to the next phase.
