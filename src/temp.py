# "Calibration, please check your text in console."
# "Click here to continue..."
# "auto-cube will start in 3 seconds" "3" "2" "1"
# ---------------------------------------------------
import re
NORMAL_POTENTIAL_REX = r"[ ]*\((?P<rarity>.+)\)[ ]*(?P<name>.+)[ ]*:[ ]*(?P<value>.+)[ ]*"
target_potential_list: list = [
    { "LUK%": 2},
    { "LUK%": 2},
]

default_text = ""
with open('default_text.txt') as f:
    default_text = f.read()

def getPotentials(text: str) -> list: 
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

def matchPotentials(target_list: list, potentials: list) -> bool:
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

# getPotentials(default_text)
matchPotentials(target_potential_list, [])


