from enum import Enum
import utils

class Character:
    
    def __init__(self, name, lvl, hp, race, scores, _weapon, _armor):
        """
        name - str : character name
        lvl - int : character level
        hp - int : character base hp
        scores - int list : character ability scores in order
        race - str : race TODO: make a class
        cclass - CClass: class TODO allow for multiclassing
        
        _weapon - Weapon : character's current weapon
        _armor - Armor : character's current armor
        alignment - str : character's alignment
        picked_skills - str list : character's known skills (+3 to skill)
        
        """
        self.name = name
        self.lvl = lvl
        self.xp = 0
        self.base_hp = hp
        self.cur_hp = hp
        self.race = race
        self.weapons = {}
        self.cur_weapon = _weapon
        self.add_weapon(_weapon)
        self.armor = {}
        self.cur_armor = _armor
        self.add_armor(_armor)
        
        mods = [utils.bonus(score) for score in scores]
        self.abilities = {}
        self.abilities[Ability.STR.value] = mods[0]
        self.abilities[Ability.DEX.value] = mods[1]
        self.abilities[Ability.CON.value] = mods[2]
        self.abilities[Ability.INT.value] = mods[3]
        self.abilities[Ability.WIS.value] = mods[4]
        self.abilities[Ability.CHA.value] = mods[5]
        
        self.ac = self.cur_armor.get_ac() + self.abilities[Ability.DEX.value]
        self.passive_perception = 10
        self.proficiency = utils.get_proficiency(lvl)
        
    def save_character(self):
        utils.save_character(self)
        
    def add_armor(self, _armor):
        self.armor[_armor.name] = _armor

    def add_weapon(self, _weapon):
        self.weapons[_weapon.name] = _weapon
        
    def get_mod(self, ab):
        return self.abilities[ab.value] + self.proficiency
    
    def take_damage(self, damage):
        self.cur_hp -= damage
        if self.cur_hp <= -self.base_hp:
            print(self.name, "dies.")
        elif self.cur_hp <= 0:
            print(self.name, "falls unconscious.")
            
    def to_json(self):
        return dict(abilities=self.abilities, name=self.name,
                    lvl=self.lvl, xp=self.xp, base_hp=self.base_hp,
                    cur_hp=self.cur_hp, race=self.race, ac=self.ac,
                    proficiency=self.proficiency,
                    weapons=self.weapons, armor=self.armor, 
                    cur_weapon=self.cur_weapon, cur_armor=self.cur_armor)
                    
        
class Playable(Character):
    def __init__(self, name, lvl, hp, race, scores, dndclass, _weapon, _armor, alignment, picked_skills):
        
        super().__init__(name, lvl, hp, race, scores, _weapon, _armor)
        self.alignment = alignment
        self.skills = picked_skills
        self.dndclass = dndclass
        self.inventory = []
        self.spells = []
        

    def ati(self, item):
        self.inventory.append(item)
        
    def learn_spell(self, name, description):
        self.spells.append(Spell(name, description))
        
    def level_up(self, hit_die):
        self.base_hp += hit_die + (self.get_mod(Ability.CON) - self.proficiency)
        self.cur_hp = self.base_hp
        self.lvl += 1
        self.proficiency = utils.get_proficiency(self.lvl)
        
        #Add spells learned manually

class Ability(Enum):
    STR = 1
    DEX = 2
    CON = 3
    INT = 4
    WIS = 5
    CHA = 6
    
    
class Skills(Enum):
    Athletics = 1
    Acrobatics = 2
    SleightofHand = 3
    Stealth = 4
    Arcana = 5
    History = 6
    Investigation = 7
    Nature = 8
    Religion = 9
    AnimalHandling = 10
    Insight = 11
    Medicine = 12
    Perception = 13
    Survival = 14
    
    Deception = 15
    Intimidation = 16
    Performance = 17
    Persuasion = 18
    
    
class Spell:
    
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        
    def to_json(self):
        return dict(name=self.name, desc=self.desc)
        
class Weapon():
    
    def __init__(self, name, atktyp='melee', droll='2d4', dtype='slashing'):
        self.name = name
        self.atktype = atktyp
        self.droll = droll
        self.dtype = dtype
        
    def to_json(self):
        return dict(name=self.name, atktype=self.atktype, droll=self.droll, dtype=self.dtype)
class Armor():
    
    def __init__(self, name, baseac=12, weight='light'):
        self.name = name
        self.baseac=baseac
        self.weight=weight
        
    def get_ac(self):
        return self.baseac
    
    def to_json(self):
        return dict(name=self.name, baseac=self.baseac, weight=self.weight)

