import math
import json
import pickle
### Gameplay messages


# Have saved messages with format fillers for weapons or character race in a file
# load the messages from a file and choose one randomly for more excitement.
def hit(chrctr):
    typ = chrctr.cur_weapon.atktype
    if typ == 'melee':
        return 'Attack Success. You deal damage with your sword'
    
    elif typ == 'ranged':
        return 'Attack Success. You deal damage with your bow'
    
    elif typ == 'spell':
        return 'Spell Success. Follow up with effects.'
    
    return 'Success.'

def miss(chrctr):
    return 'You suck and you missed.'

### Saving and loading characters
class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj,'to_json'):
            return dict(obj.to_json())
        else:
            return json.JSONEncoder.default(self, obj)

def save_character(character):
    #pickle.dump(character, open(character.name+'_bin.txt', 'wb'))
    char_str = json.dumps(character.to_json(), cls=ComplexEncoder)
    print(char_str)
    save_to_file(str(char_str), character.name+'_str.txt')

def save_to_file(char_string, filename):
    f = open(filename, 'w')
    f.write(char_string)
    f.close()
    print("Saved character to " + filename)
    
def bonus(score):
    return math.floor((score - 10)/2)

def get_proficiency(lvl):
    return lvl/4 + 2