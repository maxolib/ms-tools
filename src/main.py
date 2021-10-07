from item_potential import ItemPotential

crop = {'left': 300, 'top': 350, 'width': 350, 'height': 150}

lookingDict = {
	"Item Drop Rate": 2,
	"LUK": 2,
	"All Stats": 2
}

itemPotential = ItemPotential(crop=crop)
itemPotential.lookingPotential(lookingDict)