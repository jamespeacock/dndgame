import Character
from Character import *

class Session:
    
    def __init__(self):
        self.characters = {}
        self.players = {} 
    
    def add_character(self, char):
        if type(char) == Character:
            self.characters[char.name] = char
            print("Added character", char.name)
        elif type(char) == Playable:
            self.players[char.name] = char
            print("Added player", char.name)
        else:
            print("Could not add non Character with type", type(char))
        
    def add_players(self, players):
        for player in players:
            self.add_character(player)
        
    ### GAMEPLAY

    def attack(self, attacker, defender, atk_roll, dam_roll):
        if attacker.cur_weapon.atktype == 'melee':
            atk = atk_roll + attacker.get_mod(Ability.STR)
            damage = dam_roll + attacker.get_mod(Ability.STR)
        else:
            atk = atk_roll + attacker.get_mod(Ability.DEX)
            damage = dam_roll + attacker.get_mod(Ability.DEX)
        
        
        if atk >= defender.ac:
            print(utils.hit(attacker))
            defender.take_damage(damage)
        elif atk_roll == 20:
            print(utils.crit(attacker))
            defender.take_damage(damage + dam_roll)
        else:
            print(utils.miss(attacker))
            
            
    def cast_spell(self, caster, spell_dc, defender, dc_roll, modifier=Ability.CON):
        
        if defender.get_mod(modifier) + dc_roll >= spell_dc:
            print(utils.miss('spell', caster))
        else:
            print(utils.hit('spell', caster))
            
    def skillcheck(self, player, skill, roll, difficulty):
        check = difficulty.value
        if skill.value == 1:
            roll += player.get_mod(Ability.STR)
        elif skill.value > 1 and skill.value < 5:
            roll += player.get_mod(Ability.DEX)
        elif skill.value > 4 and skill.value < 10:
            roll += player.get_mod(Ability.INT)
        elif skill.value > 9 and skill.value < 15:
            roll += player.get_mod(Ability.WIS)
        else:
            roll += player.get_mod(Ability.CHA)

        if skill in player.skills:
            roll += 3
        
        if roll >= check:
            print("Success.")
        else:
            print("Failure.")
            
            
class Difficulty(Enum):
    EASY = 5
    MEDIUM = 10
    HARD = 15
    VERYHARD = 20
    EXTREME = 25