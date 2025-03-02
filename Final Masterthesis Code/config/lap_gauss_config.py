lap_gauss_config_file = {
    "AllergyIntolerance": {
        "recordedDate": {
            "path": ".//recordedDate",
            "mechanism": "Laplace",
            "rmse_range": [5, 10]
        }
    },
    "Condition": {
        "onsetDateTime": {
            "path": ".//onsetDateTime",
            "mechanism": "Laplace",
            "rmse_range": [5, 10]
        },
        "recordedDate": {
            "path": ".//recordedDate",
            "mechanism": "Laplace",
            "rmse_range": [5, 10]
        },
        "abatementDateTime": {
            "path": ".//abatementDateTime",
            "mechanism": "Laplace",
            "rmse_range": [5, 10]
        }
    },
    "Device": {
        "manufactureDate": {
            "path": ".//manufactureDate",
            "mechanism": "Laplace",
            "rmse_range": [5, 10]
        },
        "expirationDate": {
            "path": ".//expirationDate",
            "mechanism": "Laplace",
            "rmse_range": [5, 10]
        }
    },
    "DiagnosticReport": {
        "effectiveDateTime": {
            "path": ".//effectiveDateTime",
            "mechanism": "Laplace",
            "rmse_range": [5, 10]
        }
    },
    "DocumentReference": {
        "date": {
            "path": ".//date",
            "mechanism": "Laplace",
            "rmse_range": [5, 10]
        }
    },
    "Immunization": {
        "occurrenceDateTime": {
            "path": ".//occurrenceDateTime",
            "mechanism": "Laplace",
            "rmse_range": [5, 10]
        }
    },
    "Observation": {
        "effectiveDateTime": {
            "path": ".//effectiveDateTime",
            "mechanism": "Laplace",
            "rmse_range": [5, 10]
        }
    },
    "Patient": {
        "extension.valueDecimal": {
            "path": ".//extension/item/valueDecimal",
            "mechanism": "Laplace",
            "rmse_range": [1000, 1050]
        },
        "birthDate": {
            "path": ".//birthDate",
            "mechanism": "Laplace",
            "rmse_range": [50, 100]  
        },
        "deceasedDateTime": {
            "path": ".//deceasedDateTime",
            "mechanism": "Laplace",
            "rmse_range": [50, 100]  
        }
    }
}
