import pygame
import os 
import sys
import pygame.freetype #load fonts

'''OBJECTS'''
# put classes & functions here

def stats(score):
     #display text, 1, colour (rgb)
     text_score = myfont.render("Score: "+str(score), 1, (250,147,249))
     screen.blit(text_score, (4, 4))

     
class Platform(pygame.sprite.Sprite):
     #x location, y location, img width, img height, img file)
     def __init__(self,xloc,yloc,imgw, imgh, img):
          pygame.sprite.Sprite.__init__(self)
          self.image = pygame.Surface([imgw, imgh])
          self.image.convert_alpha()
          self.image.set_colorkey(alpha)
          self.blockpic = pygame.image.load(img).convert()
          self.rect = self.image.get_rect()
          self.rect.y = yloc
          self.rect.x = xloc

          #paint image into blocks
          self.image.blit(self.blockpic, (0,0), (0,0,imgw,imgh))

     def level1():
          #create level 1
          platform_list = pygame.sprite.Group()
          block = Platform(0, 591, 500, 77,os.path.join('images','block0.png'))
          platform_list.add(block) #after each block
          

          block = Platform(800, 591, 500, 77,os.path.join('images','block1.png'))
          platform_list.add(block)

          block = Platform(1600, 591, 500, 77,os.path.join('images','block1.png'))
          platform_list.add(block)

          block = Platform(2400, 591, 500, 77,os.path.join('images','block1.png'))
          platform_list.add(block) 

          block = Platform(3200, 591, 500, 77,os.path.join('images','block1.png'))
          platform_list.add(block) 

          

          return platform_list #at end of function level1

     def loot1():
          loot1_list = pygame.sprite.Group()
          loot1 = Platform(70, 256, 256, 256,os.path.join('images','loot.png'))
          loot1_list.add(loot1)


          return loot1_list
          


     
          
          
     
               








class Player(pygame.sprite.Sprite):
     #Spawn a player
     def __init__(self):
          pygame.sprite.Sprite.__init__(self)
          self.momentumX = 0 #move along X
          self.momentumY = 0 #move along Y

          #gravity varibles
          self.collide_delta = 0
          self.jump_delta = 6

          self.score = 0 #set score
          self.damage = 0 #player is hit

          
          self.images = [  ]
          img = pygame.image.load(os.path.join('images','hero.png')).convert()
          
           
          self.images.append(img)
          self.image = self.images[0]
          self.rect = self.image.get_rect()
          self.hitbox = pygame.Rect(0,0,209, 150)
          '''self.rectcollide_pos = self.rect + 41
          self.rectcollide_size = self.rect - 41
          self.rectcollide = (self.rectcollide_pos, self.rectcollide_size)'''
          self.image.convert_alpha() #optimise for alpha
          self.image.set_colorkey(alpha) #set alpha

     def control (self, x, y):
          #control player movement
          self.momentumX += x
          self.momentumY += y

     def update(self, enemy_list, platform_list):
     
          #update sprite position
          self.hitbox.center = self.rect.center
          currentX = self.rect.x
          nextX = currentX + self.momentumX
          self.rect.x = nextX

          currentY = self.rect.y
          nextY = currentY + self.momentumY
          self.rect.y = nextY


          #collisions
          enemy_hit_list = pygame.sprite.spritecollide(self, enemy_list, False)          
          #for enemy in enemy_hit_list:
               #self.score -= 1
               #print(self.score)
          


          if self.damage == 0:
               for enemy in enemy_hit_list:
                    if not self.rect.contains(enemy):
                         self.damage = self.rect.colliderect(enemy)
                         print(self.score)



          if self.damage == 1:
               idx = self.rect.collidelist(enemy_hit_list)
               if idx == -1:
                    self.damage = 0 #set damage back to 0
                    self.score-= 1 #subtract 1 hp

          block_hit_list = pygame.sprite.spritecollide(self, platform_list, False)
          if self.momentumX > 0:
               for block in block_hit_list:
                    self.rect.y = currentY
                    self.rect.x = currentX+9
                    self.momentumY = 0
                    self.collide_delta = 0 #stop jumping
          if self.momentumY > 0:
               for block in block_hit_list:
                    self.rect.y = currentY
                    self.momentumY = 0
                    self.collide_delta = 0 #stop jumping

          loot_hit_list = pygame.sprite.spritecollide(self, loot1_list, False)
          for loot in loot_hit_list:
               loot1_list.remove(loot)
               self.score += 1
               print(self.score)
          
          
          
          
          


          #gravity
          if self.collide_delta < 6 and self.jump_delta < 6:
               self.jump_delta =6*2
               self.momentumY -=43 #how high to jump

               self.collide_delta +=6
               self.jump_delta +=6
          

     def jump (self, platform_list):
          self.jump_delta = 0
                    

     def gravity(self):
          self.momentumY += 3.2  #how fast player falls

          if self.rect.y >720 and self.momentumY >= 0:
               self.momentumY = 0
               self.rect.y = 0
               self.rect.x = 0
               #img = pygame.image.load(os.path.join('images','hero.png')).convert()




          


class Enemy(pygame.sprite.Sprite):
     #spawn an enemy
     def __init__(self,x,y,img):
          pygame.sprite.Sprite.__init__(self)
          self.image = pygame.image.load(os.path.join('images', img))
          self.image.convert_alpha()
          self.rect = self.image.get_rect()
          self.image.set_colorkey(alpha)
          self.rect.x = 500 
          self.rect.y = 550
          self.counter = 0 #counter varible
          
     def move(self):
          #enemy movement
          if self.counter >= 0 and self.counter <= 30:
               self.rect.x -= 2
          elif self.counter >= 30 and self.counter  <= 60:
               self.rect.x += 2

          else:
               self.counter = 0
               #print('reset')

          self.counter += 1

     def update(self,firepower, enemy_list):
          '''
          detect firepower collision
          '''

          fire_hit_list = pygame.sprite.spritecollide(self,firepower,False)
          for fire in fire_hit_list:
               enemy_list.remove(self)
class Throwable(pygame.sprite.Sprite):
     '''
     spawn a throwable object
     '''

     def __init__(self,x,y,img,throw):
          pygame.sprite.Sprite.__init__(self)
          self.image = pygame.image.load(os.path.join('images',img))
          self.image.convert_alpha()
          self.image.set_colorkey(alpha)
          self.rect = self.image.get_rect()
          self.rect.x = x
          self.rect.y = y
          self.firing = throw


     def update(self, screenY):
          '''
          throw physics
          '''
          if self.rect.y < screenY: #vertical axis
               self.rect.x += 15 #how fast it moves forward
               self.rect.y += 3 #how fast it falls
          else:
               self.kill()       #remove throwable object
               self.firing = 0 #free up firing slot

          if self.rect.y == 5:
               self.kill()       

          

     
     


               
'''SETUP'''
# code runs once
screenX = 960 #width
screenY = 720 #height
alpha = (0, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)


fps = 60 #frame rate
afps = 4 #animation cycles
clock = pygame.time.Clock()
pygame.init()
pygame.font.init() #start freetype

font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "fonts",
"amazdoom.ttf")
font_size = 64
myfont = pygame.font.Font(font_path, font_size)

main = True

screen = pygame.display.set_mode([screenX, screenY])
backdrop = pygame.image.load(os.path.join('images','stage.png')).convert()

platform_list = Platform.level1() #set stage to Level 1

backdropRect = screen.get_rect()

loot1_list = Platform.loot1()

player = Player() #Spawn player
player.rect.x = 0
player.rect.y = 0
movingsprites = pygame.sprite.Group()
movingsprites.add(player)
fire = Throwable(player.rect.x, player.rect.y, 'projectile.png',0)
firepower = pygame.sprite.Group()
movesteps = 10 #how fast to move

forwardX = 600 #when to scroll
backwardX = 150 #when to scroll

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


               if event.key == ord(' '):
                    player.jump(platform_list)
                    print('up')


               if event.key == pygame.K_UP or event.key == ord(' '):
                    player.jump(platform_list)

          if event.type == pygame.MOUSEBUTTONDOWN:
               if not fire.firing:
                    fire = Throwable(player.rect.x,player.rect.y,'projectile.png',1)
                    firepower.add(fire)
                    
                    


     #scroll world forward
     if player.rect.x >= forwardX:
          scroll = player.rect.x - forwardX
          player.rect.x = forwardX
          for enemy in enemy_list:
               enemy.rect.x -= scroll
          
          for platform in platform_list:
               platform.rect.x -= scroll
          for loot1 in loot1_list:
               loot1.rect.x -= scroll


     #scroll world backward
     if player.rect.x <= backwardX:
          scroll = backwardX - player.rect.x
          player.rect.x = backwardX
          for platform in platform_list:
               platform.rect.x += scroll
          for enemy in enemy_list:
               enemy.rect.x += scroll
          for loot1 in loot1_list:
               loot1.rect.x +=scroll



     screen.blit(backdrop, backdropRect)


     loot1_list.draw(screen)
     platform_list.draw(screen) #draw platforms on screen
     player.gravity() #check gravity
     player.update(enemy_list, platform_list) #update player postion
     enemy.move() #move enemy sprite

     stats(player.score) #draw text

     if fire.firing:
          fire.update(screenY)
          firepower.draw(screen)
          enemy_list.update(firepower,enemy_list)
     movingsprites.draw(screen)  #draw player
     enemy_list.draw(screen) #refresh enemies

     pygame.display.flip()
     clock.tick(fps)





