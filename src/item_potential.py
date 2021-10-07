import numpy as np
import cv2
from mss import mss
from PIL import Image
import pytesseract
import os
import pyautogui
import time
import re

NORMAL_POTENTIAL_REX = r"[ ]*\((?P<rarity>.+)\)[ ]*(?P<value>.+)"
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class ItemPotential():
	def __init__(self, crop: dict, key: str = "enter"):
		self.crop: dict = crop
		self.key: str = key

	def lookingPotential(self, targetDict: dict, useCalibrate: bool = True, max_count = -1):
		time.sleep(3)
		with mss() as sct:
			# calibrate
			if(useCalibrate):
				self.calibrate(sct)

			# countdown
			self.countdown(3)

			# start
			while True:
				img, text = self.getText(sct)

				cv2.imshow('test', img)
				cv2.waitKey(1)

				if("Legen" not in text and "Unique" not in text):
					continue

				os.system('cls' if os.name == 'nt' else 'clear')
				# self.logText(text)
				potentials = self.getPotentials(text)
				result = "count: {count:,} ({nx:,} NX)".format(count = count, nx = count * 1200)

				for target, min_amount in targetDict.items():
					target_list = re.split(', |,', target)
					amount = 0
					for potential in potentials:
						have_all_word = all(ele in potential['value'] for ele in target_list)
						check_start_word = potential['value'].startswith(target_list[0])

						if have_all_word and check_start_word:
							amount = amount + 1

					print("{}: {}/{}".format(target_list[0], amount, min_amount))

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
				if max_count > 0 and count > max_count:
					retry = input("limit exceeded!!! press 'Y' to continue and reset count:")
					if retry.lower() != "y":
						count = 0
						return
					
	
	def calibrate(self, sct):
		# calibrate
		while True:
			img, text = self.getText(sct)
			os.system('cls' if os.name == 'nt' else 'clear')
			self.getPotentials(text)
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
		print("-------------------------------------------------------")
		for line in lines:
			matches = re.search(NORMAL_POTENTIAL_REX, line)
			if matches:
				rarity = matches["rarity"]
				value = matches["value"]
				print("({}) - {}".format(matches['rarity'], matches['value']))
				potentials.append(dict(rarity=rarity, value=value))
		print("-------------------------------------------------------")
		return potentials