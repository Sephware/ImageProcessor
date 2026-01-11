import cv2 as cv
import numpy as np 

class ImageProcessor():
    
    def getImage(file_name: str):
        """
        Docstring for getImage
        
        :param file_name: Description
        :type file_name: str
        """
        # Finds the image file, returns None if file not found
        img = cv.imread(file_name)
        if img is None:
            return None
        else:
            return img

    def blurImage(img, k_size):
        """
        Docstring for blurImage
        
        :param img: Image input
        :param k_size: Description
        """

        new_img = cv.blur(img, (k_size, k_size))
        return new_img
    
    def rotateImage(img, degrees: int):
        """
        Docstring for rotateImage
        
        :param file_name: Name of the image file.
        :type file_name: str
        :param degrees: Description
        :type degrees: int
        """
        
        # Get the height and width of the image
        rows, cols, _ = img.shape

        M = cv.getRotationMatrix2D(((cols-1)/2.0, (rows-1)/2.0), degrees, 1)
        new_img = cv.warpAffine(img, M, (cols, rows))
        return new_img

    def createWindow(img):
        """
        Docstring for createWindow
        """
        
        # Function used to pass an uneeded parameter
        def nothing(x):
            pass

        # Creates the main window
        cv.namedWindow("Image Processor")
        
        # Create trackbars for image smoothing, Image transformation, and Color Edititng
        cv.createTrackbar("Smoothness", "Image Processor", 0, 20, nothing)
        cv.createTrackbar("Rotation", "Image Processor", 0, 360, nothing)
        
        # Display Image in Window
        while(1):
            cv.imshow("Image Processor", img)
            k = cv.waitKey(1) & 0xFF
            if k == 27:
                break

            # Track current positions of trackbar values
            smoothness = cv.getTrackbarPos("Smoothness", "Image Processor")
            rotation = cv.getTrackbarPos("Rotation", "Image Processor")
            prev_s = 0
            prev_r = 0
            
            # Automatically updates the image if value changes
            if prev_s != smoothness:
                # Precondition for smoothness to avoid kernel_size error
                if smoothness > 0:
                    img = ImageProcessor.blurImage(img, smoothness)
                    prev_s = smoothness
            if prev_r != rotation:
                img = ImageProcessor.rotateImage(img, rotation)
                prev_r = rotation

        # Closes Window once loop ends
        cv.destroyAllWindows()
        
        

### Section to test functions in console with an example image
if __name__ == '__main__':
    img_path = 'static/images/Supra.jpg'
    img = ImageProcessor.getImage(img_path)
    if img is None:
        print("Image Not Found")
    else:
        ImageProcessor.createWindow(img)





