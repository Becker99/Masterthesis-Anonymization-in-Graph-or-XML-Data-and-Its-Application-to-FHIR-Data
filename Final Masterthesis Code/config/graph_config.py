# Dynamically generated configuration
graph_config = {
    'AllergyIntolerance': {
        'Patient': 'references to AllergyIntolerance',
    },
    'Condition': {
        'Encounter': 'references to Condition',
        'Patient': 'references to Condition',
    },
    'Device': {
        'Patient': 'references to Device',
    },
    'DiagnosticReport': {
        'Encounter': 'references to DiagnosticReport',
        'Observation': 'references to DiagnosticReport',
        'Organization': 'Organization',
        'Patient': 'references to DiagnosticReport',
        'Practitioner': 'Practitioner',
    },
    'DocumentReference': {
        'Encounter': 'references to DocumentReference',
        'Organization': 'Organization',
        'Patient': 'references to DocumentReference',
        'Practitioner': 'Practitioner',
    },
    'Encounter': {
        'Location': 'Location',
        'Organization': 'Organization',
        'Patient': 'references to Encounter',
        'Practitioner': 'Practitioner',
    },
    'Immunization': {
        'Encounter': 'references to Immunization',
        'Location': 'Location',
        'Patient': 'references to Immunization',
    },
    'MedicationRequest': {
        'Condition': 'references to MedicationRequest',
        'Encounter': 'references to MedicationRequest',
        'Patient': 'references to MedicationRequest',
        'Practitioner': 'Practitioner',
    },
    'Observation': {
        'Encounter': 'references to Observation',
        'Patient': 'references to Observation',
    },
    'Procedure': {
        'Condition': 'references to Procedure',
        'Encounter': 'references to Procedure',
        'Location': 'Location',
        'Patient': 'references to Procedure',
    },
}
