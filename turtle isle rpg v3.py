import pygame
from threading import Thread
from time import sleep,time
from random import randint,uniform,choice
import PyCon
from Functions import *
from string import *

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
        def __init__(self, initHealth, initAttack, initdefence, initStrength, initMagic, initmagic, initLevel, initExp, maxHealth, head, torso, feet, hand, image):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(image)
            pygame.draw.rect(self.image, (0,0,0), [5000000,5000000,0,0])
            self.rect = self.image.get_rect()
            self.health = initHealth
            self.attack = initAttack
            self.defence = initdefence
            self.strength = initStrength
            self.magic = initMagic
            self.magic = initmagic
            self.level = initLevel
            self.exp = initExp
            self.isAlive = True
            self.maxHealth = maxHealth
            self.head = head
            self.torso = torso
            self.feet = feet
            self.hand = hand
        def move(self, diri, amount):
            exec('self.rect.' + diri + ' += ' + str(amount))

        def levelUp(self, amount):
            self.level += amount
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
            self.health -= int(amount)
            if self.health <= 0:
                self.health = 0
                self.isAlive = False
            return self.isAlive
        def damage(self, amount):
            self.trueDamage(amount / ((randint(3, 4) * self.defence)/100))
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
                for index, i in enumerate(item.effects, 0):
                    exec('self.' + i + ' += ' + str(item.effects[i]))
                return True
            return False
        def calcAttackDamage(self):
            return randint(3,4) * (self.attack * (1.5 * self.strength))
        def attack(self, character):
            if type(character).name__ == 'enemyCharacter' or type(character).__name__ == 'playerCharacter':
                if self.hand == None:
                    character.damage(self.calcAttackDamage())
                return True
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
            return {'health': self.health, 'attack': self.attack, 'strength': self.strength, 'defence': self.defence, 'magic': self.magic}
        def listLevel(self):
            return {'level': self.level, 'exp': self.exp}


    class enemyCharacter(pygame.sprite.Sprite):
        def __init__(self, name, health, attack, defence, strength, magic, level, maxHealth, isAlive, head, torso, feet, hand, image):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(image)
            pygame.draw.rect(self.image, (0,0,0), [5000000,5000000,0,0])
            self.rect = self.image.get_rect()
            self.health = health
            self.attack = attack
            self.defence = defence
            self.strength = strength
            self.magic = magic
            self.level = level
            self.maxHealth = maxHealth
            self.head = head
            self.torso = torso
            self.feet = feet
            self.hand = hand
            self.name = name
        def calcAttackDamage(self):
            return randint(3,4) * (self.attack * (1.5 * self.strength))
        def attack(self, entity):
            if randint(0, attack) != 0:
                entity.damage(self.calcAttackDamage())
        def trueDamage(self, amount):
            self.health -= amount
            if self.health < 0:
                self.health = 0
                self.isAlive = False
        def damage(self, amount):
            self.trueDamage(amount / ((randint(3, 4) * self.defence)/100))
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
            return {'health': self.health, 'attack': self.attack, 'strength': self.strength, 'defence': self.defence, 'magic': self.magic}

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
    def __init__(self, initHealth, initAttack, initdefence, initStrength, initMagic, initLevel, initExp, maxHealth, head, torso, feet, hand, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        pygame.draw.rect(self.image, (0,0,0), [5000000,5000000,0,0])
        self.rect = self.image.get_rect()
        self.health = initHealth
        self.attack = initAttack
        self.defence = initdefence
        self.strength = initStrength
        self.magic = initMagic
        self.level = initLevel
        self.exp = initExp
        self.isAlive = True
        self.maxHealth = maxHealth
        self.head = head
        self.torso = torso
        self.feet = feet
        self.hand = hand



class text(pygame.sprite.Sprite): #helpful class for rendering text as a sprite
        def __init__(self, text, font_path, font_size, font_colour, x, y, opacity):
                pygame.sprite.Sprite.__init__(self)
                self.font = pygame.font.SysFont(font_path, font_size)
                self.color = font_colour
                self.render_text = text
                self.rerender(x,y,opacity)
                self.pos = y
                self.text = text
                self.opacity = opacity
        def update(self):
                pass
        def print_text(self, text_string, x, y):
                self.render_text = text_string
                self.rerender(x,y,self.opacity)
        def rerender(self, x, y, opacity):
                self.image = self.font.render(self.render_text, 0, self.color)
                self.image.set_alpha(opacity)
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y

########################
# predefined variables #
########################
running = True
positions = []
move = False
direction = "right"
olddirection = "right"
fight = False
active_mob = None
menubool = False
scrollX = 0
backgroundparty = []
placementcounter = 25
selection1 = False
selection2 = False
party_menu_list = []
turn = True
statsbool = False
temp_list = []


images = ['images\\smallTurtle.png','images\\NinjaTurtle.png','images\\WizardTurtle.png','images\\KnightTurtle.png']
turtle = entity.playerCharacter(50, 50, 50, 50, 50, 50, 1, 0, 50, None, None, None, None, image='images\\smallTurtle.png')
ninjaTurtle = entity.playerCharacter(50, 50, 50, 50, 50, 50, 1, 0, 50, None, None, None, None, image='images\\NinjaTurtle.png')
wizardTurtle = entity.playerCharacter(50, 50, 50, 50, 50, 50, 1, 0, 50, None, None, None, None, image='images\\WizardTurtle.png')
knightTurtle = entity.playerCharacter(50, 50, 50, 50, 50, 50, 1, 0, 50, None, None, None, None, image='images\\KnightTurtle.png')
turtle.rect.x = 250
turtle.rect.y = 250
ninjaTurtle.rect.x = 250
ninjaTurtle.rect.y = 300
wizardTurtle.rect.x = 250
wizardTurtle.rect.y = 350
knightTurtle.rect.x = 250
knightTurtle.rect.y = 400

###############
# CONSUMABLES #
###############

healthPotion = entity.item.consumable('Health Potion', 'A small potion that restores 10 health', ({'health': 10}), 'images\\sprites\\healthPotion.png')
mediumHealthPotion = entity.item.consumable('Medium Health Potion', 'A potion that is slightly larger than a normal Health Potion that restores 75 health', ({'health': 75}),"images\\sprites\\mediumHealthPotion.png")
bigHealthPotion = entity.item.consumable('Big Health Potion', 'A potion that is significantly larger than a normal Health Potion that restores 200 health', ({'health': 200}), 'images\\sprites\\bigHealthPotion.png')
giantHealthPotion = entity.item.consumable('Giant Health Potion', 'A potion that dwarfes a normal Health Potion in comparison that restores an amount of health that is over 9000', ({'health': 9001}), 'images\\sprites\\giantHealthPotion.png')

attackUp = entity.item.consumable('Attack Up', 'A small tablet the permanatley increases your attack by 10', ({'attack': 10}), 'images\\sprites\\attackUp.png')
strengthUp = entity.item.consumable('Strength Up', 'A small tablet the permanatley increases your strength by 10', ({'strength': 10}),"images\\sprites\\strengthUp.png")
defenceUp = entity.item.consumable('Defence Up', 'A small tablet the permanatley increases your defence by 10', ({'defence': 10}), 'images\\sprites\\defenceUp.png')
magicUp = entity.item.consumable('Magic Up', 'A small tablet the permanatley increases your magic by 10', ({'magic': 10}), 'images\\sprites\\magicUp.png')
maxHealthUp = entity.item.consumable('Max Health Up', 'A small tablet the permanatley increases your max health by 10', ({'maxHealth': 10}),"images\\sprites\\maxHealthUp.png")

expOrb = entity.item.consumable('EXP Orb', 'Test your luck', ({'exp': randint(1, 100)}), 'images\\sprites\\expOrb.png')


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

console = PyCon.PyCon(screen,
                      (0,0,1000,650 / 4),
                      functions = {
                                    "eval":evaluate,
                                    "exec":execute
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
    for enum,i in enumerate(backgroundparty, 1):
        if enum == 0:
            enumfixed = 0
        else:
            enumfixed = enum-1
        image = base_sprite(image = images[enumfixed])
        image.rect.x = placementcounter
        image.rect.y = 510
        texthealth = text(f"Turtle {enum} - Hp: {i.health}","Comic Sans MS",16,(66, 134, 244),placementcounter-15,593.5,255)
        placementcounter+=150
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
    temp = 520
    for i in active_stats:
        baz = text(i.title() + ': ' + str(active_stats[i]), 'Comic Sans MS', 18, (66, 134, 244), 400, temp, 255)
        mob_fight.add(baz)
        temp_list.append(baz)
        temp += 20


    # mob_self = text(f"{active_mob.head.name} on head, {active_mob.torso.name} on torso, {active_mob.feet.name} on feet, {active_mob}","Comic Sans MS",18,(66, 134, 244),0,active_mob.image.get_rect().size[1]+20,255)
    # mob_stats = text(f"{active_mob.name}: {active_mob.health}hp","Comic Sans MS",18,(66, 134, 244),0,active_mob.image.get_rect().size[1]+20,255)



party.add(turtle)
backgroundparty.append(turtle)
current_turtle = turtle
#party.add(ninjaTurtle)
#party.add(wizardTurtle)
#party.add(knightTurtle)
backgroundparty.append(ninjaTurtle)
backgroundparty.append(wizardTurtle)
backgroundparty.append(knightTurtle)

#pygame.key.set_repeat(10,10)

def spawnmob():
    patker = entity.enemyCharacter('Patker', 20, 5, 5, 5, 0, 1, 20, True, None, None, None, None, 'images\\patker.png')
    ultraPatker = entity.enemyCharacter('Ultra Patker', 200, 50, 50, 50, 25, 15, 200, True, None, None, None, None, 'images\\ultraPatker.png')
    mobs = [
        patker,
        ultraPatker
    ]

    spawnedmob = choice(mobs)
    #mob = mob_class(image=f"images\\{spawnedmob}.png",health=mobs.get(spawnedmob),name=spawnedmob)
    spawnedmob.rect.x = randint(50,900)
    spawnedmob.rect.y = randint(50,400)
    mobs_list.add(spawnedmob)

while running:
    party.empty()
    party.add(current_turtle)
    while fight: #fight part
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

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if partybutton.rect.collidepoint(event.pos):
                    if menubool:
                        party_list.empty()
                        menubool = False
                        placementcounter = 25
                        party_menu_list = []
                    else:
                        if statsbool:
                            for sprite in temp_list:
                                mob_fight.remove(sprite)
                            mob_fight.remove(stat_menu)
                            statsbool = False
                            temp_list = []
                        else:
                            buildPartyMenu()
                            menubool = True



                if statsbutton.rect.collidepoint(event.pos):
                    if statsbool:
                        for sprite in temp_list:
                            mob_fight.remove(sprite)
                        mob_fight.remove(stat_menu)
                        statsbool = False
                        temp_list = []

                    else:
                        if menubool:
                            party_list.empty()
                            menubool = False
                            placementcounter = 25
                            party_menu_list = []
                        else:
                            buildStatMenu()
                            statsbool = True

                if turn:
                    if len(party_list) > 0:
                        for sprite in party_menu_list:
                            if sprite[0].rect.collidepoint(event.pos):
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
                                        turn = False #enemy turn
                                        party_list.remove(pointer1)

                                else: #none selected
                                    selection1 = sprite[1]
                                    pointer1 = base_sprite(image = "images\\arrow.png")
                                    pointer1.rect.x = sprite[0].rect.x - 30
                                    pointer1.rect.y = sprite[0].rect.y + 50
                                    party_list.add(pointer1)

        mob_fight.remove(turtle_image)

        turtle_image = base_sprite(image=current_turtle.image)
        if direction == "left":
            turtle_image.image = pygame.transform.flip(turtle_image.image,100,0)
        turtle_image.image = pygame.transform.rotozoom(turtle_image.image,0,1.5)
        turtle_image.rect.x = 60
        turtle_image.rect.y = 370
        mob_fight.add(turtle_image)

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
        screen.fill(color) #gets rid of all sprites without removing them from groups
        mob_fight.draw(screen)
        party_list.draw(screen)
        general_sprites.draw(screen)
        console.draw()
        pygame.display.flip()
        #fight = False
        if False:
            fight = False
            turn = True


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

            if len(party_list) > 0:
                for sprite in party_menu_list:
                    if sprite[0].rect.collidepoint(event.pos):
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

    attackbutton = base_sprite(image = "images\\attackButton.png",x=150,y=480)
    runbutton = base_sprite(image = "images\\runButton.png",x=60,y=480)
    general_sprites.add(attackbutton)
    general_sprites.add(runbutton)

    screen.blit(game_map,(scrollX*2,0))
    olddirection = direction
    sprites_list.update()
    party.update()
    mobs_list.update()
    party_list.update()
    #screen.fill(color)
    sprites_list.draw(screen)
    party.draw(screen)
    mobs_list.draw(screen)
    party_list.draw(screen)
    console.draw()
    pygame.display.flip()
    clock.tick(60)
