import numpy as np
import cv2
from mss import mss
from PIL import Image
import pytesseract
import os
import math
import pyautogui
import time
from pynput.mouse import Button, Controller

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
mouse = Controller()

class ItemPotential():
	def __init__(self, crop: dict, lines: list, key: str = "enter"):
		self.crop: dict = crop
		self.lines: list = lines
		self.key: str = key

	def CheckCrop(self):
		with mss() as sct:
			while True:
				img, text = self.getText(sct)
				os.system('cls' if os.name == 'nt' else 'clear')
				print(text)

				cv2.imshow('test', img)
				if cv2.waitKey(33) & 0xFF in (ord('q'), 27, ):
					break

	def lookingPotential(self, targetDict: dict):
		count:int = 0
		time.sleep(3)

		with mss() as sct:
			while True:
				img, text = self.getText(sct)

				cv2.imshow('test', img)
				if cv2.waitKey(33) & 0xFF in (ord('q'), 27, ):
					break
				if("®" not in text and "Legen" not in text):
					continue

				os.system('cls' if os.name == 'nt' else 'clear')
				print("-------------------------------------------------------")
				print(text)
				print("-------------------------------------------------------")
				for target, min_amount in targetDict.items():
					amount = text.count(target)
					print("{target}: {amount}/{min_amount}".format(target= target, amount = amount, min_amount = min_amount))
					if amount >= min_amount:
						print("-------------------------------------------------------")
						print("count: {count} ({nx:,} NX)".format(count = count, nx = count * 1200))
						print("Success !!")
						return
				print("-------------------------------------------------------")
				print("count: {count} ({nx:,} NX)".format(count = count, nx = count * 1200))
				print("-------------------------------------------------------")
				self.trigger()
				count = count + 1
	
	def trigger(self):
		# pyautogui.press("enter")
		# pyautogui.press(["enter", "enter"])
		# pyautogui.click()
		# mouse.click(Button.left, 2)
		# mouse.press(Button.left)
		# mouse.release(Button.left)	
		pyautogui.keyDown(self.key)
		time.sleep(.2)
		pyautogui.keyUp(self.key)

		

	def getText(self, sct):
		screenShot = sct.grab(self.crop)
		img = Image.frombytes('RGB', (screenShot.width, screenShot.height), screenShot.rgb, )
		img = np.array(img)
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		img = cv2.bitwise_not(img)

		for line in self.lines:
			cv2.line(img, line["start"], line["end"], (255,255,255), 1)

		img = cv2.resize(img, (350 * 2, 150 * 2))
		ret, img = cv2.threshold(img, 35,255,cv2.THRESH_BINARY)
		# ret, img = cv2.threshold(img,127,255,cv2.THRESH_TRUNC)

		text = pytesseract.image_to_string(img)
		text = os.linesep.join([s for s in text.splitlines() if s and s is not " " and s is not "  "])
		return img, text