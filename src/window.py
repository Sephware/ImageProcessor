import PyQt5.QtWidgets as qt
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
import cv2 as cv
from image_processor import ImageProcessor

class MainWindow(qt.QMainWindow):
    def __init__(self, debug=False):
        """
        Initalizer for MainWindow()
        
        :param self: Description
        :param is_debug: Option to print any action made on MainWindow to the console.
        """
        super().__init__()
        self.debug = debug
        self.processor = ImageProcessor()
        self.setWindowTitle("Image Processor")

        # Create Window Layout
        self.widget = qt.QWidget()
        self.layout = qt.QVBoxLayout()

        # Image file input
        self.image_file = ''
        self.image_label = qt.QLabel(self)
        input_button = qt.QPushButton("Open Image File")
        input_button.clicked.connect(self.input_button_action)

        self.layout.addWidget(input_button)
        self.widget.setLayout(self.layout)
        self.setCentralWidget(input_button)


### Functions for each widget's action ###

    def reset_button_action(self):
        """
        Action for reset_button. Calls ImageProcessor.reset() and resets any changes to the image.
        """
        self.processor.reset()
        self.smoothness_slider.setValue(0)
        self.rotation_slider.setValue(0)
    
    def smoothness_value(self, s):
        """
        Updates the clarity value everytime the slider value changes.
        """
        self.processor.set_clarity(s)
        self.update_image()

    def rotation_value(self, r):
        """
        Updates the rotation value everytime the slider value changes.
        """
        self.processor.set_rotation(r)
        self.update_image()

    def filter_value(self, f):
        """
        Docstring for filter_value
        Updates the filter box each time a different value in the dropbox is selected.
        """
        self.processor.set_filter(f)
        self.update_image()

### Handling Widgets ###

    def add_all_widgets(self):
        # Smoothing/Sharpening Slider
        self.smoothness_slider = qt.QSlider(Qt.Horizontal)
        self.smoothness_slider.setRange(-50, 50)
        self.smoothness_slider.valueChanged.connect(self.smoothness_value)

        # Rotation Slider
        self.rotation_slider = qt.QSlider(Qt.Horizontal)
        self.rotation_slider.setRange(0, 360)
        self.rotation_slider.valueChanged.connect(self.rotation_value)

        # Filter Box
        self.filter_box = qt.QComboBox()
        self.filter_box.addItems(["Default", "Greyscale"])
        self.filter_box.currentIndexChanged.connect(self.filter_value)

        # Reset Button
        self.reset_button = qt.QPushButton("Reset to Default")
        self.reset_button.clicked.connect(self.reset_button_action)

        # Image Label
        image = QPixmap(self.image_file)
        image.scaled(
            800, 
            600, 
            Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.SmoothTransformation
            )
        self.image_label.setPixmap(image)
        self.image_label.setSizePolicy(qt.QSizePolicy.Ignored, qt.QSizePolicy.Ignored)
        self.image_label.setScaledContents(True)

        # Addwidgets to Layout
        widgets = [
            self.smoothness_slider,
            self.rotation_slider,
            self.filter_box,
            self.reset_button,
            self.image_label,
        ]

        for w in widgets:
            self.layout.addWidget(w)

    def input_button_action(self):
        input = qt.QFileDialog(self)
        input.setWindowTitle("Select Image File")
        input.setFileMode(qt.QFileDialog.FileMode.ExistingFile)
        input.setViewMode(qt.QFileDialog.ViewMode.Detail)
        #input.setNameFilter("Images (*.png, *.jpg, *.webp)")

        if input.exec():
            files = input.selectedFiles()
            self.image_file = files[0]
            self.processor = ImageProcessor(self.image_file)
            
            self.add_all_widgets()
            self.widget.setLayout(self.layout)
            self.setCentralWidget(self.widget)

    def np_to_qimage(self, cv_img):
        """
        A helper function for MainWindow.update_image() that converts a numpy array to a QImage for display.
        
        :param cv_img: A numpy array representing the image to be converted.
        :return: A QImage object that can be displayed in the PyQt5 interface.
        """
        rbg_image = cv.cvtColor(cv_img, cv.COLOR_BGR2RGB)
        height, width, channel = rbg_image.shape
        bytes_per_line = channel * width
        q_img = QImage(rbg_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(q_img)
    
    # TODO: Change how program updates and saves image without using "new_image.jpg"
    def update_image(self):
        """
        Updates the image displayed in the interface with the current settings in ImageProcessor.
        """
        self.processor.update()
        cv_image = self.processor.get_image()
        q_image = self.np_to_qimage(cv_image)
        q_image = q_image.scaled(
            800, 
            600, 
            Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.SmoothTransformation
            )
        self.image_label.setPixmap(q_image)

