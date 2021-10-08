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
MAIN_STAT_LIST = ["STR", "DEX", "INT", "LUK"]

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class ItemPotential():
	def __init__(self, crop: dict, key: str = "enter"):
		self.crop: dict = crop
		self.key: str = key

	def findingPotential(self, targetDict: dict, useCalibrate: bool = True, applyAllStat = True, maxCount = -1):
		count = 0
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

				self.clearConsole()

				potentials = self.getPotentials(text)
				countText = self.getCountText(count, maxCount)

				for target, min_amount in targetDict.items():
					target_list = re.split(', |,', target)
					amount = self.getAmountFromTargetList(target_list, potentials, applyAllStat)
					print("{}: {}/{}".format(target_list[0], amount, min_amount))

					if amount >= min_amount:
						self.logText(countText)
						print("Success !!")
						retry = input("manual re-potential one time then type 'Y' to continue:")
						if retry.lower() != "y":
							return
						else:
							self.countdown(3)
							break
				self.logText(countText)
				self.trigger()
				count = count + 1
				if maxCount > 0 and count > maxCount:
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
			print("Press any key on preview window to continue...")
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
	
	def getAmountFromTargetList(self, target_list: list, potentials: list, applyAllStat: bool):
		amount = 0
		for potential in potentials.copy():
			if applyAllStat and target_list[0] in MAIN_STAT_LIST:
				potential['value'] = potential['value'].replace("All Stats", target_list[0])

			have_all_word = all(ele in potential['value'] for ele in target_list)
			check_start_word = potential['value'].startswith(target_list[0])

			if have_all_word and check_start_word:
				amount = amount + 1
		return amount


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
	
	def getCountText(self, count, maxCount) -> str:
		return "count: {count:,}/{max_count} ({nx:,} NX)".format(
			count = count, 
			max_count = "unlimited" if maxCount < 0 else "{:,}".format(maxCount), 
			nx = count * 1200
			)
	
	def clearConsole(self):
		os.system('cls' if os.name == 'nt' else 'clear')
