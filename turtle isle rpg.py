import pygame
from threading import Thread
from time import sleep,time
from random import randint,uniform

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




###########
# classes #
###########
class base_sprite(pygame.sprite.Sprite): #turtle spawned in middle of screen
        def __init__(self, color=(0,0,0), width=0, height=0, image=None):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(image)
            pygame.draw.rect(self.image, color, [5000000,5000000,width,height])
            self.rect = self.image.get_rect()
        def move(self, diri, amount):
            exec('self.rect.' + diri + ' += ' + str(amount))



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

turtle = base_sprite(image="images\\smallTurtle.png")
ninjaTurtle = base_sprite(image="images\\NinjaTurtle.png")
wizardTurtle = base_sprite(image="images\\wizardTurtle.png")
knightTurtle = base_sprite(image='images\\KnightTurtle.png')
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
for i in party:
    positions.append(i.rect)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        turtle.move('y', -10)

    elif keys[pygame.K_s]:
        turtle.move('y', 10)

    elif keys[pygame.K_a]:
        turtle.move('x', -10)

    elif keys[pygame.K_d]:
        turtle.move('x', 10)




    sprites_list.update()
    party.update()
    screen.fill(color)
    sprites_list.draw(screen)
    party.draw(screen)
    pygame.display.flip()
    clock.tick(60)
