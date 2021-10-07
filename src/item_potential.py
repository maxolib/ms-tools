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

import re
NORMAL_POTENTIAL_REX = r"[ ]*\((?P<rarity>.+)\)[ ]*(?P<name>.+)[ ]*:[ ]*(?P<value>.+)[ ]*"

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
mouse = Controller()

class ItemPotential():
	def __init__(self, crop: dict, key: str = "enter"):
		self.crop: dict = crop
		self.key: str = key

	# def CheckCrop(self):
	# 	with mss() as sct:
	# 		while True:
	# 			img, text = self.getText(sct)
	# 			os.system('cls' if os.name == 'nt' else 'clear')
	# 			print(text)

	# 			cv2.imshow('test', img)
	# 			if cv2.waitKey(33) & 0xFF in (ord('q'), 27, ):
	# 				break

	def lookingPotential(self, targetDict: dict, showDebug: bool = True, count: int = 0, isCalibrate: bool = True):
		time.sleep(3)
		with mss() as sct:
			# calibrate
			if isCalibrate:
				self.calibrate(sct)

			# countdown
			self.countdown(3)

			# start
			while True:
				img, text = self.getText(sct)

				if showDebug:
					cv2.imshow('test', img)
					cv2.waitKey(1)

				if("Legen" not in text and "Unique" not in text ):
					continue

				os.system('cls' if os.name == 'nt' else 'clear')
				self.logText(text)
				result = "count: {count:,} ({nx:,} NX)".format(count = count, nx = count * 1200)

				for target, min_amount in targetDict.items():
					amount = text.count(target)
					print("{target}: {amount}/{min_amount}".format(target= target, amount = amount, min_amount = min_amount))
					if amount >= min_amount:
						self.logText(result)
						print("Success !!")
						retry = input("manual re-potential one time then type 'Y' to continue:")
						if retry.lower() != "y":
							return
						else:
							self.countdown(3)
							break
				self.logText(result)
				self.trigger()
				count = count + 1
	
	def calibrate(self, sct):
		# calibrate
		while True:
			img, text = self.getText(sct)
			os.system('cls' if os.name == 'nt' else 'clear')
			self.logText(text)
			print("Calibration")
			print("Press any key to continue...")
			cv2.imshow('test', img)
			if cv2.waitKey(1) is not -1:
				break
	
	def countdown(self, seconds: int = 3):
		os.system('cls' if os.name == 'nt' else 'clear')
		print("Auto-cube will start in 3 seconds, Please focus the MapleStory window.")
		while seconds >= 0:
			print(seconds)
			time.sleep(1)
			seconds = seconds - 1

	def trigger(self):
		pyautogui.press("enter")

	def getText(self, sct):
		screenShot = sct.grab(self.crop)
		img = Image.frombytes('RGB', (screenShot.width, screenShot.height), screenShot.rgb, )
		img = np.array(img)

		img = cv2.bitwise_not(img)

		img = cv2.resize(img, (350 * 2, 150 * 2))
		ret, img = cv2.threshold(img, 77,255,cv2.THRESH_BINARY)
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		ret, img = cv2.threshold(img, 35,255,cv2.THRESH_BINARY)
		kernel = np.ones((2,2), np.uint8)
		img = cv2.dilate(img, kernel, iterations = 1)
		
		text = pytesseract.image_to_string(img)
		text = os.linesep.join([s for s in text.splitlines() if s and s is not " " and s is not "  "])
		return img, text
	
	def logText(self, text: str):
		print("-------------------------------------------------------")
		print(text)
		print("-------------------------------------------------------")

	def getPotentials(self, text: str) -> list: 
		lines = text.splitlines()
		
		potentials = []
		for line in lines:
			matches = re.search(NORMAL_POTENTIAL_REX, line)
			if matches:
				rarity = matches["rarity"]
				name = matches["name"]
				value = matches["value"]
				print("#{}#, #{}#, #{}#".format(matches['rarity'], matches['name'], matches['value']))
				potentials.append(dict(key=name, value=value))
		print(potentials)

	def matchPotentials(self, target_list: list, potentials: list) -> bool:
		for target in target_list:
			print("-------------------------")
			score = 0
			total_score = 0
			for key, value in target.items():
				names = re.split(', |,', key)
				for name in names:
					count = 0
					need_percent = '%' in name
					name = name.replace('%', '')

					total_score = total_score
					print(name, value, need_percent)