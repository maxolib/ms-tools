from item_potential import ItemPotential

# preview window setting
crop = {'left': 300, 'top': 350, 'width': 350, 'height': 150}

# KEY - keyword for searching each line (multi-key split by ",")
# VALUE - line amount
target_potential_list = {
	"Item Drop Rate, %": 3,
	"Critical Damage, %": 2,
	"ATT, %": 3,
}

# run 
if __name__ == "__main__":
	itemPotential = ItemPotential(crop=crop)
	itemPotential.findingPotential(
		targetDict = target_potential_list,
		useCalibrate = True, # enable/disable calibration step
		applyAllStat = True, # use/unsed all state as a main stat
		maxCount = -1, # set maximum count (unlimited is -1)
	)