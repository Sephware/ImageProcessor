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
        self.current_image = self.original_image

    def blurImage(self, k_size):
        """
        Docstring for blurImage
        
        :param img: Image input
        :param k_size: Description
        """
        self.current_image = cv.blur(self.current_image, (k_size, k_size))

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

        self.current_image = cv.filter2D(self.current_image, -1, kernel)
    
    def rotateImage(self, degrees: int):
        """
        Docstring for rotateImage
        
        :param img: Image input
        :param degrees: Description
        :type degrees: int
        """
        
        degrees = np.clip(degrees, 0, 360)
        # Get the height and width of the image
        rows, cols, _ = self.current_image.shape

        M = cv.getRotationMatrix2D(((cols-1)/2.0, (rows-1)/2.0), degrees, 1)
        self.current_image = cv.warpAffine(self.current_image, M, (cols, rows))
        

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
    cv.createTrackbar("Smoothness", window_name, 0, 100, nothing)
    cv.createTrackbar("Rotation", window_name, 0, 360, nothing)

    # Display Image in Window
    cv.imshow(window_name, p.current_image)

    prev_s = 0
    prev_r = 0

    while(1):
        # Program will exit once user press 'esc' key
        k = cv.waitKey(1) & 0xFF
        if k == 27:
            break

        # Track current positions of trackbar values
        smoothness = cv.getTrackbarPos("Smoothness", window_name)
        rotation = cv.getTrackbarPos("Rotation", window_name)

        s_sum = smoothness - prev_s
        if s_sum > 0:
            p.sharpen_image(s_sum)
            prev_s = smoothness
        elif s_sum < 0:
            
            prev_s = smoothness
        elif s_sum == 0:
            pass
        
        r_sum = rotation - prev_r
        if r_sum > 0:
            p.rotateImage(r_sum)
            prev_r = rotation
        elif r_sum < 0:
            p.rotateImage(r_sum)
            prev_r = rotation
        elif r_sum == 0:
            pass

        cv.imshow(window_name, p.current_image)
    
    # Closes window once loop ends
    cv.destroyAllWindows()



