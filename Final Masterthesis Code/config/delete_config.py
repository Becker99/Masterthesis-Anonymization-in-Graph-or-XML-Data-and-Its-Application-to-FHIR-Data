# Configuration file for the attributes to be deleted
delete_config_file = {
    "Patient": {
        "record_paths": [
            {"path": ".//address/item/extension"},
            {"path": ".//address/item/line"},
            {"path": ".//address/item/postalCode"}
        ]
    }
}


