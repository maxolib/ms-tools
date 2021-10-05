# Installation
1. install tesseract from [link](https://github.com/UB-Mannheim/tesseract/wiki)
2. check path in `item_potential.py`
	``` python
	pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
	```
	>> 
3. install library requirements
	```
	pip install -r requirements.txt
	```

# How to use
1. calibration ROI and override lines below text
	``` python
	from item_potential import ItemPotential

	crop = {'left': 500, 'top': 500, 'width': 350, 'height': 150}
	lines = [ 
		{ "start": (0, 58), "end": (2000, 58)},
		{ "start": (0, 76), "end": (2000, 76)},
		{ "start": (0, 94), "end": (2000, 94)},
	]
	itemPotential = ItemPotential(crop=crop, lines=lines)
	itemPotential.CheckCrop()
	```
2. looking some potential
	``` python
	from item_potential import ItemPotential

	lookingDict = {
		"Item Drop Rate": 2,
		"ATT": 2,
		"LUK": 2,
		"All Stats": 2
	}

	itemPotential = ItemPotential(crop=crop, lines=lines)
	itemPotential.lookingPotential(lookingDict)
	```