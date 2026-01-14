import PyQt5.QtWidgets as qt
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
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
        self.layout = qt.QGridLayout()

        # Image file input
        self.image_file = ''
        self.image_label = qt.QLabel(self)
        input_button = qt.QPushButton("Open Image File")
        input_button.clicked.connect(self.input_button_action)

        self.layout.addWidget(input_button)
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)


    def reset_button_action(self):
        if self.debug:
            print("Reset button clicked.")
        self.processor.reset()
        self.update_image()

    
    def smoothness_value(self, s):
        if s < 0:
            self.processor.sharpen_image(abs(s))
        elif s > 0:
            self.processor.blur_image(s)
        self.update_image()

    
    def rotation_value(self, r):
        self.processor.rotate_image(r)
        self.update_image()


    def add_all_widgets(self):

        # Smoothing/Sharpening Slider
        smoothness_slider = qt.QSlider(Qt.Horizontal)
        smoothness_slider.setRange(-50, 50)
        smoothness_slider.valueChanged.connect(self.smoothness_value)

        # Rotation Slider
        rotation_slider = qt.QSlider(Qt.Horizontal)
        rotation_slider.setRange(0, 360)
        rotation_slider.valueChanged.connect(self.rotation_value)

        # Reset Button
        reset_button = qt.QPushButton("Reset to Default")
        reset_button.clicked.connect(self.reset_button_action)

        # Image Label
        self.image_label.setPixmap(QPixmap(self.image_file))

        # Addwidgets to Layout
        widgets = [
            smoothness_slider,
            rotation_slider,
            reset_button,
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


    def update_image(self):
        new_img_file = self.processor.save()
        self.image_label.setPixmap(QPixmap(new_img_file))

