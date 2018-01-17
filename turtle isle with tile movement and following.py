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


#################
# sprite groups #
#################

sprites_list = pygame.sprite.Group()
party = pygame.sprite.Group()
mobs_list = pygame.sprite.Group()
mob_fight = pygame.sprite.Group()



###########
# classes #
###########
class base_sprite(pygame.sprite.Sprite): #turtle spawned in middle of screen
        def __init__(self, color=(0,0,0), width=0, height=0, image=None,health=100):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(image)
            pygame.draw.rect(self.image, color, [5000000,5000000,width,height])
            self.rect = self.image.get_rect()
            self.health = health
        def move(self, diri, amount):
            exec('self.rect.' + diri + ' += ' + str(amount))


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
'''
class entity():
    class playerCharacter(pygame.sprite.Sprite):
        def __init__(self, initHealth, initAttack, initDeffence, initStrength, initMagic, initRanged, initLevel, initExp):
            self.health = initHealth
            self.attack = initAttack
            self.deffence = initDeffence
            self.strength = initStrength
            self.magic = initMagic
            self.ranged = initRanged
            self.level = initLevel
            self.exp = initExp
            self.isAlive = True
        def levleUp(amount):
            self.level += amount
        def checkExp():
            if self.exp >= self.level*5:
                self.levelUp(1)
                self.exp = self.exp - self.level*5
                self.checkExp()
        def expUp(amount):
            self.exp += amount
            self.checkExp()


    class enemyCharacter():
        None
    class item():
        class keyItem():
            None
'''




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


running = True
positions = []
move = False
direction = "right"
olddirection = "right"
fight = False
active_mob = None

turtle = base_sprite(image="images\\smallTurtle.png",health=100)
ninjaTurtle = base_sprite(image="images\\NinjaTurtle.png",health=100)
wizardTurtle = base_sprite(image="images\\wizardTurtle.png",health=100)
knightTurtle = base_sprite(image='images\\KnightTurtle.png',health=100)
turtle.rect.x = 250
turtle.rect.y = 250
ninjaTurtle.rect.x = 250
ninjaTurtle.rect.y = 300
wizardTurtle.rect.x = 250
wizardTurtle.rect.y = 350
knightTurtle.rect.x = 250
knightTurtle.rect.y = 400


party.add(turtle)
party.add(ninjaTurtle)
party.add(wizardTurtle)
party.add(knightTurtle)

pygame.key.set_repeat(50,50)
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
            if event.key == pygame.K_w:
                positions.append((turtle.rect.x,turtle.rect.y))
                turtle.move('y', -100)
                move = True

            elif event.key == pygame.K_s:
                positions.append((turtle.rect.x,turtle.rect.y))
                turtle.move('y', 80)
                move = True

            elif event.key == pygame.K_a:
                positions.append((turtle.rect.x,turtle.rect.y))
                turtle.move('x', -100)
                move = True
                direction = "left"

            elif event.key == pygame.K_d:
                positions.append((turtle.rect.x,turtle.rect.y))
                turtle.move('x', 80)
                move = True
                direction = "right"
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


    olddirection = direction
    sprites_list.update()
    party.update()
    mobs_list.update()
    screen.fill(color)
    sprites_list.draw(screen)
    party.draw(screen)
    mobs_list.draw(screen)
    pygame.display.flip()
    clock.tick(60)
