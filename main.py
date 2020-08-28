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
		
		#initial variable sets
		self.width = 0
		self.height = 0
		self.left = 0
		self.top = 0
		self.lang_src = ''
		self.ocr_lang = ''
		self.app_start = False
		
		#set the language for ocr and translator default is set to english
		self.lang_option = QComboBox()
		self.lang_option.addItems(googletrans.LANGUAGES.values())
		self.lang_option.currentIndexChanged.connect(self.lang_change)
		self.layout.addWidget(self.lang_option)
		
		#button to start application translation
		self.button = QPushButton("Start Application")
		self.button.clicked.connect(self.start_trans)
		self.layout.addWidget(self.button)
		
		self.label = QLabel('Text Display Here')
		self.label.setAlignment(Qt.AlignCenter)
		
		self.setLayout(self.layout)
		self.show()
	
	def lang_change(self, i):
		#adjust the language settings for the OCR and goolgetrans libraries
		key = list(googletrans.LANGUAGES.keys())
		self.lang_src = key[i]
		
		d = {}
		with open('lang_text.txt') as f:
			lines = f.readlines()
			for line in lines:
				(key, val) = line.replace(' ','').strip().split('=')
				d[key] = val
		f.close()
		
		self.ocr_lang = d.get(self.lang_src)
		self.label.setText(self.lang_src)
		
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

		#remove button and language option then display translation
		self.button.deleteLater()
		self.lang_option.deleteLater()
		self.refresh_label
		self.layout.addWidget(self.label)
	
	def refresh_label(self):
		#updates translated text // bypass refresh if the application start button not pressed
		if self.app_start:
			frame = self.screen_rec(left=self.left, top=self.top, width=self.width, height=self.height)
			text = self.translate_text(frame)
			self.label.setText(text)
		else:
			pass

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
