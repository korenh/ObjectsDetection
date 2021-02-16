from imageai.Detection import ObjectDetection
from PIL import Image
from io import BytesIO
import os


class ClassDetection(object):
    def __init__(self):
        self.execution_path = os.getcwd()
        self.detector = ObjectDetection()
        self.detector.setModelTypeAsRetinaNet()
        self.detector.setModelPath(os.path.join(
            self.execution_path, "objects.h5"))
        self.detector.loadModel()

    def prediction(self, file):
        im = Image.open(BytesIO(file))
        im.save('./image.png', 'PNG')
        returned_image, detection = self.detector.detectObjectsFromImage(
            input_image='./image.png', output_type="array", minimum_percentage_probability=30)
        return detection
