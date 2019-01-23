VALID_SCHEMA = {
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

MAX_FIELD_SIZE = 300

DEFAULT_LIMITS=["2000 per day", "500 per hour"]
