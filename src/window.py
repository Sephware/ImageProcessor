import PyQt5.QtWidgets as qt
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

        # Adding Widgets
        reset_button = qt.QPushButton("Reset to Default")
        reset_button.clicked.connect(self.reset_button_action)
        self.setCentralWidget(reset_button)

    def reset_button_action(self):
        if self.debug:
            print("Reset button clicked.")

        self.processor.reset()
    