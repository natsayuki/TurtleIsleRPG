import pygame
from threading import Thread
from time import sleep,time
from random import randint,uniform,choice
import PyCon
from Functions import *
from string import *
from math import ceil,floor
from textwrap import wrap,fill
from PIL import Image

########
# init #
########
pygame.init()
color = (255,255,255)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1000,650))
screen_rect = pygame.Rect((0, 0), (1000, 650))
game_map = pygame.image.load("images\\testmap.png")
pygame.display.set_caption("Turtle Isle RPG")

#################
# sprite groups #
#################

sprites_list = pygame.sprite.Group()
party = pygame.sprite.Group()
mobs_list = pygame.sprite.Group()
mob_fight = pygame.sprite.Group()
party_list = pygame.sprite.Group()
general_sprites = pygame.sprite.Group()
attack_menu = pygame.sprite.Group()
turnalert_list = pygame.sprite.Group()
equipment_list = pygame.sprite.Group()

###########
# classes #
###########
class base_sprite(pygame.sprite.Sprite): #turtle spawned in middle of screen
        def __init__(self, color=(0,0,0), width=0, height=0, image=None,health=100,x=0,y=0):
            pygame.sprite.Sprite.__init__(self)
            if "Surface" in type(image).__name__:
                self.image = image
            else:
                self.image = pygame.image.load(image)
            pygame.draw.rect(self.image, color, [5000000,5000000,width,height])
            self.rect = self.image.get_rect()
            self.health = health
            self.rect.x = x
            self.rect.y = y



class mob_class(pygame.sprite.Sprite): #turtle spawned in middle of screen
        def __init__(self, name, color=(0,0,0), width=0, height=0, image=None,health=100):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(image)
            pygame.draw.rect(self.image, color, [5000000,5000000,width,height])
            self.rect = self.image.get_rect()
            self.health = health
            self.name = name
        def move(self, diri, amount):
            exec('self.rect.' + diri + ' += ' + str(amount))

        def attack(self): #todo
            pass


class entity():

    class playerCharacter(pygame.sprite.Sprite):
        def __init__(self, name, initHealth, initAttack, initdefence, initStrength, initMagic, initmagic, initSpeed, initLevel, initExp, maxHealth, head, torso, feet, hand, image):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(image)
            pygame.draw.rect(self.image, (0,0,0), [5000000,5000000,0,0])
            self.rect = self.image.get_rect()
            self.name = name
            self.health = initHealth
            self.attack = initAttack
            self.defence = initdefence
            self.strength = initStrength
            self.magic = initMagic
            self.magic = initmagic
            self.speed = initSpeed
            self.level = initLevel
            self.exp = initExp
            self.isAlive = True
            self.maxHealth = maxHealth
            self.head = head
            self.torso = torso
            self.feet = feet
            self.hand = hand
            self.effects = {'burned': [False, [4, 8], 0], 'frozen': [False, [2, 4], 0], 'confused': [False, [6, 10], 0]}
            self.levelTree = {'attack': 1, 'defence': 1, 'strength': 1, 'magic': 1, 'speed': 1, 'maxHealth': 1}
            self.tempBuffs = {'attack': 0, 'defence': 0, 'strength': 0, 'magic': 0, 'speed': 1, 'maxHealth': 0}
        def learnSkill(self, learn, forget):
            for i in self.abilities:
                # self.abilities = {'Basic Attack': [self.basicAttack, 0, 0], 'Bite': [self.bite, 3, 0], 'Splash': [self.splash, 9001, 0], 'Self Heal': [self.selfHeal, 3, 0]}
                None
                '''
                if (self.abilities[i])[0] == forget:

                '''
        def buff(self, stat, amount):
            exec('self.' + stat + ' += ' + str(amount))
            self.tempBuffs[stat] += amount
            return [stat, amount]
        def handleBuffs(self):
            for i in self.tempBuffs:
                exec('self.' + i + ' -= ' + str(self.tempBuffs[i]))
                self.tempBuffs[i] = 0
        def inflictEffect(self, effect):
            for i in self.effects:
                (self.effects[i])[0] = False
            effect = self.effects[effect]
            effect[0] = True
            effect[2] = randint((effect[1])[0], (effect[1])[1])
        def handleEffects(self):
            for effect in self.effects:
                effectList = self.effects[effect]
                if effectList[0]:
                    effectList[2] -= 1
                    if effectList[2] <= 0:
                        effectList[0] = False
                    if effect == 'burned':
                        burndamage = ceil(self.maxHealth * (5/100))
                        self.trueDamage(burndamage)
                        return [False, f'Your turtle has taken {burndamage} damage from burn']
                    elif effect == 'frozen':
                        return [True, 'Your turtle is frozen']
                    elif effect == 'confused':
                        if randint(1, 2) == 1:
                            self.trueDamage(15) # TODO change fixed damage here
                            return [True, 'Your turtle has damged itself for 15 from confusion']

            return [False]

        def move(self, diri, amount):
            exec('self.rect.' + diri + ' += ' + str(amount))

        def levelUp(self, amount):
            self.level += amount
            for i in self.levelTree:
                exec('self.' + i + ' += ' + str((ceil(self.levelTree[i] * self.level))))
            for i in self.skillTree:
                if i == self.level:
                    return self.skillTree[i]
            return self.level
        def checkExp(self):
            if self.exp >= self.level*5:
                self.levelUp(1)
                self.exp = self.exp - self.level*5
                self.checkExp()
        def expUp(self, amount):
            self.exp += amount
            self.checkExp()
            return self.exp
        def trueDamage(self, amount):
            self.health -= ceil(amount)
            if self.health <= 0:
                self.health = 0
                self.isAlive = False
            return ceil(amount)
        def damage(self, amount):
            return self.trueDamage(amount / ((randint(3, 4) * self.defence)/100))
        def heal(self, amount):
            self.health += amount
            if self.health > self.maxHealth:
                self.health = self.maxHealth
            return self.health
        def equip(self, item):
            if type(item).__name__ == 'equipable':
                for i in item.effects:
                    exec('self.' + i + ' += ' + str(item.effects[i]))
                exec('self.' + item.type + ' = item')
                return True
            return False
        def unequip(self, type):
            if eval('self.' + type) != None:
                item = eval('self.' + type)
                for i in item.effects:
                    exec('self.' + i + ' -= ' + str(item.effects[i]))
                exec('self.' + type + ' = None')
                return item
            return False
        def consume(self, item):
            if type(item).__name__ == 'consumable':
                if item.effects[0] == 'perm':
                    for index, i in enumerate(item.effects[1], 0):
                        exec('self.' + i + ' += ' + str(item.effects[i]))
                    return True
                elif item.effects[0] == 'temp':
                    if fight:
                        for i in item.effects[1]:
                            return self.buff(i, (item.effects[1])[i])
                    else:
                        return False
            return False
        def calcAttackDamage(self):
            return randint(self.strength, self.strength+int((.5*self.attack)))
        def Attack(self, character):
            if type(character).__name__ == 'enemyCharacter' or type(character).__name__ == 'playerCharacter':
                return character.damage(self.calcAttackDamage())
            return False
        def listSelf(self):
            temp = {}
            for i in ['head', 'torso', 'feet', 'hand']:
                try:
                    temp[i] = eval('self.' + i + '.name')
                except:
                    temp[i] = eval('self.' + i)
            return temp
        def listStats(self):
                return {'health': self.health, 'attack': self.attack, 'strength': self.strength, 'defence': self.defence, 'magic': self.magic, 'speed': self.speed}
        def listLevel(self):
            return {'level': self.level, 'exp': self.exp}


    class enemyCharacter(pygame.sprite.Sprite):
        def __init__(self, name, health, attack, defence, strength, magic, speed, level, maxHealth, isAlive, head, torso, feet, hand, image):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(image)
            pygame.draw.rect(self.image, (0,0,0), [5000000,5000000,0,0])
            self.rect = self.image.get_rect()
            self.health = health
            self.attack = attack
            self.defence = defence
            self.strength = strength
            self.magic = magic
            self.speed = speed
            self.level = level
            self.maxHealth = maxHealth
            self.isAlive = isAlive
            self.head = head
            self.torso = torso
            self.feet = feet
            self.hand = hand
            self.name = name
            self.effects = {'burned': [False, [4, 8], 0], 'frozen': [False, [2, 4], 0], 'confused': [False, [6, 10], 0]}
            self.tempBuffs = {'attack': 0, 'defence': 0, 'strength': 0, 'magic': 0, 'speed': 1, 'maxHealth': 0}
        def buff(self, stat, amount):
            exec('self.' + stat + ' += ' + str(amount))
            self.tempBuffs[stat] += amount
        def handleBuffs(self):
            for i in self.tempBuffs:
                exec('self.' + i + ' -= ' + self.tempBuffs[i])
                self.tempBuffs[i] = 0
        def inflictEffect(self, effect):
            for i in self.effects:
                (self.effects[i])[0] = False
            effect = self.effects[effect]
            effect[0] = True
            effect[2] = randint((effect[1])[0], (effect[1])[1])
        def handleEffects(self):
            for effect in self.effects:
                effectList = self.effects[effect]
                if effectList[0]:
                    effectList[2] -= 1
                    if effectList[2] <= 0:
                        effectList[0] = False
                    if effect == 'burned':
                        burndamage = ceil(self.maxHealth * (5/100))
                        self.trueDamage(burndamage)
                        return [False, f'{self.name} has taken {burndamage} damage from burn']
                    elif effect == 'frozen':
                        return [True, f'{self.name} is frozen']
                    elif effect == 'confused':
                        if randint(1, 2) == 1:
                            self.trueDamage(15) # TODO change fixed damage here
                            return [True, f'{self.name} has damged itself for 15 from confusion']

            return [False]

        def calcAttackDamage(self):
            return randint(self.strength, self.strength+int((.5*self.attack)))
        def Attack(self, entity):
            if randint(0, self.attack) != 0:
                return [[entity.damage(self.calcAttackDamage()), 'player', 'damaged', None]]
            return [[0, 'player', 'damaged', None]]
        def trueDamage(self, amount):
            self.health -= ceil(amount)
            if self.health <= 0:
                self.health = 0
                self.isAlive = False
            return ceil(amount)
        def damage(self, amount):
            return self.trueDamage(amount / ((randint(3, 4) * self.defence)/100))
        def heal(self, amount):
            self.health += amount
            if self.health > self.maxHealth:
                self.health = self.maxHealth
        def equip(self, item):
            if type(item).__name__ == 'equipable':
                for i in item.effects:
                    exec('self.' + i + ' += ' + str(item.effects[i]))
                exec('self.' + item.type + ' = item')
                return True
            return False
        def unequip(self, type):
            if eval('self.' + type) != None:
                item = eval('self.' + type)
                for i in item.effects:
                    exec('self.' + i + ' -= ' + str(item.effects[i]))
                exec('self.' + type + ' = None')
                return item
            return False
        def listSelf(self):
            temp = {}
            for i in ['head', 'torso', 'feet', 'hand']:
                try:
                    temp[i] = eval('self.' + i + '.name')
                except:
                    temp[i] = eval('self.' + i)
            return temp
        def listStats(self):
            return {'health': self.health, 'attack': self.attack, 'strength': self.strength, 'defence': self.defence, 'magic': self.magic, 'speed': self.speed}

    class item():
        # effects will take a dictionary eg:
        # {'heath': '10', 'attack': '5'}
        class equipable():
            def __init__(self, name, description, type, effects, image):
                self.name = name
                self.description = description
                self.type = type
                self.effects = effects
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.image.load(image)
                pygame.draw.rect(self.image, (0,0,0), [5000000,5000000,0,0])
                self.rect = self.image.get_rect()
        class consumable(pygame.sprite.Sprite):
            def __init__(self, name, description, effects, image):
                self.name = name
                self.description = description
                self.effects = effects
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.image.load(image)
                pygame.draw.rect(self.image, (0,0,0), [5000000,5000000,0,0])
                self.rect = self.image.get_rect()
        class keyItem(pygame.sprite.Sprite):
            def __init__(self, name, image):
                self.name = name
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.image.load(image)
                pygame.draw.rect(self.image, (0,0,0), [5000000,5000000,0,0])
                self.rect = self.image.get_rect()
class smallTurtle(entity.playerCharacter):
    def __init__(self, name, initHealth, initAttack, initdefence, initStrength, initMagic, initSpeed, initLevel, initExp, maxHealth, head, torso, feet, hand, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        pygame.draw.rect(self.image, (0,0,0), [5000000,5000000,0,0])
        self.rect = self.image.get_rect()
        self.name = name
        self.health = initHealth
        self.attack = initAttack
        self.defence = initdefence
        self.strength = initStrength
        self.magic = initMagic
        self.speed = initSpeed
        self.level = initLevel
        self.exp = initExp
        self.isAlive = True
        self.maxHealth = maxHealth
        self.head = head
        self.torso = torso
        self.feet = feet
        self.hand = hand
        self.abilities = {'Basic Attack': [self.basicAttack, 0, 0], 'Bite': [self.bite, 3, 0], 'Splash': [self.splash, 9001, 0], 'Self Heal': [self.selfHeal, 3, 0]}
        self.effects = {'burned': [False, [4, 8], 0], 'frozen': [False, [2, 4], 0], 'confused': [False, [6, 10], 0]}
        self.levelTree = {'attack': 2, 'defence': 2, 'strength': 2, 'magic': 2, 'speed': 2, 'maxHealth': 2}
        self.tempBuffs = {'attack': 0, 'defence': 0, 'strength': 0, 'magic': 0, 'speed': 1, 'maxHealth': 0}
        self.skillTree = {0: [self.basicAttack, 0, 0], 0: [self.bite, 3, 0], 0: [self.splash, 9001, 0], 0: [self.selfHeal, 3, 0], 5: [self.shellTuck, 3, 0]}

    def tickDown(self):
        for i in self.abilities:
            (self.abilities[i])[2] -= 1
            if (self.abilities[i])[2] < 0:
                (self.abilities[i])[2] = 0
    def basicAttack(self, character):
        self.tickDown()
        return [[self.Attack(character), 'enemy', 'damaged', None]]
    def bite(self, character, name = 'Bite'):
        if (self.abilities[name])[2] == 0:
            self.tickDown()
            (self.abilities[name])[2] = (self.abilities[name])[1]
            return [[character.trueDamage(2*self.attack), 'enemy', 'damaged', None]]
        return False
    def splash(self, character, name = 'Splash'):
        if (self.abilities[name])[2] == 0:
            self.tickDown()
            (self.abilities[name])[2] = (self.abilities[name])[1]
            return [[character.trueDamage(0), 'enemy', 'damaged', None]]
        return False
    def selfHeal(self, character, name = 'Self Heal'):
        if (self.abilities[name])[2] == 0:
            self.tickDown()
            (self.abilities[name])[2] = (self.abilities[name])[1]
            return [[self.heal(25), 'self', 'healed', None]]
        return False
    def shellTuck(self, character, name = 'Shell Tuck'):
        if (self.abilities[name])[2] == 0:
            self.tickDown()
            (self.abilities[name])[2] = (self.abilities[name])[1]
            return [[self.buff('defence', 10), 'self', 'buffed', None]]
        return False

class ninjaTurtle(entity.playerCharacter):
    def __init__(self, name, initHealth, initAttack, initdefence, initStrength, initMagic, initSpeed, initLevel, initExp, maxHealth, head, torso, feet, hand, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        pygame.draw.rect(self.image, (0,0,0), [5000000,5000000,0,0])
        self.rect = self.image.get_rect()
        self.name = name
        self.health = initHealth
        self.attack = initAttack
        self.defence = initdefence
        self.strength = initStrength
        self.magic = initMagic
        self.speed = initSpeed
        self.level = initLevel
        self.exp = initExp
        self.isAlive = True
        self.maxHealth = maxHealth
        self.head = head
        self.torso = torso
        self.feet = feet
        self.hand = hand
        self.abilities = {'Basic Attack': [self.basicAttack, 0, 0], 'Super Sneaky Strike': [self.superSneakyStrike, 5, 0], 'Ninja Star': [self.ninjaStar, 5, 0], 'Ogre Smash': [self.ogreSmash, 0, 0]}
        self.effects = {'burned': [False, [4, 8], 0], 'frozen': [False, [2, 4], 0], 'confused': [False, [6, 10], 0]}
        self.levelTree = {'attack': 1, 'defence': .2, 'strength': .5, 'magic': .1, 'speed': 1, 'maxHealth': .4}
        self.tempBuffs = {'attack': 0, 'defence': 0, 'strength': 0, 'magic': 0, 'speed': 1, 'maxHealth': 0}
        self.skillTree = {0: [self.basicAttack, 0, 0], 0: [self.superSneakyStrike, 5, 0], 0: [self.ninjaStar, 5, 0], 0: [self.ogreSmash, 0, 0], 5: [self.switcheroo, 3, 0]}

    def tickDown(self):
        for i in self.abilities:
            (self.abilities[i])[2] -= 1
            if (self.abilities[i])[2] < 0:
                (self.abilities[i])[2] = 0
    def basicAttack(self, character):
        self.tickDown()
        return [[self.Attack(character), 'enemy', 'damaged', None]]
    def superSneakyStrike(self, character, name = 'Super Sneaky Strike'):
        if (self.abilities[name])[2] == 0:
            self.tickDown()
            (self.abilities[name])[2] = (self.abilities[name])[1]
            return [[character.trueDamage(self.calcAttackDamage()), 'enemy', 'damaged', None]]
        return False
    def ninjaStar(self, character, name = 'Ninja Star'):
        if (self.abilities[name])[2] == 0:
            self.tickDown()
            (self.abilities[name])[2] = (self.abilities[name])[1]
            if randint(1, 2) == 1:
                return [[character.damage(1.5*self.calcAttackDamage()), 'enemy', 'damaged', None]]
            return [[character.trueDamage(0), 'enemy', 'damaged', None]]
        return False
    def ogreSmash(self, character, name = 'Ogre Smash'):
        if (self.abilities[name])[2] == 0:
            self.tickDown()
            (self.abilities[name])[2] = (self.abilities[name])[1]
            return [[character.damage(self.attack*9001), 'enemy', 'damaged', None]]
        return False
    def switcheroo(self, character, name = 'Switcheroo'):
        if (self.abilities[name])[2] == 0:
            self.tickDown()
            (self.abilities[name])[2] = (self.abilities[name])[1]
            return [[self.buff('defence', acitve_mob.defence - self.defence), 'self', 'buffed', None], [active_mob.buff('defence', -(acitve_mob.defence - self.defence)), 'enemy', 'debuffed', None]]
        return False

class wizardTurtle(entity.playerCharacter):
    def __init__(self, name, initHealth, initAttack, initdefence, initStrength, initMagic, initSpeed, initLevel, initExp, maxHealth, head, torso, feet, hand, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        pygame.draw.rect(self.image, (0,0,0), [5000000,5000000,0,0])
        self.rect = self.image.get_rect()
        self.name = name
        self.health = initHealth
        self.attack = initAttack
        self.defence = initdefence
        self.strength = initStrength
        self.magic = initMagic
        self.speed = initSpeed
        self.level = initLevel
        self.exp = initExp
        self.isAlive = True
        self.maxHealth = maxHealth
        self.head = head
        self.torso = torso
        self.feet = feet
        self.hand = hand
        self.abilities = {'Basic Attack': [self.basicAttack, 0, 0], 'Attack Spell': [self.attackSpell, 1, 0], 'Strength Spell': [self.strengthSpell, 1, 0], 'Defence Spell': [self.defenceSpell, 1, 0]}
        self.effects = {'burned': [False, [4, 8], 0], 'frozen': [False, [2, 4], 0], 'confused': [False, [6, 10], 0]}
        self.levelTree = {'attack': .1, 'defence': .3, 'strength': .1, 'magic': 3, 'speed': .4, 'maxHealth': .5}
        self.tempBuffs = {'attack': 0, 'defence': 0, 'strength': 0, 'magic': 0, 'speed': 1, 'maxHealth': 0}
        self.skillTree = {0: [self.basicAttack, 0, 0], 0: [self.attackSpell, 1, 0], 0: [self.strengthSpell, 1, 0], 0: [self.defenceSpell, 1, 0], 5: [self.mysteryForce, 4, 0]}

    def tickDown(self):
        for i in self.abilities:
            (self.abilities[i])[2] -= 1
            if (self.abilities[i])[2] < 0:
                (self.abilities[i])[2] = 0
    def basicAttack(self, character):
        self.tickDown()
        return [[self.Attack(character), 'enemy', 'damaged', None]]
    def attackSpell(self, character, name = 'Attack Spell'):
        if (self.abilities[name])[2] == 0:
            self.tickDown()
            (self.abilities[name])[2] = (self.abilities[name])[1]
            character.inflictEffect('burned')
            return [[character.damage(self.attack + self.magic), 'enemy', 'damaged', 'burned']]
        return False
    def strengthSpell(self, character, name = 'Strength Spell'):
        if (self.abilities[name])[2] == 0:
            self.tickDown()
            (self.abilities[name])[2] = (self.abilities[name])[1]
            character.inflictEffect('frozen')
            return [[character.damage(self.strength + self.magic), 'enemy', 'damaged', 'frozen']]
        return False
    def defenceSpell(self, character, name = 'Defence Spell'):
        if (self.abilities[name])[2] == 0:
            self.tickDown()
            (self.abilities[name])[2] = (self.abilities[name])[1]
            character.inflictEffect('confused')
            return [[character.damage(self.defence + self.magic), 'enemy', 'damaged', 'confused']]
        return False
    def mysteryForce(self, character, name = 'Mystery Force'):
        if (self.abilities[name])[2] == 0:
            self.tickDown()
            (self.abilities[name])[2] = (self.abilities[name])[1]
            return [[self.buff('magic', ceil(self.magic/15)), 'self', 'buffed', None]]

class knightTurtle(entity.playerCharacter):
    def __init__(self, name,  initHealth, initAttack, initdefence, initStrength, initMagic, initSpeed, initLevel, initExp, maxHealth, head, torso, feet, hand, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        pygame.draw.rect(self.image, (0,0,0), [5000000,5000000,0,0])
        self.rect = self.image.get_rect()
        self.name = name
        self.health = initHealth
        self.attack = initAttack
        self.defence = initdefence
        self.strength = initStrength
        self.magic = initMagic
        self.speed = initSpeed
        self.level = initLevel
        self.exp = initExp
        self.isAlive = True
        self.maxHealth = maxHealth
        self.head = head
        self.torso = torso
        self.feet = feet
        self.hand = hand
        self.abilities = {'Basic Attack': [self.basicAttack, 0, 0], 'Hit With Sword': [self.hitWithSword, 5, 0], 'Charge': [self.charge, 10, 0], 'Holy Smite': [self.holySmite, 15, 0]}
        self.effects = {'burned': [False, [4, 8], 0], 'frozen': [False, [2, 4], 0], 'confused': [False, [6, 10], 0]}
        self.levelTree = {'attack': .4, 'defence': .4, 'strength': .4, 'magic': .1, 'speed': .2, 'maxHealth': .3}
        self.tempBuffs = {'attack': 0, 'defence': 0, 'strength': 0, 'magic': 0, 'speed': 1, 'maxHealth': 0}
        self.skillTree = {0: [self.basicAttack, 0, 0], 0: [self.hitWithSword, 5, 0], 0: [self.charge, 10, 0], 0: [self.holySmite, 15, 0], 5: [self.forHonor, 5, 0]}

    def tickDown(self):
        for i in self.abilities:
            (self.abilities[i])[2] -= 1
            if (self.abilities[i])[2] < 0:
                (self.abilities[i])[2] = 0
    def basicAttack(self, character):
        self.tickDown()
        return [[self.Attack(character), 'enemy', 'damaged', None]]
    def hitWithSword(self, character, name = 'Hit With Sword'):
        if (self.abilities[name])[2] == 0:
            self.tickDown()
            (self.abilities[name])[2] = (self.abilities[name])[1]
            return [[character.trueDamage(self.attack*2), 'enemy', 'damaged', None]]
        return False
    def charge(self, character, name = 'Charge'):
        if (self.abilities[name])[2] == 0:
            self.tickDown()
            (self.abilities[name])[2] = (self.abilities[name])[1]
            return [[character.damage(self.strength * 3), 'enemy', 'damaged', None], [self.damage(ceil(.5*self.strength)), 'self', 'damaged', None]]
        return False
    def holySmite(self, character, name = 'Holy Smite'):
        if (self.abilities[name])[2] == 0:
            self.tickDown()
            (self.abilities[name])[2] = (self.abilities[name])[1]
            return [[character.damage(self.magic * 2), 'enemy', 'damaged', None], [self.heal(self.magic), 'self', 'healed', None]]
        return False
    def forHonor(self, character, name = 'For Honor'):
        if (self.abilities[name])[2] == 0:
            self.tickDown()
            (self.abilities[name])[2] = (self.abilities[name])[1]
            return [[self.buff('attack', ceil(self.attack/10)), 'self', 'buffed', None], [self.buff('strength', ceil(self.strength/10)), 'self', 'buffed', None]]
        return False

class text(pygame.sprite.Sprite): #helpful class for rendering text as a sprite
        def __init__(self, text, font_path, font_size, font_colour, x, y, opacity,background=None):
                pygame.sprite.Sprite.__init__(self)
                self.font = pygame.font.SysFont(font_path, font_size)
                self.color = font_colour
                self.render_text = text
                self.rerender(x,y,opacity,background)
                self.pos = y
                self.text = text
                self.opacity = opacity
                self.background = background
        def update(self):
                pass
        def print_text(self, text_string, x, y):
                self.render_text = text_string
                self.rerender(x,y,self.opacity,self.background)
        def rerender(self, x, y, opacity,background):
                self.image = self.font.render(self.render_text, 0, self.color,background)
                self.image.set_alpha(opacity)
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y

##############
# predefined variables #
##############
running = True
gameover = False
positions = []
move = False
direction = "right"
olddirection = "right"
fight = False
active_mob = None
menubool = False
equipmentbool = False
scrollX = 0
backgroundparty = []
placementcounter = 25
selection1 = False
selection2 = False
party_menu_list = []
attack_menu_list = []
turn = True
statsbool = False
temp_list = []
fightover = False
attack_active = False
turnalert = False
passturn = False
button_list = []
equipment_turtle = None


#     def __init__(self, name,  initHealth, initAttack, initdefence, initStrength, initMagic, initSpeed, initLevel, initExp, maxHealth, head, torso, feet, hand, image):

images = ['images\\smallTurtle.png','images\\NinjaTurtle.png','images\\WizardTurtle.png','images\\KnightTurtle.png']
turtle = smallTurtle('Turtle', 50000, 5, 5, 5, 5, 20, 1, 0, 50000, None, None, None, None, image='images\\smallTurtle.png')
ninjaTurtle = ninjaTurtle('Ninja Turtle', 30, 15, 15, 2, 2, 15,  1, 0, 30, None, None, None, None, image='images\\NinjaTurtle.png')
wizardTurtle = wizardTurtle('Wizard Turtle', 45, 5, 10, 5, 30, 20, 1, 0, 45, None, None, None, None, image='images\\WizardTurtle.png')
knightTurtle = knightTurtle('Knight Turtle', 50, 10, 5, 15, 5, 3, 1, 0, 50, None, None, None, None, image='images\\KnightTurtle.png')
turtle.rect.x = 250
turtle.rect.y = 250
ninjaTurtle.rect.x = 250
ninjaTurtle.rect.y = 300
wizardTurtle.rect.x = 250
wizardTurtle.rect.y = 350
knightTurtle.rect.x = 250
knightTurtle.rect.y = 400

############
# CONSUMABLES #
############

healthPotion = entity.item.consumable('Health Potion', 'A small potion that restores 10 health', ['perm', {'health': 10}], 'images\\sprites\\healthPotion.png')
mediumHealthPotion = entity.item.consumable('Medium Health Potion', 'A potion that is slightly larger than a normal Health Potion that restores 75 health', ['perm', {'health': 75}],"images\\sprites\\mediumHealthPotion.png")
bigHealthPotion = entity.item.consumable('Big Health Potion', 'A potion that is significantly larger than a normal Health Potion that restores 200 health', ['perm', {'health': 200}], 'images\\sprites\\bigHealthPotion.png')
giantHealthPotion = entity.item.consumable('Giant Health Potion', 'A potion that dwarfes a normal Health Potion in comparison that restores an amount of health that is over 9000', ['perm', {'health': 9001}], 'images\\sprites\\giantHealthPotion.png')

attackUp = entity.item.consumable('Attack Up', 'A small tablet the permanatley increases your attack by 10', ['perm', {'attack': 10}], 'images\\sprites\\attackUp.png')
strengthUp = entity.item.consumable('Strength Up', 'A small tablet the permanatley increases your strength by 10', ['perm', {'strength': 10}],"images\\sprites\\strengthUp.png")
defenceUp = entity.item.consumable('Defence Up', 'A small tablet the permanatley increases your defence by 10', ['perm', {'defence': 10}], 'images\\sprites\\defenceUp.png')
magicUp = entity.item.consumable('Magic Up', 'A small tablet the permanatley increases your magic by 10', ['perm', {'magic': 10}], 'images\\sprites\\magicUp.png')
maxHealthUp = entity.item.consumable('Max Health Up', 'A small tablet the permanatley increases your max health by 10', ['perm', {'maxHealth': 10}],"images\\sprites\\maxHealthUp.png")

expOrb = entity.item.consumable('EXP Orb', 'Test your luck', ['perm', {'exp': randint(1, 100)}], 'images\\sprites\\expOrb.png')

attackBoost = entity.item.consumable('Attack Boost', 'Temporarily boost your attack in a fight', ['temp', {'attack': 25}], 'images\\sprites\\attackUp.png')
strengthBoost = entity.item.consumable('Strength Boost', 'Temporarily boost your strength in a fight', ['temp', {'attack': 25}], 'images\\sprites\\strengthUp.png')
defenceBoost = entity.item.consumable('Defence Boost', 'Temporarily boost your defence in a fight', ['temp', {'attack': 25}], 'images\\sprites\\defenceUp.png')
magicBoost = entity.item.consumable('Magic Boost', 'Temporarily boost your magic in a fight', ['temp', {'attack': 25}], 'images\\sprites\\magicUp.png')
maxHealthBoost = entity.item.consumable('Max Health Boost', 'Temporarily boost your max health in a fight', ['temp', {'attack': 25}], 'images\\sprites\\maxHealthUp.png')





###########
# WEAPONS #
###########

cardboardSword = entity.item.equipable('Cardboard Sword', 'Don\'t take it out in the rain', 'hand', ({'attack': 1, 'strength': 1}), 'images\\sprites\\cardboardSword.png')
greatSwordOfPatker = entity.item.equipable('Great Sword Of Patker', 'This sword was only rumored of... until now', 'hand', ({'attack': 15, 'strength': 15, 'maxHealth': 25}), 'images\\sprites\\greatSwordOfPatker.png')
syphoningSword = entity.item.equipable('Syphoning Sword', 'A sword that draws power from your health', 'hand', ({'attack': 20, 'strength': 10, 'health': -10}), 'images\\sprites\\syphoningSword.png')

stick = entity.item.equipable('Stick', 'What\'s brown and sticky', 'hand', ({'magic': 1}), 'images\\sprites\\stick.png')
showerRod = entity.item.equipable('Shower Rod', 'It used to hold up a shower curtain', 'hand', ({'magic': 5}), 'images\\sprites\\showerRod.png')
nimRod = entity.item.equipable('Nim Rod', 'Simple mach production', 'hand', ({'magic': 13}),"images\\sprites\\nimRod.png")
lightningRod = entity.item.equipable('Lightning Rod', 'Clever joke about Ben Franklin or something', 'hand', ({'magic': 20}), 'images\\sprites\\lightningRod.png')

########
# HEAD #
########

helmOfPatker = entity.item.equipable('Helm Of Patker', 'A great helm for a great leader', 'head', ({'defence': 7}),"images\\sprites\\helmOfPatker.png")
bikeHelmet = entity.item.equipable('Bike Helmet', 'If you wear this you won\'t die in a bike crash', 'head', ({'defence': 5}), 'images\\sprites\\bikeHelmet.png')

#########
# TORSO #
#########

gownsOfPatker = entity.item.equipable('Gowns Of Patker', 'Sacred gowns from the cult of Patker', 'torso', ({'defence': 15}),"images\\sprites\\gownsOfPatker.png")
syphoningSigil = entity.item.equipable('Syphoning Sigil', 'It\'s a piece of garlic', 'torso', ({'attack': 5, 'defence': 5, 'health': -3}), 'images\\sprites\\syphoningSigil.png')
abSuit = entity.item.equipable('Ab Suit', 'The fake muscles don\'t really do much', 'torso', ({'attack': 2, 'strength': 2, 'defence': 2}), 'images\\sprites\\abSuit.png')
bodOfBoasting = entity.item.equipable('Bod Of Boasting', 'Confidence is key', 'torso', ({'attack': 5, 'strength': 5, 'defence': 5, 'magic': 5}), 'images\\sprites\\bodOfBoasting.png')

########
# FEET #
########

sandlesOfPatker = entity.item.equipable('Sandles Of Patker', "They're pretty dumb.", 'feet', ({'defence': 5}), 'images\\sprites\\sandlesOfPatker.png')
crocodilesWithSockodiles = entity.item.equipable('Crocodiles With Sockodiles', 'The cool kids call them crocs with socks', 'feet', ({'defence': 7}), 'images\\sprites\\crocodilesWithSockodiles.png')
stilts = entity.item.equipable('Stilts', 'They leave you more open to attacks', 'feet', ({'defence': -2}), 'images\\sprites\\stilts.png')

partybutton = base_sprite(image="images\\partyButton.png")
partybutton.rect.x = 0
partybutton.rect.y = 0
sprites_list.add(partybutton)

equipmentbutton = base_sprite(image="images\\equipmentButton.png")
equipmentbutton.rect.x = 0
equipmentbutton.rect.y = 50
sprites_list.add(equipmentbutton)

def evaluate(arg):
    """executes code"""
    try:
        return(eval(arg))
    except Exception as e:
        return e

def execute(arg):
    try:
        return(exec(arg))
    except Exception as e:
        return e

def mob():
    spawnmob("foo")


def listEquipSelf():
    return current_turtle.listSelf()

def listStatsSelf():
    return current_turtle.listStats()

def listEquipMob():
    return active_mob.listSelf()

def listStatsMob():
    return active_mob.listStats()

def foobar(effect):
    try:
        if effect == "f":
            active_mob.inflictEffect("frozen")
        elif effect == "b":
            active_mob.inflictEffect("burned")
        elif effect == "c":
            active_mob.inflictEffect("confused")
    except Exception as e:
        print(e)

def passTurn():
    global turn
    turn = False
console = PyCon.PyCon(screen,
                      (0,0,1000,650 / 4),
                      functions = {
                                    "eval":evaluate,
                                    "exec":execute,
                                    "mob":mob,
                                    'listequipself': listEquipSelf,
                                    'liststatsself': listStatsSelf,
                                    'listequipmob': listEquipMob,
                                    'liststatsmob': listStatsMob,
                                    "a":foobar,
                                    'pass': passTurn
                                    },
                      key_calls = {},
                      vari={"A":100,"B":200,"C":300},
                      syntax={re_function:console_func}
                      )

#########################
# basic build functions #
#########################
def buildPartyMenu():
    partymenu = base_sprite(image="images\\partyMenu.png")
    partymenu.rect.x = 0
    partymenu.rect.y = 500
    party_list.add(partymenu)
    global placementcounter
    for enum,i in enumerate(backgroundparty, 0):
        if i.isAlive:
            image = base_sprite(image = images[enum])
        else:
            test = Image.open(images[enum]).convert("LA").convert("RGBA")
            mode = test.mode
            size = test.size
            data = test.tobytes()
            testimage = pygame.image.fromstring(data,size,mode)
            image = base_sprite(image = testimage)
        image.rect.x = placementcounter
        image.rect.y = 510
        texthealth = text(f"{i.name} - Hp: {i.health}/{i.maxHealth}","Comic Sans MS",16,(66, 134, 244),placementcounter-15,593.5,255)
        placementcounter+=250
        party_list.add(image)
        party_list.add(texthealth)
        party_menu_list.append((image,i))

def buildStatMenu():
    global stat_menu
    global mob_self
    stat_menu = base_sprite(image = "images\\partyMenu.png")
    stat_menu.rect.x = 0
    stat_menu.rect.y = 500

    mob_fight.add(stat_menu)

    active_self = active_mob.listSelf()
    temp = 530
    for i in active_self:
        baz = text(i.title() + ': ' + str(active_self[i]), 'Comic Sans MS', 18, (66, 134, 244), 10, temp, 255)
        mob_fight.add(baz)
        temp_list.append(baz)
        temp += 20

    active_stats = active_mob.listStats()
    temp = 510
    for i in active_stats:
        if i == "health":
            baz = text(i.title() + ': ' + f"{active_stats[i]}/{active_mob.maxHealth}", 'Comic Sans MS', 18, (66, 134, 244), 400, temp, 255)
        else:
            baz = text(i.title() + ': ' + str(active_stats[i]), 'Comic Sans MS', 18, (66, 134, 244), 400, temp, 255)
        mob_fight.add(baz)
        temp_list.append(baz)
        temp += 20


def buildAttackMenu():
    global attack_active
    attack_menu_box = base_sprite(image="images\\attackMenu2.png",x=30,y=505)
    attack_menu.add(attack_menu_box)
    counterx = 45
    countery = 515
    for enum,ability in enumerate(current_turtle.abilities,1):
        abilitytext = text(ability + '(' + str((current_turtle.abilities[ability])[2]) + ')',"Comic Sans MS",18, (66,134,244),counterx,countery,255,(255,255,255))
        counterx += abilitytext.image.get_rect().size[0]+30
        if enum % 2 == 0:
            countery += 35
            counterx = 45
        attack_menu.add(abilitytext)
        attack_menu_list.append((abilitytext,ability))
    cancelbutton = text("Cancel","Comic Sans MS",13,(255,0,0),75,580,255)
    attack_menu.add(cancelbutton)
    attack_menu_list.append((cancelbutton,None))
    attack_active = True


party.add(turtle)
backgroundparty.append(turtle)
current_turtle = turtle
#party.add(ninjaTurtle)
#party.add(wizardTurtle)
#party.add(knightTurtle)
backgroundparty.append(ninjaTurtle)
backgroundparty.append(wizardTurtle)
backgroundparty.append(knightTurtle)


def buildTurnAlertMenu(event):
    counter = 520
    menu = base_sprite(image="images\\partyMenu.png",x=0,y=520)
    turnalert_list.add(menu)

    entertocontinue = text("Press enter or click to continue","Comic Sans MS",20, (255,0,0),330,610,255)
    turnalert_list.add(entertocontinue)

    wrapped = wrap(event,80)
    for textblock in wrapped:
        event_text = text(textblock,"Comic Sans MS",25,(66,134,244),5,counter,255)
        counter += 30
        turnalert_list.add(event_text)



def buildEquipmentMenu():
    counter = 17.5
    equipment_menu = base_sprite(image = "images\\partyMenu.png",x=0,y=500)
    equipment_list.add(equipment_menu)
    for turtle in [turtle for turtle in backgroundparty if turtle.isAlive]:
        button = text(turtle.name,"Comic Sans MS",40,(66,134,244),counter,540,255,(255,255,255))
        counter+=button.rect[2]+30
        equipment_list.add(button)
        button_list.append((button,turtle))



def spawnmob(mob=None):
    patker = entity.enemyCharacter('Patker', 20, 5, 5, 5, 0, 50, 1, 20, True, None, None, None, None, 'images\\patker.png')
    ultraPatker = entity.enemyCharacter('Ultra Patker', 200, 50, 50, 50, 25, 50, 15, 200, True, None, None, None, None, 'images\\ultraPatker.png')
    gersoxl = entity.enemyCharacter('Gersoxl', 1, 2, 3, 4, 5, 50,  6, 7, True, None, None, None, None, 'images\\gersoxl.png')
    mrComicSans = entity.enemyCharacter('Mr Comic Sans', 1, 2, 3, 4, 5, 50,  6, 7, True, None, None, None, None, 'images\\attackButton.png')
    mobs = [
        patker,
        ultraPatker,
        gersoxl,
        mrComicSans
    ]
    if mob != None:
        spawnedmob = ultraPatker
    else:
        spawnedmob = choice(mobs)
    #mob = mob_class(image=f"images\\{spawnedmob}.png",health=mobs.get(spawnedmob),name=spawnedmob)
    spawnedmob.rect.x = randint(50,900)
    spawnedmob.rect.y = randint(50,400)
    mobs_list.add(spawnedmob)

while running:
    if gameover:
        running = False

    party.empty()
    party.add(current_turtle)

    if backgroundparty == []:
        break



    while fight: #fight part
        #must be first in case all turtles are dead
        partydead = all(x.health == 0 for x in backgroundparty)
        if partydead:
            gameover = True
            running = False
            fight = False
            break


        backgroundparty[0].image = pygame.image.load(images[0])

        current_turtle = backgroundparty[0]


        if not turn and (not turnalert):
            print("starting mob turn")
            effectReturn = active_mob.handleEffects()
            print(effectReturn)
            if len(effectReturn) > 1:
                buildTurnAlertMenu(effectReturn[1])
                turnalert = True
                if effectReturn[0] == False:
                    passturn = False
                else:
                    passturn = True
                continue

            if active_mob.isAlive != False:
                attack = active_mob.Attack(current_turtle)

                tempalert = ''
                for index, i in enumerate(attack):
                    if index > 0:
                        tempalert += ' and '
                    tempalert += active_mob.name + ' ' + i[2] + ' '
                    if i[1] == 'player':
                        tempalert += current_turtle.name + ' '
                    else:
                        tempalert += 'self '
                    tempalert += 'for ' + str(i[0]) + ' with Basic Attack'
                    if i[3] != None:
                        tempalert += ' and '  + i[3]
                buildTurnAlertMenu(tempalert)


                turnalert = True
                passturn = True

                print("Mob attacked")
                if current_turtle.isAlive == False:
                    sprite,image = backgroundparty[0],images[0]
                    backgroundparty.pop(0)
                    images.pop(0)
                    backgroundparty.append(sprite)
                    images.append(image)
                    buildTurnAlertMenu(f"{active_mob.name} has done {attack[0][0]} damage. {current_turtle.name} has died.")
                    turnalert = True
                    passturn = True

                if len(party_list) > 0:
                    party_list.empty()
                    placementcounter = 25
                    party_menu_list = []
                    buildPartyMenu()

            else:
                fightover = True


        eventlist = pygame.event.get()
        console.process_input(eventlist)
        pygame.display.flip()
        for event in eventlist:
            if event.type == pygame.QUIT:
                running = False
                fight=False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    console.set_active()

                if event.key == pygame.K_RETURN:
                    if turnalert:
                        turnalert = False
                        turnalert_list.empty()
                        if passturn:
                            if turn:
                                turn = False #whenever dialog box is closed it will end turn
                            else: #if mob's turn and passturn is true changes it to your turn
                                effectReturn = current_turtle.handleEffects()
                                #if effectReturn[0]:
                                if len(effectReturn) > 1: #checks to see if any effects are active
                                    buildTurnAlertMenu(effectReturn[1])
                                    #turn = False buildturnalertmenu sets var turnalert to true, when turnalert is true it listens for enter or click to end turn
                                    turnalert = True
                                    if effectReturn[0] == False: #if the effect doesnt end turn
                                        passturn = False
                                    else:
                                        passturn = True
                                turn = True

                        else:
                            if not turn:
                                """
                                ENTIRE MOB'S TURN
                                """
                                if active_mob.isAlive != False:
                                    attack = active_mob.Attack(current_turtle)

                                    tempalert = ''
                                    for index, i in enumerate(attack):
                                        if index > 0:
                                            tempalert += ' and '
                                        tempalert += active_mob.name + ' ' + i[2] + ' '
                                        if i[1] == 'player':
                                            tempalert += current_turtle.name + ' '
                                        else:
                                            tempalert += 'self '
                                        tempalert += 'for ' + str(i[0]) + ' with Basic Attack'
                                        if i[3] != None:
                                            tempalert += ' and '  + i[3]
                                    buildTurnAlertMenu(tempalert)


                                    turnalert = True
                                    passturn = True

                                    print("Mob attacked")
                                    if current_turtle.isAlive == False:
                                        sprite,image = backgroundparty[0],images[0]
                                        backgroundparty.pop(0)
                                        images.pop(0)
                                        backgroundparty.append(sprite)
                                        test = Image.open(image).convert("LA").convert("RGBA")
                                        mode = test.mode
                                        size = test.size
                                        data = test.tobytes()
                                        testimage = pygame.image.fromstring(data,size,mode)
                                        images.append(testimage)
                                        buildTurnAlertMenu("Your active turtle has died")
                                        turnalert = True
                                        passturn = True

                                    if len(party_list) > 0:
                                        party_list.empty()
                                        placementcounter = 25
                                        party_menu_list = []
                                        buildPartyMenu()

                                else:
                                    fightover = True
                                """
                                END OF ENTIRE MOB'S CODE
                                """

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if partybutton.rect.collidepoint(event.pos):
                    if statsbool:
                        for sprite in temp_list:
                            mob_fight.remove(sprite)
                        mob_fight.remove(stat_menu)
                        statsbool = False
                        temp_list = []

                    if menubool:
                        party_list.empty()
                        menubool = False
                        placementcounter = 25
                        party_menu_list = []

                    else:
                        buildPartyMenu()
                        menubool = True




                if statsbutton.rect.collidepoint(event.pos):
                    if menubool:
                        party_list.empty()
                        menubool = False
                        placementcounter = 25
                        party_menu_list = []

                    if statsbool:
                        for sprite in temp_list:
                            mob_fight.remove(sprite)
                        mob_fight.remove(stat_menu)
                        statsbool = False
                        temp_list = []


                    else:
                        buildStatMenu()
                        statsbool = True

                if not statsbutton.rect.collidepoint(event.pos) and (not partybutton.rect.collidepoint(event.pos)) and (turnalert):
                    turnalertloopbool = True
                    turnalert = False
                    turnalert_list.empty()
                    if passturn:
                        if turn:
                            turn = False #whenever dialog box is closed it will end turn
                        else: #if mob's turn and passturn is true changes it to your turn
                            effectReturn = current_turtle.handleEffects()
                            #if effectReturn[0]:
                            if len(effectReturn) > 1: #checks to see if any effects are active
                                buildTurnAlertMenu(effectReturn[1])
                                #turn = False buildturnalertmenu sets var turnalert to true, when turnalert is true it listens for enter or click to end turn
                                turnalert = True
                                if effectReturn[0] == False: #if the effect doesnt end turn
                                    passturn = False
                                else:
                                    passturn = True
                            turn = True

                    else:
                        if not turn:
                            """
                            HANDLES ENTIRE MOB TURN
                            """
                            if active_mob.isAlive != False:
                                attack = active_mob.Attack(current_turtle)

                                tempalert = ''
                                for index, i in enumerate(attack):
                                    if index > 0:
                                        tempalert += ' and '
                                    tempalert += active_mob.name + ' ' + i[2] + ' '
                                    if i[1] == 'player':
                                        tempalert += current_turtle.name + ' '
                                    else:
                                        tempalert += 'self '
                                    tempalert += 'for ' + str(i[0]) + ' with Basic Attack'
                                    if i[3] != None:
                                        tempalert += ' and '  + i[3]
                                buildTurnAlertMenu(tempalert)


                                turnalert = True
                                passturn = True

                                print("Mob attacked")
                                if current_turtle.isAlive == False:
                                    sprite,image = backgroundparty[0],images[0]
                                    backgroundparty.pop(0)
                                    images.pop(0)
                                    backgroundparty.append(sprite)
                                    test = Image.open(image).convert("LA").convert("RGBA")
                                    mode = test.mode
                                    size = test.size
                                    data = test.tobytes()
                                    testimage = pygame.image.fromstring(data,size,mode)
                                    images.append(testimage)
                                    buildTurnAlertMenu("Your active turtle has died")
                                    turnalert = True
                                    passturn = True

                                if len(party_list) > 0:
                                    party_list.empty()
                                    placementcounter = 25
                                    party_menu_list = []
                                    buildPartyMenu()

                            else:
                                fightover = True


                            """
                            END OF ENTIRE MOB'S TURN
                            """





                if turn and (not turnalert):

                    if len(party_list) > 0:
                        for sprite in party_menu_list:
                            if sprite[0].rect.collidepoint(event.pos) and sprite[1].isAlive:
                                if selection1: #first selected
                                    if selection1 == sprite[1]:
                                        selection1 = False
                                        party_list.remove(pointer1)
                                    else:
                                        selection2 = sprite[1]
                                        sprite1,sprite2 = backgroundparty.index(selection1), backgroundparty.index(selection2)
                                        backgroundparty[sprite1], backgroundparty[sprite2] = backgroundparty[sprite2], backgroundparty[sprite1]
                                        images[sprite1],images[sprite2] = images[sprite2],images[sprite1]
                                        backgroundparty[0].rect.x = current_turtle.rect.x
                                        backgroundparty[0].rect.y = current_turtle.rect.y
                                        backgroundparty[0].image = pygame.image.load(images[0])
                                        if direction == "left":
                                            backgroundparty[0].image = pygame.transform.flip(backgroundparty[0].image,100,0)
                                        current_turtle = backgroundparty[0]
                                        selection1 = False
                                        selection2 = False
                                        party_list.empty()
                                        placementcounter = 25
                                        party_menu_list = []
                                        #buildPartyMenu()
                                        # turn = False
                                        buildTurnAlertMenu("Swapped party member")
                                        turnalert = True
                                        passturn = True
                                        party_list.remove(pointer1)

                                else: #none selected
                                    selection1 = sprite[1]
                                    pointer1 = base_sprite(image = "images\\arrow.png")
                                    pointer1.rect.x = sprite[0].rect.x - 30
                                    pointer1.rect.y = sprite[0].rect.y + 50
                                    party_list.add(pointer1)

                    elif runbutton.rect.collidepoint(event.pos) and attack_active == False and (not turnalertloopbool):
                        # TODO when speed added have it calculate if you run. if fail turn = False
                        fightover = True



                    elif len(attack_menu_list) > 0 and (not turnalertloopbool):
                        for sprite in attack_menu_list:
                            if sprite[0].rect.collidepoint(event.pos):
                                    if sprite[0].text == "Cancel":
                                        attack_active = False
                                        attack_menu.empty()
                                        attack_menu_list = []
                                    else:
                                        attack = (current_turtle.abilities[sprite[1]][0])(active_mob)
                                        if attack != False:
                                            if active_mob.isAlive == False:
                                                fightover = True
                                            # [[character.trueDamage(self.attack*2), 'enemy', 'damaged', None]]
                                            #turn = False

                                            tempalert = ''
                                            for index, i in enumerate(attack):
                                                if index > 0:
                                                    tempalert += ' and '
                                                tempalert += current_turtle.name + ' ' + i[2] + ' '
                                                if i[1] == 'enemy':
                                                    tempalert += active_mob.name+ ' '
                                                else:
                                                    tempalert += 'self '
                                                tempalert += 'for ' + str(i[0]) + ' with ' + sprite[1]
                                                if i[3] != None:
                                                    tempalert += ' and '  + i[3]
                                            buildTurnAlertMenu(tempalert)
                                            turnalert = True
                                            passturn = True
                                        attack_active = False
                                        attack_menu.empty()
                                        attack_menu_list = []

                    elif attackbutton.rect.collidepoint(event.pos) and attack_active == False and (not turnalertloopbool):
                        if attack_active:
                            attack_active = False
                            attack_menu.empty()
                            attack_menu_list = []


                        else: #build menu
                            buildAttackMenu()






        mob_fight.remove(turtle_image)

        turtle_image = base_sprite(image=current_turtle.image)
        #if direction == "left":
        #    turtle_image.image = pygame.transform.flip(turtle_image.image,100,0)
        turtle_image.image = pygame.transform.rotozoom(turtle_image.image,0,1.5)
        turtle_image.rect.x = 60
        turtle_image.rect.y = 370
        mob_fight.add(turtle_image)
        bar = [x for x in current_turtle.effects if (current_turtle.effects[x])[0]]
        if bar:
            foobar =' - ' +  ",".join(bar).title()
        else:
            foobar = ""
        hptext.print_text(f"Hp: {current_turtle.health}/{current_turtle.maxHealth}{foobar}",60,495)
        joined = ",".join([x for x in active_mob.effects if (active_mob.effects[x])[0]])
        active_mob_effects.print_text(f"{joined.title()}",0,active_mob_effects.rect.y)
        active_mob_effects.rect.x = 1000-active_mob_effects.rect[2] - 10
        mob_fight.remove(mob_info)
        mob_fight.remove(turntext)
        if turn:
            turntext = text("Your turn","Comic Sans MS",30,(66,134,244),200,5,255)
        else:
            turntext = text(f"{active_mob.name}'s turn","Comic Sans MS", 30, (66,134,244), 200, 5, 255)
        #turntext.print_text("niet",turntext.rect.x,turntext.rect.y) #change text
        mob_info = text(f"{active_mob.name}: {active_mob.health}hp","Comic Sans MS",18,(66, 134, 244),0,active_mob.image.get_rect().size[1]+20,255)
        mob_info.rect.x = 1000 - mob_info.rect[2] - 10
        mob_fight.add(mob_info)
        mob_fight.add(turntext)
        mob_fight.update()
        party_list.update()
        sprites_list.update()
        general_sprites.update()
        equipment_list.update()
        attack_menu.update()
        screen.fill(color) #gets rid of all sprites without removing them from groups
        general_sprites.draw(screen)
        attack_menu.draw(screen)
        turnalert_list.draw(screen)
        mob_fight.draw(screen)
        party_list.draw(screen)
        equipment_list.draw(screen)
        console.draw()
        pygame.display.flip()
        turnalertloopbool = False
        #fight = False
        if fightover:
            for turtle in backgroundparty: turtle.handleBuffs()
            mob_fight.empty()
            general_sprites.empty()
            fightover = False
            fight = False
            turn = True
            attack_active = False
            attack_menu.empty()
            attack_menu_list = []
            if direction == "left":
                backgroundparty[0].image = pygame.transform.flip(backgroundparty[0].image,100,0)

            turnalert = False
            turnalert_list.empty()
            for turtle in backgroundparty: #blanks effects after battle
                turtle.effects = {'burned': [False, [4, 8], 0], 'frozen': [False, [2, 4], 0], 'confused': [False, [6, 10], 0]}

            passturn = False


    if randint(0,500) == 0: #mob spawner
        spawnmob()

    eventlist = pygame.event.get()
    console.process_input(eventlist)
    pygame.display.flip()
    for event in eventlist:
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                console.set_active()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if partybutton.rect.collidepoint(event.pos):
                if menubool:
                    party_list.empty()
                    menubool = False
                    placementcounter = 25
                    party_menu_list = []
                else:
                    buildPartyMenu()
                    menubool = True

            elif equipmentbutton.rect.collidepoint(event.pos): #TODO make it toggle with menubool
                if equipmentbool: #TODO
                    equipment_list.empty()
                    equipmentbool = False
                    button_list = []
                    equipment_turtle = None
                    #empty
                else:
                    buildEquipmentMenu()
                    equipmentbool = True


            elif len(equipment_list) > 0:
                if len(button_list) == 4: #if in main menu (lists all 4 turtles)
                    for button in button_list:
                        if button[0].rect.collidepoint(event.pos):
                            exitbutton = text("Exit","Comic Sans MS",18,(66,134,244),960,620,255)
                            equipment_list.add(exitbutton)
                            equipment_turtle = button[1]
                            list_temp = equipment_list
                            for sprite in list_temp:
                                if any(sprite in x for x in button_list):
                                    equipment_list.remove(sprite)
                            button_list = []
                            levelButton = text("Level tree","Comic Sans MS",46,(66,134,244),225,540,255,(255,255,255))
                            equipmentButton = text("Equipment","Comic Sans MS",46,(66,134,244),500,540,255,(255,255,255))
                            equipment_list.add(levelButton)
                            equipment_list.add(equipmentButton)
                            button_list.append(levelButton)
                            button_list.append(equipmentButton)

                            #build equipment turtle menu
                elif len(button_list) == 2: #turtle has been selected - 2 buttons (equipment/level tree)
                    for button in button_list:
                        if button.rect.collidepoint(event.pos):
                            tempcount = 15
                            for i in button_list:
                                equipment_list.remove(i)
                            if button.text == "Level tree":
                                stats = equipment_turtle.listStats()
                                for level in stats:
                                        leveltext = text(f"{level}: {stats[level]}","Comic Sans MS",24,(66,134,244),tempcount,575,255)
                                        equipment_list.add(leveltext)
                                        tempcount+=leveltext.rect[2]+30
                                turtle_text = text(f"{equipment_turtle.name}'s stats","Comic Sans MS",36,(66,134,244),300,510,255)
                                equipment_list.add(turtle_text)
                                button_list = []

                            elif button.text == "Equipment":
                                equipment = equipment_turtle.listSelf()
                                for i in equipment:
                                    print(i)
                                    print(equipment[i])



                if equipment_turtle != None:
                    #handle clicks on individual turtle's armor and items menu

                    if exitbutton.rect.collidepoint(event.pos):
                        equipment_list.empty()
                        equipment_turtle = None
                        button_list = []
                        buildEquipmentMenu()


            if len(party_list) > 0:
                for sprite in party_menu_list:
                    if sprite[0].rect.collidepoint(event.pos) and sprite[1].isAlive:
                        if selection1: #first selected
                            if selection1 == sprite[1]:
                                selection1 = False
                                party_list.remove(pointer1)
                            else:
                                selection2 = sprite[1]
                                sprite1,sprite2 = backgroundparty.index(selection1), backgroundparty.index(selection2)
                                backgroundparty[sprite1], backgroundparty[sprite2] = backgroundparty[sprite2], backgroundparty[sprite1]
                                images[sprite1],images[sprite2] = images[sprite2],images[sprite1]
                                backgroundparty[0].rect.x = current_turtle.rect.x
                                backgroundparty[0].rect.y = current_turtle.rect.y
                                backgroundparty[0].image = pygame.image.load(images[0])
                                if direction == "left":
                                    backgroundparty[0].image = pygame.transform.flip(backgroundparty[0].image,100,0)
                                current_turtle = backgroundparty[0]
                                selection1 = False
                                selection2 = False
                                party_list.empty()
                                placementcounter = 25
                                party_menu_list = []
                                buildPartyMenu()
                                party_list.remove(pointer1)

                        else: #none selected
                            selection1 = sprite[1]
                            pointer1 = base_sprite(image = "images\\arrow.png")
                            pointer1.rect.x = sprite[0].rect.x - 30
                            pointer1.rect.y = sprite[0].rect.y + 50
                            party_list.add(pointer1)



    keys = pygame.key.get_pressed()
    if console.active == False:
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            positions.append((current_turtle.rect.x,current_turtle.rect.y))
            current_turtle.move('y', -8)
            current_turtle.rect.clamp_ip(screen_rect)
            move = True

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            positions.append((current_turtle.rect.x,current_turtle.rect.y))
            current_turtle.move('y', 8)
            current_turtle.rect.clamp_ip(screen_rect)
            move = True

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            positions.append((current_turtle.rect.x,current_turtle.rect.y))
            current_turtle.move('x', -8)
            current_turtle.rect.clamp_ip(screen_rect)
            move = True
            direction = "left"
            if scrollX < 0:
                scrollX += 8

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            positions.append((current_turtle.rect.x,current_turtle.rect.y))
            current_turtle.move('x', 8)
            current_turtle.rect.clamp_ip(screen_rect)
            move = True
            direction = "right"
            scrollX -= 8



    if direction != olddirection:
        current_turtle.image = pygame.transform.flip(current_turtle.image,100,0)

    '''
    if move:
        for enum,i in enumerate(party,0):
            if enum != 0:
                foo = positions[-1]
                positions.append((i.rect.x,i.rect.y))
                i.rect.x = foo[0]
                i.rect.y = foo[1]
            if direction != olddirection:
                i.image = pygame.transform.flip(i.image,100,0)
        move = False
    '''

    collision = pygame.sprite.groupcollide(mobs_list,party,True,False)
    if collision: #handle one time things here before fight starts
        active_mob = list(collision)[0]
        active_mob.image = pygame.transform.rotozoom(active_mob.image,0,2.75)
        active_mob.rect.x = 1000 - active_mob.image.get_rect().size[0]
        active_mob.rect.y = 0
        if active_mob.name == "Patker":
            if randint(0,1) == 0:
                console.output('it has stilts')
                active_mob.equip(stilts)
        elif active_mob.name == 'Ultra Patker':
            active_mob.equip(helmOfPatker)
            active_mob.equip(gownsOfPatker)
            active_mob.equip(sandlesOfPatker)
            active_mob.equip(greatSwordOfPatker)
        turntext = text("Your turn","Comic Sans MS",30,(66,134,244),200,5,255)
        mob_info = text(f"{active_mob.name}: {active_mob.health}hp","Comic Sans MS",18,(66, 134, 244),0,active_mob.image.get_rect().size[1]+20,255)

        mob_info.rect.x = 1000 - mob_info.rect[2] - 10
        mob_fight.add(active_mob)
        mob_fight.add(turntext)
        mob_fight.add(mob_info)

        attackbutton = base_sprite(image = "images\\attackButton.png",x=30,y=525)
        runbutton = base_sprite(image = "images\\runButton.png",x=135,y=525)
        general_sprites.add(attackbutton)
        general_sprites.add(runbutton)


        fight = True
        if menubool:
            party_list.empty()
            menubool = False
            placementcounter = 25
            party_menu_list = []
        general_sprites.add(partybutton)

        statsbutton = base_sprite(image = "images\\statsButton.png")
        statsbutton.rect.x = 0
        statsbutton.rect.y = 50
        general_sprites.add(statsbutton)
        turtle_image = base_sprite(image=current_turtle.image)
        if direction == "left":
            turtle_image.image = pygame.transform.flip(turtle_image.image,100,0)
        turtle_image.image = pygame.transform.rotozoom(turtle_image.image,0,1.5)
        turtle_image.rect.x = 60
        turtle_image.rect.y = 435
        mob_fight.add(turtle_image)
        bar = [x for x in current_turtle.effects if (current_turtle.effects[x])[0]]
        if bar:
            foobar =' - ' +  ",".join(bar).title()
        else:
            foobar = ""
        hptext = text(f"Hp: {current_turtle.health}/{current_turtle.maxHealth}{foobar}","Comic Sans MS",18,(66,134,244),60,495,255)
        mob_fight.add(hptext)
        joined = ",".join([x for x in active_mob.effects if (active_mob.effects[x])[0]])
        active_mob_effects = text(f"{joined.title()}","Comic Sans MS",18,(66,134,244),0,active_mob.image.get_rect().size[1]+45,255)
        active_mob_effects.rect.x = 1000-active_mob_effects.rect[2] - 10
        mob_fight.add(active_mob_effects)


    screen.blit(game_map,(scrollX*2,0))
    olddirection = direction
    sprites_list.update()
    party.update()
    mobs_list.update()
    party_list.update()
    equipment_list.update()
    #screen.fill(color)
    sprites_list.draw(screen)
    party.draw(screen)
    mobs_list.draw(screen)
    party_list.draw(screen)
    equipment_list.draw(screen)
    console.draw()
    pygame.display.flip()
    clock.tick(60)

if gameover:
    screen.fill((255,255,255))
    screen.blit(pygame.font.SysFont("Comic Sans MS",80,italic=True).render("Game over",1,(0,0,0)),(300,40))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


        pygame.display.flip()


else: #safely shuts down pygame and other data
    pygame.quit()

# TODO make it so that turtles can die
# TODO add health to current_turtle displayed
# TODO enemies able to die from burn
# TODO SKILL TREE ON LEVLE UP BABYYY

#TODO make it list active mob's status effects
#TODO change names from turtle 1 to actual names
