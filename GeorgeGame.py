import pygame
import os 
import sys

'''OBJECTS'''
# put classes & functions here
class Player(pygame.sprite.Sprite):
     #Spawn a player
     def __init__(self):
          pygame.sprite.Sprite.__init(self)
          self.images = [  ]
          img = pygame.image.load(os.path.join('images','hero.png')).convert()
          self.images.append(img)
          self.image = self.images[0]
          self.rect = self.image.get_rect()
          
          
        



'''SETUP'''
# code runs once
screenX = 960 #width
screenY = 720 #heightll

fps = 60 #frame rate
afps = 4 #animation cycles
clock = pygame.time.Clock()
pygame.init()

main = True

screen = pygame.display.set_mode([screenX, screenY])
backdrop = pygame.image.load(os.path.join('images','stage.png')).convert()
backdropRect = screen.get_rect()

player = Player() #Spawn player
player.rect.x = 0
player.rect.x = 0
movingsprites = pygame.sprite.Group()
movingsprites.add(player)


'''MAIN LOOP'''
# code runs many times
while main == True:
    for event in pygame.event.get():
        if  event.type == pygame.KEYUP:
            if event.key == ord('q'):
                pygame.quit()
                sys.exit()
                main = False


    screen.blit(backdrop, backdropRect)
    pygame.display.flip()
    clock.tick(fps)




