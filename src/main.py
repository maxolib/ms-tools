from item_potential import ItemPotential

# preview setting
crop = {'left': 300, 'top': 350, 'width': 350, 'height': 150}

# add keys for searching each line (multi-key split by ",")
target_potential_list = {
	"Item Drop Rate, %": 2,
	"Critical Damage, %": 2,
	"ATT, %": 3,
}

# run 
if __name__ == "__main__":
	itemPotential = ItemPotential(crop=crop)
	itemPotential.lookingPotential(
		targetDict = target_potential_list,
		# useCalibrate = False,
		# max_count = -1,
	)