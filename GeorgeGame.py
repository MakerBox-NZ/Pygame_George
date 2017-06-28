import pygame
import os 
import sys

'''OBJECTS'''
# put classes & functions here
class Player(pygame.sprite.Sprite):
     #Spawn a player
     def __init__(self):
          pygame.sprite.Sprite.__init__(self)
          self.momentumX = 0 #move along X
          self.momentumY = 0 #move along Y
          self.images = [  ]
          img = pygame.image.load(os.path.join('images','hero.png')).convert()
          self.images.append(img)
          self.image = self.images[0]
          self.rect = self.image.get_rect()
          self.image.convert_alpha() #optimise for alpha
          self.image.set_colorkey(alpha) #set alpha

     def control (self, x, y):
          #control player movement
          self.momentumX += x
          self.momentumY += y

     def update(self):
          #update sprite position
          currentX = self.rect.x
          nextX = currentX + self.momentumX
          self.rect.x = nextX

          currentY = self.rect.y
          nextY = currentY + self.momentumY
          self.rect.y = nextY


class Enemy(pygame.sprite.Sprite):
     #spawn an enemy
     def __init__(self,x,y,img):
          pygame.sprite.Sprite.__init__(self)
          self.image = pygame.image.load(os.path.join('images', img))
          self.image.convert_alpha()
          self.image.set_colorkey(alpha)
          self.rect.x = x
          self.rect.y = y
          self.counter = 0 #counter varible
          
     def move(self):
          #enemy movement
          if self.counter >= 0 and self.counter <= 30:
               self.rect.x -= 2
          elif self.counter >= 30 and self.counter  <= 60:
               self.rect.x == 2

          else:
               self.counter = 0
               print('reset')

          self.counter += 1



'''SETUP'''
# code runs once
screenX = 960 #width
screenY = 720 #height
alpha = (0, 0, 0)
black = (1, 1, 1)
white = (255, 255, 255)


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
player.rect.y = 0
movingsprites = pygame.sprite.Group()
movingsprites.add(player)
movesteps = 10 #how fast to move

#enemy code
enemy = Enemy(100,50,'enemy.png') #spawn enemy
enemy_list = pygame.sprite.Group() #create enemy group
enemy_list.add(enemy) #add enemy to group

'''MAIN LOOP'''
# code runs many times
while main == True:
    for event in pygame.event.get():
        if  event.type == pygame.KEYDOWN:
          if event.key == ord('q'):
                pygame.quit()
                sys.exit()
                main = False
          if event.key == ord('a'):
               player.control(-movesteps, 0)
               print('left stop')
          if event.key == ord('d'):
               player.control(movesteps, 0)
               print('right stop')
          if event.key == ord('w'):
               print('up stop')

        if event.type == pygame.KEYUP:
         if event.key == ord('a'):
               player.control(movesteps, 0)
               print('left')
         if event.key == ord('d'):
               player.control(-movesteps, 0)
               print('right')
         if event.key == ord('w'):
               print('up')


    screen.blit(backdrop, backdropRect)
    player.update() #update player postion
    movingsprites.draw(screen)  #draw player
    enemy_list.draw(screen) #refresh enemies
    enemy.move() #move enemy sprite
    


    


                    
    pygame.display.flip()
    clock.tick(fps)





