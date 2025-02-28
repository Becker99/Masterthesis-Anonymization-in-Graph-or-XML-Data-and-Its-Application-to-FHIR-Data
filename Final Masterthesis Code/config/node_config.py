# Dynamically generated configuration file
NODE_CONFIG = {
    "AllergyIntolerance": {
        "resourceType": {
            "is_leaf": True
        },
        "id": {
            "is_leaf": True
        },
        "meta": {
            "is_leaf": False,
            "children": {
                "profile": {
                    "is_leaf": False,
                    "children": {
                        "item": {
                            "is_leaf": True
                        }
                    }
                }
            }
        },
        "clinicalStatus": {
            "is_leaf": False,
            "children": {
                "coding": {
                    "is_leaf": False,
                    "children": {
                        "item": {
                            "is_leaf": False,
                            "children": {
                                "system": {
                                    "is_leaf": True
                                },
                                "code": {
                                    "is_leaf": True
                                }
                            }
                        }
                    }
                }
            }
        },
        "verificationStatus": {
            "is_leaf": False,
            "children": {
                "coding": {
                    "is_leaf": False,
                    "children": {
                        "item": {
                            "is_leaf": False,
                            "children": {
                                "system": {
                                    "is_leaf": True
                                },
                                "code": {
                                    "is_leaf": True
                                }
                            }
                        }
                    }
                }
            }
        },
        "type": {
            "is_leaf": True
        },
        "category": {
            "is_leaf": False,
            "children": {
                "item": {
                    "is_leaf": True
                }
            }
        },
        "criticality": {
            "is_leaf": True
        },
        "code": {
            "is_leaf": False,
            "children": {
                "coding": {
                    "is_leaf": False,
                    "children": {
                        "item": {
                            "is_leaf": False,
                            "children": {
                                "system": {
                                    "is_leaf": True
                                },
                                "code": {
                                    "is_leaf": True
                                },
                                "display": {
                                    "is_leaf": True
                                }
                            }
                        }
                    }
                },
                "text": {
                    "is_leaf": True
                }
            }
        },
        "patient": {
            "is_leaf": False,
            "children": {
                "reference": {
                    "is_leaf": True
                }
            }
        },
        "recordedDate": {
            "is_leaf": True
        }
    },
    "Condition": {
        "resourceType": {
            "is_leaf": True
        },
        "id": {
            "is_leaf": True
        },
        "meta": {
            "is_leaf": False,
            "children": {
                "profile": {
                    "is_leaf": False,
                    "children": {
                        "item": {
                            "is_leaf": True
                        }
                    }
                }
            }
        },
        "clinicalStatus": {
            "is_leaf": False,
            "children": {
                "coding": {
                    "is_leaf": False,
                    "children": {
                        "item": {
                            "is_leaf": False,
                            "children": {
                                "system": {
                                    "is_leaf": True
                                },
                                "code": {
                                    "is_leaf": True
                                }
                            }
                        }
                    }
                }
            }
        },
        "verificationStatus": {
            "is_leaf": False,
            "children": {
                "coding": {
                    "is_leaf": False,
                    "children": {
                        "item": {
                            "is_leaf": False,
                            "children": {
                                "system": {
                                    "is_leaf": True
                                },
                                "code": {
                                    "is_leaf": True
                                }
                            }
                        }
                    }
                }
            }
        },
        "category": {
            "is_leaf": False,
            "children": {
                "item": {
                    "is_leaf": False,
                    "children": {
                        "coding": {
                            "is_leaf": False,
                            "children": {
                                "item": {
                                    "is_leaf": False,
                                    "children": {
                                        "system": {
                                            "is_leaf": True
                                        },
                                        "code": {
                                            "is_leaf": True
                                        },
                                        "display": {
                                            "is_leaf": True
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "code": {
            "is_leaf": False,
            "children": {
                "coding": {
                    "is_leaf": False,
                    "children": {
                        "item": {
                            "is_leaf": False,
                            "children": {
                                "system": {
                                    "is_leaf": True
                                },
                                "code": {
                                    "is_leaf": True
                                },
                                "display": {
                                    "is_leaf": True
                                }
                            }
                        }
                    }
                },
                "text": {
                    "is_leaf": True
                }
            }
        },
        "subject": {
            "is_leaf": False,
            "children": {
                "reference": {
                    "is_leaf": True
                }
            }
        },
        "encounter": {
            "is_leaf": False,
            "children": {
                "reference": {
                    "is_leaf": True
                }
            }
        },
        "onsetDateTime": {
            "is_leaf": True
        },
        "recordedDate": {
            "is_leaf": True
        }
    },
    "Device": {
        "resourceType": {
            "is_leaf": True
        },
        "id": {
            "is_leaf": True
        },
        "meta": {
            "is_leaf": False,
            "children": {
                "profile": {
                    "is_leaf": False,
                    "children": {
                        "item": {
                            "is_leaf": True
                        }
                    }
                }
            }
        },
        "udiCarrier": {
            "is_leaf": False,
            "children": {
                "item": {
                    "is_leaf": False,
                    "children": {
                        "deviceIdentifier": {
                            "is_leaf": True
                        },
                        "carrierHRF": {
                            "is_leaf": True
                        }
                    }
                }
            }
        },
        "status": {
            "is_leaf": True
        },
        "distinctIdentifier": {
            "is_leaf": True
        },
        "manufactureDate": {
            "is_leaf": True
        },
        "expirationDate": {
            "is_leaf": True
        },
        "lotNumber": {
            "is_leaf": True
        },
        "serialNumber": {
            "is_leaf": True
        },
        "deviceName": {
            "is_leaf": False,
            "children": {
                "item": {
                    "is_leaf": False,
                    "children": {
                        "name": {
                            "is_leaf": True
                        },
                        "type": {
                            "is_leaf": True
                        }
                    }
                }
            }
        },
        "type": {
            "is_leaf": False,
            "children": {
                "coding": {
                    "is_leaf": False,
                    "children": {
                        "item": {
                            "is_leaf": False,
                            "children": {
                                "system": {
                                    "is_leaf": True
                                },
                                "code": {
                                    "is_leaf": True
                                },
                                "display": {
                                    "is_leaf": True
                                }
                            }
                        }
                    }
                },
                "text": {
                    "is_leaf": True
                }
            }
        },
        "patient": {
            "is_leaf": False,
            "children": {
                "reference": {
                    "is_leaf": True
                }
            }
        }
    },
    "DiagnosticReport": {
        "resourceType": {
            "is_leaf": True
        },
        "id": {
            "is_leaf": True
        },
        "meta": {
            "is_leaf": False,
            "children": {
                "profile": {
                    "is_leaf": False,
                    "children": {
                        "item": {
                            "is_leaf": True
                        }
                    }
                }
            }
        },
        "status": {
            "is_leaf": True
        },
        "category": {
            "is_leaf": False,
            "children": {
                "item": {
                    "is_leaf": False,
                    "children": {
                        "coding": {
                            "is_leaf": False,
                            "children": {
                                "item": {
                                    "is_leaf": False,
                                    "children": {
                                        "system": {
                                            "is_leaf": True
                                        },
                                        "code": {
                                            "is_leaf": True
                                        },
                                        "display": {
                                            "is_leaf": True
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "code": {
            "is_leaf": False,
            "children": {
                "coding": {
                    "is_leaf": False,
                    "children": {
                        "item": {
                            "is_leaf": False,
                            "children": {
                                "system": {
                                    "is_leaf": True
                                },
                                "code": {
                                    "is_leaf": True
                                },
                                "display": {
                                    "is_leaf": True
                                }
                            }
                        }
                    }
                }
            }
        },
        "subject": {
            "is_leaf": False,
            "children": {
                "reference": {
                    "is_leaf": True
                }
            }
        },
        "encounter": {
            "is_leaf": False,
            "children": {
                "reference": {
                    "is_leaf": True
                }
            }
        },
        "effectiveDateTime": {
            "is_leaf": True
        },
        "issued": {
            "is_leaf": True
        },
        "performer": {
            "is_leaf": False,
            "children": {
                "item": {
                    "is_leaf": False,
                    "children": {
                        "reference": {
                            "is_leaf": True
                        },
                        "display": {
                            "is_leaf": True
                        }
                    }
                }
            }
        },
        "presentedForm": {
            "is_leaf": False,
            "children": {
                "item": {
                    "is_leaf": False,
                    "children": {
                        "contentType": {
                            "is_leaf": True
                        },
                        "data": {
                            "is_leaf": True
                        }
                    }
                }
            }
        }
    },
    "DocumentReference": {
        "resourceType": {
            "is_leaf": True
        },
        "id": {
            "is_leaf": True
        },
        "meta": {
            "is_leaf": False,
            "children": {
                "profile": {
                    "is_leaf": False,
                    "children": {
                        "item": {
                            "is_leaf": True
                        }
                    }
                }
            }
        },
        "identifier": {
            "is_leaf": False,
            "children": {
                "item": {
                    "is_leaf": False,
                    "children": {
                        "system": {
                            "is_leaf": True
                        },
                        "value": {
                            "is_leaf": True
                        }
                    }
                }
            }
        },
        "status": {
            "is_leaf": True
        },
        "type": {
            "is_leaf": False,
            "children": {
                "coding": {
                    "is_leaf": False,
                    "children": {
                        "item": {
                            "is_leaf": False,
                            "children": {
                                "system": {
                                    "is_leaf": True
                                },
                                "code": {
                                    "is_leaf": True
                                },
                                "display": {
                                    "is_leaf": True
                                }
                            }
                        }
                    }
                }
            }
        },
        "category": {
            "is_leaf": False,
            "children": {
                "item": {
                    "is_leaf": False,
                    "children": {
                        "coding": {
                            "is_leaf": False,
                            "children": {
                                "item": {
                                    "is_leaf": False,
                                    "children": {
                                        "system": {
                                            "is_leaf": True
                                        },
                                        "code": {
                                            "is_leaf": True
                                        },
                                        "display": {
                                            "is_leaf": True
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "subject": {
            "is_leaf": False,
            "children": {
                "reference": {
                    "is_leaf": True
                }
            }
        },
        "date": {
            "is_leaf": True
        },
        "author": {
            "is_leaf": False,
            "children": {
                "item": {
                    "is_leaf": False,
                    "children": {
                        "reference": {
                            "is_leaf": True
                        },
                        "display": {
                            "is_leaf": True
                        }
                    }
                }
            }
        },
        "custodian": {
            "is_leaf": False,
            "children": {
                "reference": {
                    "is_leaf": True
                },
                "display": {
                    "is_leaf": True
                }
            }
        },
        "content": {
            "is_leaf": False,
            "children": {
                "item": {
                    "is_leaf": False,
                    "children": {
                        "attachment": {
                            "is_leaf": False,
                            "children": {
                                "contentType": {
                                    "is_leaf": True
                                },
                                "data": {
                                    "is_leaf": True
                                }
                            }
                        },
                        "format": {
                            "is_leaf": False,
                            "children": {
                                "system": {
                                    "is_leaf": True
                                },
                                "code": {
                                    "is_leaf": True
                                },
                                "display": {
                                    "is_leaf": True
                                }
                            }
                        }
                    }
                }
            }
        },
        "context": {
            "is_leaf": False,
            "children": {
                "encounter": {
                    "is_leaf": False,
                    "children": {
                        "item": {
                            "is_leaf": False,
                            "children": {
                                "reference": {
                                    "is_leaf": True
                                }
                            }
                        }
                    }
                },
                "period": {
                    "is_leaf": False,
                    "children": {
                        "start": {
                            "is_leaf": True
                        },
                        "end": {
                            "is_leaf": True
                        }
                    }
                }
            }
        }
    },
    "Encounter": {
        "resourceType": {
            "is_leaf": True
        },
        "id": {
            "is_leaf": True
        },
        "meta": {
            "is_leaf": False,
            "children": {
                "profile": {
                    "is_leaf": False,
                    "children": {
                        "item": {
                            "is_leaf": True
                        }
                    }
                }
            }
        },
        "identifier": {
            "is_leaf": False,
            "children": {
                "item": {
                    "is_leaf": False,
                    "children": {
                        "use": {
                            "is_leaf": True
                        },
                        "system": {
                            "is_leaf": True
                        },
                        "value": {
                            "is_leaf": True
                        }
                    }
                }
            }
        },
        "status": {
            "is_leaf": True
        },
        "class": {
            "is_leaf": False,
            "children": {
                "system": {
                    "is_leaf": True
                },
                "code": {
                    "is_leaf": True
                }
            }
        },
        "type": {
            "is_leaf": False,
            "children": {
                "item": {
                    "is_leaf": False,
                    "children": {
                        "coding": {
                            "is_leaf": False,
                            "children": {
                                "item": {
                                    "is_leaf": False,
                                    "children": {
                                        "system": {
                                            "is_leaf": True
                                        },
                                        "code": {
                                            "is_leaf": True
                                        },
                                        "display": {
                                            "is_leaf": True
                                        }
                                    }
                                }
                            }
                        },
                        "text": {
                            "is_leaf": True
                        }
                    }
                }
            }
        },
        "subject": {
            "is_leaf": False,
            "children": {
                "reference": {
                    "is_leaf": True
                },
                "display": {
                    "is_leaf": True
                }
            }
        },
        "participant": {
            "is_leaf": False,
            "children": {
                "item": {
                    "is_leaf": False,
                    "children": {
                        "type": {
                            "is_leaf": False,
                            "children": {
                                "item": {
                                    "is_leaf": False,
                                    "children": {
                                        "coding": {
                                            "is_leaf": False,
                                            "children": {
                                                "item": {
                                                    "is_leaf": False,
                                                    "children": {
                                                        "system": {
                                                            "is_leaf": True
                                                        },
                                                        "code": {
                                                            "is_leaf": True
                                                        },
                                                        "display": {
                                                            "is_leaf": True
                                                        }
                                                    }
                                                }
                                            }
                                        },
                                        "text": {
                                            "is_leaf": True
                                        }
                                    }
                                }
                            }
                        },
                        "period": {
                            "is_leaf": False,
                            "children": {
                                "start": {
                                    "is_leaf": True
                                },
                                "end": {
                                    "is_leaf": True
                                }
                            }
                        },
                        "individual": {
                            "is_leaf": False,
                            "children": {
                                "reference": {
                                    "is_leaf": True
                                },
                                "display": {
                                    "is_leaf": True
                                }
                            }
                        }
                    }
                }
            }
        },
        "period": {
            "is_leaf": False,
            "children": {
                "start": {
                    "is_leaf": True
                },
                "end": {
                    "is_leaf": True
                }
            }
        },
        "reasonCode": {
            "is_leaf": False,
            "children": {
                "item": {
                    "is_leaf": False,
                    "children": {
                        "coding": {
                            "is_leaf": False,
                            "children": {
                                "item": {
                                    "is_leaf": False,
                                    "children": {
                                        "system": {
                                            "is_leaf": True
                                        },
                                        "code": {
                                            "is_leaf": True
                                        },
                                        "display": {
                                            "is_leaf": True
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "location": {
            "is_leaf": False,
            "children": {
                "item": {
                    "is_leaf": False,
                    "children": {
                        "location": {
                            "is_leaf": False,
                            "children": {
                                "reference": {
                                    "is_leaf": True
                                },
                                "display": {
                                    "is_leaf": True
                                }
                            }
                        }
                    }
                }
            }
        },
        "serviceProvider": {
            "is_leaf": False,
            "children": {
                "reference": {
                    "is_leaf": True
                },
                "display": {
                    "is_leaf": True
                }
            }
        }
    },
    "Immunization": {
        "resourceType": {
            "is_leaf": True
        },
        "id": {
            "is_leaf": True
        },
        "meta": {
            "is_leaf": False,
            "children": {
                "profile": {
                    "is_leaf": False,
                    "children": {
                        "item": {
                            "is_leaf": True
                        }
                    }
                }
            }
        },
        "status": {
            "is_leaf": True
        },
        "vaccineCode": {
            "is_leaf": False,
            "children": {
                "coding": {
                    "is_leaf": False,
                    "children": {
                        "item": {
                            "is_leaf": False,
                            "children": {
                                "system": {
                                    "is_leaf": True
                                },
                                "code": {
                                    "is_leaf": True
                                },
                                "display": {
                                    "is_leaf": True
                                }
                            }
                        }
                    }
                },
                "text": {
                    "is_leaf": True
                }
            }
        },
        "patient": {
            "is_leaf": False,
            "children": {
                "reference": {
                    "is_leaf": True
                }
            }
        },
        "encounter": {
            "is_leaf": False,
            "children": {
                "reference": {
                    "is_leaf": True
                }
            }
        },
        "occurrenceDateTime": {
            "is_leaf": True
        },
        "primarySource": {
            "is_leaf": True
        },
        "location": {
            "is_leaf": False,
            "children": {
                "reference": {
                    "is_leaf": True
                },
                "display": {
                    "is_leaf": True
                }
            }
        }
    },
    "MedicationRequest": {
        "resourceType": {
            "is_leaf": True
        },
        "id": {
            "is_leaf": True
        },
        "meta": {
            "is_leaf": False,
            "children": {
                "profile": {
                    "is_leaf": False,
                    "children": {
                        "item": {
                            "is_leaf": True
                        }
                    }
                }
            }
        },
        "status": {
            "is_leaf": True
        },
        "intent": {
            "is_leaf": True
        },
        "category": {
            "is_leaf": False,
            "children": {
                "item": {
                    "is_leaf": False,
                    "children": {
                        "coding": {
                            "is_leaf": False,
                            "children": {
                                "item": {
                                    "is_leaf": False,
                                    "children": {
                                        "system": {
                                            "is_leaf": True
                                        },
                                        "code": {
                                            "is_leaf": True
                                        },
                                        "display": {
                                            "is_leaf": True
                                        }
                                    }
                                }
                            }
                        },
                        "text": {
                            "is_leaf": True
                        }
                    }
                }
            }
        },
        "medicationCodeableConcept": {
            "is_leaf": False,
            "children": {
                "coding": {
                    "is_leaf": False,
                    "children": {
                        "item": {
                            "is_leaf": False,
                            "children": {
                                "system": {
                                    "is_leaf": True
                                },
                                "code": {
                                    "is_leaf": True
                                },
                                "display": {
                                    "is_leaf": True
                                }
                            }
                        }
                    }
                },
                "text": {
                    "is_leaf": True
                }
            }
        },
        "subject": {
            "is_leaf": False,
            "children": {
                "reference": {
                    "is_leaf": True
                }
            }
        },
        "encounter": {
            "is_leaf": False,
            "children": {
                "reference": {
                    "is_leaf": True
                }
            }
        },
        "authoredOn": {
            "is_leaf": True
        },
        "requester": {
            "is_leaf": False,
            "children": {
                "reference": {
                    "is_leaf": True
                },
                "display": {
                    "is_leaf": True
                }
            }
        },
        "reasonReference": {
            "is_leaf": False,
            "children": {
                "item": {
                    "is_leaf": False,
                    "children": {
                        "reference": {
                            "is_leaf": True
                        },
                        "display": {
                            "is_leaf": True
                        }
                    }
                }
            }
        },
        "dosageInstruction": {
            "is_leaf": False,
            "children": {
                "item": {
                    "is_leaf": False,
                    "children": {
                        "sequence": {
                            "is_leaf": True
                        },
                        "timing": {
                            "is_leaf": False,
                            "children": {
                                "repeat": {
                                    "is_leaf": False,
                                    "children": {
                                        "frequency": {
                                            "is_leaf": True
                                        },
                                        "period": {
                                            "is_leaf": True
                                        },
                                        "periodUnit": {
                                            "is_leaf": True
                                        }
                                    }
                                }
                            }
                        },
                        "asNeededBoolean": {
                            "is_leaf": True
                        },
                        "doseAndRate": {
                            "is_leaf": False,
                            "children": {
                                "item": {
                                    "is_leaf": False,
                                    "children": {
                                        "type": {
                                            "is_leaf": False,
                                            "children": {
                                                "coding": {
                                                    "is_leaf": False,
                                                    "children": {
                                                        "item": {
                                                            "is_leaf": False,
                                                            "children": {
                                                                "system": {
                                                                    "is_leaf": True
                                                                },
                                                                "code": {
                                                                    "is_leaf": True
                                                                },
                                                                "display": {
                                                                    "is_leaf": True
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        },
                                        "doseQuantity": {
                                            "is_leaf": False,
                                            "children": {
                                                "value": {
                                                    "is_leaf": True
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    "Observation": {
        "resourceType": {
            "is_leaf": True
        },
        "id": {
            "is_leaf": True
        },
        "meta": {
            "is_leaf": False,
            "children": {
                "profile": {
                    "is_leaf": False,
                    "children": {
                        "item": {
                            "is_leaf": True
                        }
                    }
                }
            }
        },
        "status": {
            "is_leaf": True
        },
        "category": {
            "is_leaf": False,
            "children": {
                "item": {
                    "is_leaf": False,
                    "children": {
                        "coding": {
                            "is_leaf": False,
                            "children": {
                                "item": {
                                    "is_leaf": False,
                                    "children": {
                                        "system": {
                                            "is_leaf": True
                                        },
                                        "code": {
                                            "is_leaf": True
                                        },
                                        "display": {
                                            "is_leaf": True
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "code": {
            "is_leaf": False,
            "children": {
                "coding": {
                    "is_leaf": False,
                    "children": {
                        "item": {
                            "is_leaf": False,
                            "children": {
                                "system": {
                                    "is_leaf": True
                                },
                                "code": {
                                    "is_leaf": True
                                },
                                "display": {
                                    "is_leaf": True
                                }
                            }
                        }
                    }
                },
                "text": {
                    "is_leaf": True
                }
            }
        },
        "subject": {
            "is_leaf": False,
            "children": {
                "reference": {
                    "is_leaf": True
                }
            }
        },
        "encounter": {
            "is_leaf": False,
            "children": {
                "reference": {
                    "is_leaf": True
                }
            }
        },
        "effectiveDateTime": {
            "is_leaf": True
        },
        "issued": {
            "is_leaf": True
        },
        "valueQuantity": {
            "is_leaf": False,
            "children": {
                "value": {
                    "is_leaf": True
                },
                "unit": {
                    "is_leaf": True
                },
                "system": {
                    "is_leaf": True
                },
                "code": {
                    "is_leaf": True
                }
            }
        }
    },
    "Patient": {
        "resourceType": {
            "is_leaf": True
        },
        "id": {
            "is_leaf": True
        },
        "meta": {
            "is_leaf": False,
            "children": {
                "profile": {
                    "is_leaf": False,
                    "children": {
                        "item": {
                            "is_leaf": True
                        }
                    }
                }
            }
        },
        "text": {
            "is_leaf": False,
            "children": {
                "status": {
                    "is_leaf": True
                },
                "div": {
                    "is_leaf": True
                }
            }
        },
        "extension": {
            "is_leaf": False,
            "children": {
                "item": {
                    "is_leaf": False,
                    "children": {
                        "url": {
                            "is_leaf": True
                        },
                        "valueDecimal": {
                            "is_leaf": True
                        }
                    }
                }
            }
        },
        "identifier": {
            "is_leaf": False,
            "children": {
                "item": {
                    "is_leaf": False,
                    "children": {
                        "type": {
                            "is_leaf": False,
                            "children": {
                                "coding": {
                                    "is_leaf": False,
                                    "children": {
                                        "item": {
                                            "is_leaf": False,
                                            "children": {
                                                "system": {
                                                    "is_leaf": True
                                                },
                                                "code": {
                                                    "is_leaf": True
                                                },
                                                "display": {
                                                    "is_leaf": True
                                                }
                                            }
                                        }
                                    }
                                },
                                "text": {
                                    "is_leaf": True
                                }
                            }
                        },
                        "system": {
                            "is_leaf": True
                        },
                        "value": {
                            "is_leaf": True
                        }
                    }
                }
            }
        },
        "name": {
            "is_leaf": False,
            "children": {
                "item": {
                    "is_leaf": False,
                    "children": {
                        "use": {
                            "is_leaf": True
                        },
                        "family": {
                            "is_leaf": True
                        },
                        "given": {
                            "is_leaf": False,
                            "children": {
                                "item": {
                                    "is_leaf": True
                                }
                            }
                        },
                        "prefix": {
                            "is_leaf": False,
                            "children": {
                                "item": {
                                    "is_leaf": True
                                }
                            }
                        }
                    }
                }
            }
        },
        "telecom": {
            "is_leaf": False,
            "children": {
                "item": {
                    "is_leaf": False,
                    "children": {
                        "system": {
                            "is_leaf": True
                        },
                        "value": {
                            "is_leaf": True
                        },
                        "use": {
                            "is_leaf": True
                        }
                    }
                }
            }
        },
        "gender": {
            "is_leaf": True
        },
        "birthDate": {
            "is_leaf": True
        },
        "deceasedDateTime": {
            "is_leaf": True
        },
        "address": {
            "is_leaf": False,
            "children": {
                "item": {
                    "is_leaf": False,
                    "children": {
                        "city": {
                            "is_leaf": True
                        },
                        "state": {
                            "is_leaf": True
                        },
                        "country": {
                            "is_leaf": True
                        }
                    }
                }
            }
        },
        "maritalStatus": {
            "is_leaf": False,
            "children": {
                "coding": {
                    "is_leaf": False,
                    "children": {
                        "item": {
                            "is_leaf": False,
                            "children": {
                                "system": {
                                    "is_leaf": True
                                },
                                "code": {
                                    "is_leaf": True
                                },
                                "display": {
                                    "is_leaf": True
                                }
                            }
                        }
                    }
                },
                "text": {
                    "is_leaf": True
                }
            }
        },
        "multipleBirthBoolean": {
            "is_leaf": True
        },
        "communication": {
            "is_leaf": False,
            "children": {
                "item": {
                    "is_leaf": False,
                    "children": {
                        "language": {
                            "is_leaf": False,
                            "children": {
                                "coding": {
                                    "is_leaf": False,
                                    "children": {
                                        "item": {
                                            "is_leaf": False,
                                            "children": {
                                                "system": {
                                                    "is_leaf": True
                                                },
                                                "code": {
                                                    "is_leaf": True
                                                },
                                                "display": {
                                                    "is_leaf": True
                                                }
                                            }
                                        }
                                    }
                                },
                                "text": {
                                    "is_leaf": True
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    "Procedure": {
        "resourceType": {
            "is_leaf": True
        },
        "id": {
            "is_leaf": True
        },
        "meta": {
            "is_leaf": False,
            "children": {
                "profile": {
                    "is_leaf": False,
                    "children": {
                        "item": {
                            "is_leaf": True
                        }
                    }
                }
            }
        },
        "status": {
            "is_leaf": True
        },
        "code": {
            "is_leaf": False,
            "children": {
                "coding": {
                    "is_leaf": False,
                    "children": {
                        "item": {
                            "is_leaf": False,
                            "children": {
                                "system": {
                                    "is_leaf": True
                                },
                                "code": {
                                    "is_leaf": True
                                },
                                "display": {
                                    "is_leaf": True
                                }
                            }
                        }
                    }
                },
                "text": {
                    "is_leaf": True
                }
            }
        },
        "subject": {
            "is_leaf": False,
            "children": {
                "reference": {
                    "is_leaf": True
                }
            }
        },
        "encounter": {
            "is_leaf": False,
            "children": {
                "reference": {
                    "is_leaf": True
                }
            }
        },
        "performedPeriod": {
            "is_leaf": False,
            "children": {
                "start": {
                    "is_leaf": True
                },
                "end": {
                    "is_leaf": True
                }
            }
        },
        "location": {
            "is_leaf": False,
            "children": {
                "reference": {
                    "is_leaf": True
                },
                "display": {
                    "is_leaf": True
                }
            }
        }
    }
}