# Installation
1. install tesseract from [link](https://github.com/UB-Mannheim/tesseract/wiki)
2. check path in `item_potential.py`
	``` python
	pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
	```
3. install Python v3.6 or newer
3. install library
	```
	pip install -r requirements.txt
	```

# How to use
1. set `target_potential_list` 
	- `KEY` - keyword for searching each line (multi-key split by ",")
	- `VALUE` - line amount
	``` python
	target_potential_list = {
		"Item Drop Rate, %": 3,
		"Critical Damage, %": 2,
		"ATT, %": 3,
	}
	```
2. run `main.py`
	```
	python src/main.py
	```
2. move maple window for calibrating then click anykey in preview window
3. click at maple window and wait 3 seconds