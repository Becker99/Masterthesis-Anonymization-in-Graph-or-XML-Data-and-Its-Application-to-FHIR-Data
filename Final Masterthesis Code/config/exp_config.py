exponential_config_file= {
    "Immunization": {
        "location": {
            "type": "simple", 
            "path": ".//location/display",  
            "tvd_range": [0.1, 0.4]
        }
    }
    ,
    "Encounter": {
        "location": {
            "type": "simple",
            "path": ".//location/item/location/display",
            "tvd_range": [0.1, 0.4]
        },
        "serviceProvider": {
            "type": "simple",
            "path": ".//serviceProvider/display",
            "tvd_range": [0.1, 0.4]
        }
    },
    "Procedure": {
        "location": {
            "type": "simple",
            "path": ".//location/display",
            "tvd_range": [0.1, 0.4]
        }
    },
    "Patient": {
        "gender": {
            "type": "simple",
            "path": ".//gender",
            "tvd_range": [0.1, 0.4]
        },
        "maritalStatus_combinations": {
            "type": "combination",
            "paths": [
                ".//maritalStatus/coding/item/code",
                ".//maritalStatus/coding/item/display",
                ".//maritalStatus/text"
            ],
            "tvd_range": [0.1, 0.4]
        },
        "address_combinations": {
            "type": "combination",
            "paths": [
                ".//address/item/city",
                ".//address/item/state",
                ".//address/item/country"
            ],
            "tvd_range": [0.1, 0.4]
        }
        ,
        "race": {
            "type": "nested_combination",
            "path": ".//extension/item",
            "filter": {
                "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race",
                "value_paths": [
                    ".//valueCoding/code",
                    ".//valueCoding/display",
                    ".//valueString"
                ]
            },
            "tvd_range": [0.1, 0.4]
        },
        "ethnicity": {
            "type": "nested_combination",
            "path": ".//extension/item",
            "filter": {
                "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity",
                "value_paths": [
                    ".//extension/item/valueCoding/code",
                    ".//extension/item/valueCoding/display",
                    ".//extension/item/valueString"
                ]
            },
            "tvd_range": [0.1, 0.4]
        },
        "birthsex": {
            "type": "nested",
            "path": ".//extension/item",
            "filter": {
                "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex",
                "value_path": ".//valueCode"
            },
            "tvd_range": [0.1, 0.4]
        },
        "multipleBirthInteger": {
            "type": "simple",
            "path": ".//multipleBirthInteger",
            "tvd_range": [0.1, 0.4]
        },
        "communication_combinations": {
            "type": "combination",
            "paths": [
                ".//communication/item/language/coding/item/code",
                ".//communication/item/language/coding/item/display",
                ".//communication/item/language/text"
            ],
            "tvd_range": [0.1, 0.4]
        }
    },
    "DiagnosticReport": {
        "code_triplets": {
            "type": "combination",
            "paths": [
                ".//coding/item/code",
                ".//coding/item/display",
                ".//text"
            ],
            "tvd_range": [0.1, 0.4]
        },
        "performer": {
            "type": "simple",
            "path": ".//performer/item/display",
            "tvd_range": [0.1, 0.4]
        }
    },
    "DocumentReference": {
        "custodian": {
            "type": "simple",
            "path": ".//custodian/display",
            "tvd_range": [0.1, 0.4]
        }
    }
}
