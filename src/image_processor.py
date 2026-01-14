import cv2 as cv
import numpy as np

class ImageProcessor():

    def __init__(self, file_name=None):
        """
        Constructor for the `ImageProcessor()` class
        
        :param self: Description
        :param file_name: Path or input of the image file
        """
        if file_name is None:
            self.current_image = np.zeros((300, 521, 3), np.uint8)
        else:
            self.current_image = cv.imread(file_name)
            
        self.original_image = self.current_image
        self.image_shape = self.current_image.shape

    def reset(self):
        """
        Resets the current image to its original
        
        :param self: Description
        """
        self.current_image = self.original_image

    def save(self):
        file = "static/images/new_image.jpg"
        cv.imwrite(file, self.current_image)
        return file


    def blur_image(self, k_size):
        """
        Docstring for blurImage
        
        :param img: Image input
        :param k_size: Description
        """
        self.current_image = cv.blur(self.original_image, (k_size, k_size))

    def sharpen_image(self, strength):
        """
        Docstring for sharpen_image
        
        :param self: Description
        :param value: Description
        """
        alpha = strength / 10.0

        kernel = np.array([
            [0, -alpha, 0],
            [-alpha, 1 + 4*alpha, -alpha],
            [0, -alpha, 0],
        ])

        self.current_image = cv.filter2D(self.original_image, -1, kernel)
    
    def rotate_image(self, degrees: int):
        """
        Docstring for rotateImage
        
        :param img: Image input
        :param degrees: Description
        :type degrees: int
        """
        
        degrees = np.clip(degrees, 0, 360)
        # Get the height and width of the image
        rows, cols, _ = self.original_image.shape

        M = cv.getRotationMatrix2D(((cols-1)/2.0, (rows-1)/2.0), degrees, 1)
        self.current_image = cv.warpAffine(self.original_image, M, (cols, rows))
        

### Section to test functions in console with an example image
if __name__ == '__main__':
    img_path = 'static/images/Supra.jpg'
    p = ImageProcessor(img_path)
    
    # Function used to pass an uneeded parameter
    def nothing(x):
        pass
    
    # Creates the main window
    window_name = "Image Processor (Press 'esc' to exit program)"
    cv.namedWindow(window_name)
    
    # Create trackbars for image smoothing, Image transformation, and Color Edititng
    cv.createTrackbar("Smoothness", window_name, 50, 100, nothing)
    cv.createTrackbar("Rotation", window_name, 0, 360, nothing)

    # Display Image in Window
    cv.imshow(window_name, p.current_image)

    while(1):
        # Program will exit once user press 'esc' key
        k = cv.waitKey(1) & 0xFF
        if k == 27:
            break

        # Track smoothness and rotation value
        smoothness = cv.getTrackbarPos("Smoothness", window_name)
        rotation = cv.getTrackbarPos("Rotation", window_name)

        if smoothness > 50:
            p.blur_image(smoothness - 50)
        elif smoothness < 50:
            p.sharpen_image(50 - smoothness)

        p.rotate_image(rotation)

        cv.imshow(window_name, p.current_image)
    
    # Closes window once loop ends
    cv.destroyAllWindows()



