valid_schema = {
                    "type": "object",
                    "properties": {
                        "csp-report": {
                            "type": "object",
                            "properties": {
                                "blocked-uri": {
                                    "type": "string"
                                },
                                "document-uri": {
                                    "type": "string"
                                },
                                "original-policy": {
                                    "type": "string"
                                },
                                "referrer": {
                                    "type": "string"
                                },
                                "violated-directive": {
                                    "type": "string"
                                },
                                "line-number": {
                                    "type": "integer",
                                    "optional": True
                                },
                                "source-file": {
                                    "type": "string",
                                    "optional": True
                                },
                                "column-number": {
                                    "type": "integer",
                                    "optional": True
                                }
                            }
                        }
                    }
                }

max_field_size = 300

