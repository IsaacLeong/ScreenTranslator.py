from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import numpy
import cv2
import pytesseract
import pyautogui
import datetime
from PIL import Image
from googletrans import Translator

class ScreenTrans(QWidget):
	def __init__(self):
		super().__init__()
		self.title = 'Main Application'
		self.layout = QGridLayout()
		
		#dimension size and coordinate variables
		self.width = 0
		self.height = 0
		self.left = 0
		self.top = 0
		
		#button to start application translation
		self.button = QPushButton("Start Application")
		self.button.clicked.connect(self.start_trans)
		self.layout.addWidget(self.button)
		
		self.label = QLabel('Text Display Here')
		self.label.setAlignment(Qt.AlignCenter)
		
		self.setLayout(self.layout)
		self.show()
	
	def start_trans(self):
		#intialize necessary dimension sizes within 2.5 seconds
		pyautogui.click()
		pyautogui.PAUSE = 2.5
		pyautogui.click()
		fw = pyautogui.getActiveWindow()
		self.width = fw.width
		self.height = fw.height
		self.left = fw.left
		self.top = fw.top

		#remove button and display translation
		self.button.deleteLater()
		self.refresh_label
		self.layout.addWidget(self.label)
	
	def refresh_label(self):
		#updates translated text
		frame = self.screen_rec(left=self.left, top=self.top, width=self.width, height=self.height)
		text = self.translate_text(frame)
		self.label.setText(text)

	def screen_rec(self, width, height, left, top):
		#gets screenshot of image with dimensions specified above	
		image = pyautogui.screenshot(region=(left, top, width-20, height-20))
		frame = numpy.array(image)
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		frame = cv2.bitwise_not(frame)
		#added threshold to clearup images
		frame = cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
		cv2.destroyAllWindows()
		return frame

	def translate_text(self, frame):
		#get as much text extracted from the image and convert
		#currently language requirements are hardcoded (must implement a dynamic set feature)
		translator = Translator()
		text = pytesseract.image_to_string(Image.fromarray(frame), lang='jpn')
		text = translator.translate(text, src='ja', dest='en').text
		return text


app = QApplication([])
screen_baby = ScreenTrans()
timer = QTimer()
timer.timeout.connect(screen_baby.refresh_label)
timer.start(5000)
cv2.destroyAllWindows()
app.exec_()
