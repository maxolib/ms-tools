from item_potential import ItemPotential

crop = {'left': 300, 'top': 350, 'width': 350, 'height': 150}
lines = [ 
	{ "start": (0, 58), "end": (2000, 58)},
	{ "start": (0, 76), "end": (2000, 76)},
	{ "start": (0, 94), "end": (2000, 94)},
]

lookingDict = {
	"Item Drop Rate": 2,
	"ATT": 2,
	"LUK": 2,
	"All Stats": 2
}

itemPotential = ItemPotential(crop=crop, lines=lines)
# itemPotential.CheckCrop()
itemPotential.lookingPotential(lookingDict)