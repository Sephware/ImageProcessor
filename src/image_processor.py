import cv2 as cv
import numpy as np

class ImageProcessor():

    def __init__(self, file_name=None):
        """
        Constructor for the `ImageProcessor()` class
        
        :param file_name: Path or input of the image file
        """
        self.file = file_name
        if file_name is None:
            self.current_image = np.zeros((300, 521, 3), np.uint8)
        else:
            self.current_image = cv.imread(file_name)
        
        self.original_image = self.current_image 
        self.image_shape = self.current_image.shape
        self.settings = {
            "smoothness": 0,
            "rotation": 0,
            "filter": 0, # 0 is normal, 1 is greyscale, 2-N will be a colored filter
        }

    def set_smoothness(self, strength: int):
        """
        Sets the smoothness of the image.

        :param strength: Value of the smoothness. Positive values will blur the image, while negative values sharpen the image.
        :type strength: int
        """
        self.settings["smoothness"] = strength
    
    def set_rotation(self, degrees: int):
        """
        Rotates the Image

        :param degrees: Value of the image's rotation form 0 to 360 degrees.
        :type degrees: int
        """
        self.settings["rotation"] = degrees

    def set_filter(self, filter: int):
        """
        Docstring for set_filter

        :param filter: Value of a selected filter. 0 is default, 1 is greyscale, 2 is warmed, 3 is cooled
        :type filter: int
        """
        self.settings["filter"] = filter


    def update(self):
        """
        Updates the image with the changed settings
        """
        self.current_image = self.original_image

        # Filter
        x = self.settings["filter"]
        if x == 0:
            pass
        elif x == 1:
            self.current_image = cv.imread(self.file, cv.IMREAD_GRAYSCALE)
        elif x == 2:
            pass

        # Smoothness
        x = self.settings["smoothness"]
        if x > 0: # Will blur the image
            self.current_image = cv.blur(self.current_image, (x, x))
        elif x < 0: # Will sharpen the image
            alpha = x / 10
            kernel = np.array([
                [0, -alpha, 0],
                [-alpha, 1 + 4*alpha, -alpha],
                [0, -alpha, 0],
            ])
            self.current_image = cv.filter2D(self.current_image, -1, kernel)

        # Rotation
        x = self.settings["rotation"]
        rows, cols, _ = self.original_image.shape

        M = cv.getRotationMatrix2D(((cols-1)/2.0, (rows-1)/2.0), x, 1)
        self.current_image = cv.warpAffine(self.current_image, M, (cols, rows))



    def reset(self):
        """
        Resets the current image to its original
        """
        self.current_image = self.original_image

        for n in self.settings:
            n = 0

    def save(self):
        """
        Saves the current image with the settings
        """
        file = "static/images/new_image.jpg"
        cv.imwrite(file, self.current_image)
        return file
