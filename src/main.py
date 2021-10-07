from item_potential import ItemPotential

crop = {'left': 300, 'top': 350, 'width': 350, 'height': 150}

target_potential_list = {
	"Item Drop Rate, %": 2,
	"ATT, %": 3,
	"All Stats, %": 3
}

itemPotential = ItemPotential(crop=crop)
itemPotential.lookingPotential(target_potential_list)