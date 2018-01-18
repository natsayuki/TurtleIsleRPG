import pygame

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1000, 650))


sprites_list = pygame.sprite.Group()

running = True

class pygame_utils():
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


    class button(pygame.sprite.Sprite):
        # for image
        def __init__(self, x, y, image, font_size = None, color = None, background = None):
            if font_size == None and color == None and background == None:
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.image.load(image)
                pygame.draw.rect(self.image,(0,0,0),[50000,50000,0,0])
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
            else:
                pygame.sprite.Sprite.__init__(self)
                self.font = pygame.font.SysFont('Comic Sans MS', font_size)
                self.text = image
                self.color = color
                self.image = self.font.render(image,0,color,background)
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
    class menu(pygame.sprite.Sprite):
        def __init__(self, x, y, width, height,color):
            pygame.sprite.Sprite.__init__(self)
            self.rectangle = pygame.rect.Rect((x,y,width,height))
            pygame.draw.rect(screen,color,self.rectangle)
            self.text_group = []
            self.rect = self.rectangle
            self.rect.x = x
            self.rect.y = y
        def addText(self, text, x, y, color, background):
            text_sprite = self.font.render(text, 0, color, background)
            text_sprite.rect = text.get_rect()
            text_sprite.rect.x = x
            text_sprite.rect.y = y
            self.text_group.add(text_sprite)
        def removeText(self, text):
            self.text_group.remove(text)


def move(sprite,x=0,y=0):
    sprite.rect.x += x
    sprite.rect.y += y


test_menu = pygame_utils.menu(5, 5, 50, 50, (255, 255, 255))
#test_menu.addText('hello world', 5, 5, (0, 0, 0), (255, 255, 255))


# test_menu = pygame_utils.menu(100,100,500,500,(157,156,156))
test_button = pygame_utils.button(50,50,"images\\partyButton.png")
test_button_text = pygame_utils.button(100, 100, 'hello world', 20, (0, 0, 0), (150, 150, 150))
sprites_list.add(test_button)
sprites_list.add(test_button_text)
sprites_list.add(test_menu)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if test_button_text.rect.collidepoint(event.pos):
                pass

    sprites_list.update()
    screen.fill((255,255,255))
    sprites_list.draw(screen)
    pygame.display.flip()
