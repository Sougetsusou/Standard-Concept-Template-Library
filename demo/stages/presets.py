"""Deterministic presets used by mock Stage 1/2 and examples."""

PRESET_WORKFLOW = {
    "Laptop": {
        "prompt": "Create a practical laptop with a rectangular base, a thin hinged screen, and two rectangular side ports.",
        "parts": [
            {
                "semantic": "Base",
                "class_name": "Regular_Base",
                "decision": "use_existing",
                "params": {
                    "size": [0.32, 0.02, 0.22],
                    "position": [0.0, -0.01, 0.0],
                    "rotation": [0.0, 0.0, 0.0],
                },
            },
            {
                "semantic": "Screen",
                "class_name": "Regular_Screen",
                "decision": "use_existing",
                "params": {
                    "size": [0.30, 0.01, 0.21],
                    "offset": [0.11, 0.0],
                    "screen_rotation": [110],
                    "position": [0.0, 0.02, -0.01],
                    "rotation": [0.0, 0.0, 0.0],
                },
            },
            {
                "semantic": "Connector",
                "class_name": "Cuboidal_Connector",
                "decision": "use_existing",
                "params": {
                    "number_of_connector": [2],
                    "size": [0.015, 0.008, 0.012],
                    "separation": [0.01],
                    "offset": [-0.02, -0.005, 0.08],
                    "connector_rotation": [0],
                    "position": [0.0, 0.0, 0.0],
                    "rotation": [0.0, 0.0, 0.0],
                },
            },
        ],
    },
    "Mug": {
        "prompt": "Create a mug with a hollow cylindrical cup body and one curved side handle.",
        "parts": [
            {
                "semantic": "Body",
                "class_name": "Cylindrical_Body",
                "decision": "use_existing",
                "params": {
                    "outer_size": [0.045, 0.04, 0.09],
                    "inner_size": [0.035, 0.03, 0.07],
                    "position": [0.0, 0.0, 0.0],
                    "rotation": [0.0, 0.0, 0.0],
                },
            },
            {
                "semantic": "Handle",
                "class_name": "Curved_Handle",
                "decision": "use_existing",
                "params": {
                    "radius": [0.025, 0.004],
                    "central_angle": [220],
                    "position": [0.045, 0.0, 0.0],
                    "rotation": [0.0, 0.0, 0.0],
                },
            },
        ],
    },
}
