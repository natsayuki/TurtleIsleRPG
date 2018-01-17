import pygame
from threading import Thread
from time import sleep,time
from random import randint,uniform,choice

########
# init #
########
pygame.init()
color = (255,255,255)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1000,650))
screen_rect = pygame.Rect((0, 0), (1000, 650))
game_map = pygame.image.load("images\\testmap.png")

#################
# sprite groups #
#################

sprites_list = pygame.sprite.Group()
party = pygame.sprite.Group()
mobs_list = pygame.sprite.Group()
mob_fight = pygame.sprite.Group()
party_list = pygame.sprite.Group()


###########
# classes #
###########
class base_sprite(pygame.sprite.Sprite): #turtle spawned in middle of screen
        def __init__(self, color=(0,0,0), width=0, height=0, image=None,health=100):
            pygame.sprite.Sprite.__init__(self)
            if "Surface" in type(image).__name__:
                self.image = image
            else:
                self.image = pygame.image.load(image)
            pygame.draw.rect(self.image, color, [5000000,5000000,width,height])
            self.rect = self.image.get_rect()
            self.health = health



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
        def __init__(self, initHealth, initAttack, initDeffence, initStrength, initMagic, initRanged, initLevel, initExp, maxHealth, head, torso, feet, hand, image):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(image)
            pygame.draw.rect(self.image, (0,0,0), [5000000,5000000,0,0])
            self.rect = self.image.get_rect()
            self.health = initHealth
            self.attack = initAttack
            self.deffence = initDeffence
            self.strength = initStrength
            self.magic = initMagic
            self.ranged = initRanged
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
        def damage(self, amount, type):
            self.health -= int(amount)
            if self.health <= 0:
                self.health = 0
                self.isAlive = False
            return self.isAlive
        def heal(self, amount):
            self.health += amount
            if self.health > self.maxHealth:
                self.health = self.maxHealth
            return self.health
        def equip(self, item):
            if type(item) == entity.item.equipable:
                for i in item.effects:
                    exec('self.' + i + ' += ' + item.effects[i])
                exec('self.' + item.type + ' = item')
                return True
            return False
        def unequip(self, type):
            if eval('self.' + type) != None:
                item = eval('self.' + type)
                for i in item.effects:
                    exec('self.' + i + ' -= ' + item.effects[i])
                exec('self.' + type + ' = None')
                return item
            return False
        def consume(self, item):
            if type(item) == entity.item.consumable:
                for index, i in enumerate(item.effects, 0):
                    exec('self.' + i + ' += ' + item.effects[i])
                return True
            return False


    class enemyCharacter(pygame.sprite.Sprite):
        def __init__(self, name, health, attack, deffence, strength, magic, ranged, level, maxHealth, isAlive, head, torso, feet, hand):
            self.health = health
            self.attack = attack
            self.defence = deffence
            self.strength = strength
            self.magic = magic
            self.ranged = ranged
            self.level = level
            self.maxHealth = maxHealth
            self.head = head
            self.torso = torso
            self.feet = feet
            self.hand = hand
            self.name = name
        def calcAttackDamage(self):
            return self.stregth*(.5*self.attack)
        def attack(self, entity):
            if randint(0, attack) != 0:
                entity.damage(self.calcAttackDamage())
        def damage(self, amount):
            self.health -= amount
            if self.health < 0:
                self.health = 0
                self.isAlive = False
        def heal(self, amount):
            self.health += amount
            if self.health > self.maxHealth:
                self.health = self.maxHealth

    class item():
        # effects will take a dictionary eg:
        # {'heath': '10', 'attack': '5'}
        class equipable():
            def __init__(self, name, type, effects):
                self.name = name
                self.type = type
                self.effects = effects
        class consumable(pygame.sprite.Sprite):
            def __init__(self, effects):
                self.effects = effects
        class keyItem(pygame.sprite.Sprite):
            None
class smallTurtle(entity.playerCharacter):
    def __init__(self, initHealth, initAttack, initDeffence, initStrength, initMagic, initRanged, initLevel, initExp, maxHealth, head, torso, feet, hand, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        pygame.draw.rect(self.image, (0,0,0), [5000000,5000000,0,0])
        self.rect = self.image.get_rect()
        self.health = initHealth
        self.attack = initAttack
        self.deffence = initDeffence
        self.strength = initStrength
        self.magic = initMagic
        self.ranged = initRanged
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
        def update(self):
                pass
        def print_text(self, text_string, x, y):
                self.render_text = text_string
                self.rerender(x,y)
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

partybutton = base_sprite(image="images\\partyButton.png")
partybutton.rect.x = 0
partybutton.rect.y = 0
sprites_list.add(partybutton)

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
        if direction == "left" and enum == 1:
            image = pygame.transform.flip(i.image,100,0)
        else:
            image = i.image
        image = base_sprite(image = image)
        image.rect.x = placementcounter
        image.rect.y = 510
        texthealth = text(f"Turtle {enum} - Hp: {i.health}","Comic Sans MS",16,(66, 134, 244),placementcounter-15,593.5,255)
        placementcounter+=150
        party_list.add(image)
        party_list.add(texthealth)
        party_menu_list.append(image)


party.add(turtle)
backgroundparty.append(turtle)
current_turtle = turtle
#party.add(ninjaTurtle)
#party.add(wizardTurtle)
#party.add(knightTurtle)
backgroundparty.append(ninjaTurtle)
backgroundparty.append(wizardTurtle)
backgroundparty.append(knightTurtle)

pygame.key.set_repeat(10,10)
def spawnmob():
    mobs = {
        "patker":20
    } #get health of mob

    spawnedmob = choice(list(mobs))
    mob = mob_class(image=f"images\\{spawnedmob}.png",health=mobs.get(spawnedmob),name=spawnedmob)
    mob.rect.x = randint(50,900)
    mob.rect.y = randint(50,400)
    mobs_list.add(mob)

while running:
    while fight: #fight part
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                fight=False

        mob_fight.remove(mob_info)
        mob_info = text(f"{active_mob.name}: {active_mob.health}hp","Comic Sans MS",18,(66, 134, 244),active_mob.rect.x+50,active_mob.image.get_rect().size[1]+20,255)
        mob_fight.add(mob_info)
        mob_fight.update()
        screen.fill(color) #gets rid of all sprites without removing them from groups
        mob_fight.draw(screen)
        pygame.display.flip()
        #fight = False


    if randint(0,500) == 0: #mob spawner
        spawnmob()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                positions.append((turtle.rect.x,turtle.rect.y))
                turtle.move('y', -6.4)
                turtle.rect.clamp_ip(screen_rect)
                move = True

            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                positions.append((turtle.rect.x,turtle.rect.y))
                turtle.move('y', 6.4)
                turtle.rect.clamp_ip(screen_rect)
                move = True

            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                positions.append((turtle.rect.x,turtle.rect.y))
                turtle.move('x', -8)
                turtle.rect.clamp_ip(screen_rect)
                move = True
                direction = "left"
                if scrollX < 0:
                    scrollX += 8

            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                positions.append((turtle.rect.x,turtle.rect.y))
                turtle.move('x', 8)
                turtle.rect.clamp_ip(screen_rect)
                move = True
                direction = "right"
                scrollX -= 8

        if event.type == pygame.MOUSEBUTTONDOWN:
            if partybutton.rect.collidepoint(event.pos):
                if menubool:
                    party_list.empty()
                    menubool = False
                    placementcounter = 25
                else:
                    buildPartyMenu()
                    menubool = True

            if len(party_list) > 0:
                for sprite in party_menu_list:
                    if sprite.rect.collidepoint(event.pos):
                        if selection1: #first selected
                            if selection1 == sprite:
                                selection1 = False
                            else:
                                selection2 = sprite
                                sprite1,sprite2 = backgroundparty.index(selection1), backgroundparty.index(selection2)
                                backgroundparty[sprite1], backgroundparty[sprite2] = backgroundparty[sprite2], backgroundparty[sprite1]

                                selection1 = False
                                selection2 = False

                        else: #none selected
                            selection1 = sprite





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
        mob_info = text(f"{active_mob.name}: {active_mob.health}hp","Comic Sans MS",18,(66, 134, 244),active_mob.rect.x+50,active_mob.image.get_rect().size[1]+20,255)
        mob_fight.add(active_mob)
        mob_fight.add(mob_info)
        fight = True

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
    pygame.display.flip()
    clock.tick(60)
