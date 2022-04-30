from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

import time
import RPi.GPIO as GPIO

#sets the on/off switch for voltage
ON = GPIO.LOW
OFF = GPIO.HIGH

#put LED pins in an array
PINR = 11
PINB = 13
PING = 15
PINS = [PINR, PINB, PING]

#initialize GPIO and set pins to output mode
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PINR, GPIO.OUT)
GPIO.setup(PINB, GPIO.OUT)
GPIO.setup(PING, GPIO.OUT)

#create a custom window
class MyWindow(QMainWindow):
	def __init__(self):
		super(MyWindow, self).__init__()
		self.setGeometry(200, 200, 300, 300)
		self.setWindowTitle("LED GUI Program")		
		self.initUI()
		
	def initUI(self):
		self.pins = [PINR, PINB, PING]
		self.rB = MyButton(self, QtWidgets.QRadioButton, "Red LED", 100, 10, LEDClicker(PINR))
		self.bB = MyButton(self, QtWidgets.QRadioButton, "Blue LED", 100, 50, LEDClicker(PINB))
		self.gB = MyButton(self, QtWidgets.QRadioButton, "Green LED", 100, 90, LEDClicker(PING))
		self.eB = MyButton(self, QtWidgets.QPushButton, "Exit", 100, 130, self.close)
		
	def closeEvent(self, event):
		turnOff()
		GPIO.cleanup()
		return

#custom button class
class MyButton:
	def __init__(self, win, buttonType, text, x, y, response):
        
		self.win = win
		self.text = text
		self.x = x
		self.y = y
		self.response = response
		
		self.InitButton(buttonType)
		
	#initialize button
	def InitButton(self, buttonType):
        
        #render radio button in selected window
		self.button = buttonType(self.win)
		self.button.setText(self.text)
		self.button.move(self.x, self.y)
		self.button.clicked.connect(self.response)
	

#action when button is clicked
class LEDClicker:
    
    #button recieves output pin
	def __init__(self, pin):
		self.pin = pin
		
	#searches pin array for selected pin
	def __call__(self):
		for pin in PINS:
            
            #turn selected LED on
			if (pin == self.pin):
				GPIO.output(pin, ON)
				
            #other pins are turned off
			else:
				GPIO.output(pin, OFF)

#main window
def window():
	app = QApplication(sys.argv)
	win = MyWindow()
	
	win.show()
	sys.exit(app.exec_())

#shutdown procedure to turn all pins off
def turnOff():
    for pin in PINS:
        GPIO.output(pin, OFF)

turnOff()
window()
