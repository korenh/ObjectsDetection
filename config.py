def get_config():
    return{
        "APP_HOST": "0.0.0.0",
        "APP_PORT": 8000,
        "APP_NAME": "ObjectsDetection",
        "APP_VERSION": "1.0",
        "APP_SECRET": "protected_ai",
        "APP_ERR_MSG": "Could not validate credentials",
        "MODEL_PATH": "objects.h5",
        "IMAGE_PATH": "./image.png",
        "MODEL_OUT_TYPE": "array",
        "MODEL_MPP": 30
    }
