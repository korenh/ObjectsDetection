from imageai.Detection import ObjectDetection
from PIL import Image
from io import BytesIO
import os
import config

config = config.get_config()


class ClassDetection(object):
    def __init__(self):
        self.execution_path = os.getcwd()
        self.detector = ObjectDetection()
        self.detector.setModelTypeAsRetinaNet()
        self.detector.setModelPath(os.path.join(
            self.execution_path, config["MODEL_PATH"]))
        self.detector.loadModel()

    def prediction(self, file):
        im = Image.open(BytesIO(file))
        im.save(config["IMAGE_PATH"], 'PNG')
        returned_image, detection = self.detector.detectObjectsFromImage(
            input_image=config["IMAGE_PATH"], output_type=config["MODEL_OUT_TYPE"], minimum_percentage_probability=config["MODEL_MPP"])
        return detection
