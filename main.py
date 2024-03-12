#from level1 import Vector
from spritesheet import Spritesheet, Clock

from vector import Vector
from tiles import Tile
from platforms import Platform
import random
import os

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import math
WIDTH = 900#1980
HEIGHT = 700#1200
directory = os.path.dirname(os.path.abspath(__file__))            
global scroll_pos # used to move all objects right to left
scroll_pos = 0

simplegui.KEY_MAP['shift'] = 17
  
class Player:
    def __init__(self, pos, radius, sprite):
        self.pos = pos
        self.vel = Vector()
        self.radius = max(radius, 10)
        self.colour = 'Black'
        self.sprite = sprite
        self.lives = 3
        self.is_jumping = False
        self.double_jump = False
        self.jump_cooldown = 60
        self.move_direction = 0
        self.dash_cooldown = 60 # in frames

    def draw(self, canvas):
        #canvas.draw_image(floatingmabeltest.image, (256, 256), (512, 512), (self.pos.x-WIDTH,self.pos.y), (2*self.radius, 2*self.radius))
        #canvas.draw_image(floatingmabeltest.image, (256, 256), (512, 512), (self.pos.x+WIDTH,self.pos.y), (2*self.radius, 2*self.radius))
        #canvas.draw_image(self.sprite.image, (256, 256), (512, 512), self.pos.get_p(), (2*self.radius, 2*self.radius))
        pass
        
        
    def update(self):
        self.pos.add(self.vel)
        self.vel.multiply(0.85)
        if self.on_ground():
            self.is_jumping = False
            self.double_jump = False
            self.vel.y = 0
            self.move_direction = 0
        
        if self.is_jumping:
            self.vel.add(Vector(0, 2))
            self.vel.add(Vector(self.move_direction, 0))
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1
        if self.on_ground():
            self.jump_cooldown = 0

        
    def jump(self):
        if not self.is_jumping and self.on_ground():
            # if not jumping and on ground then jump and set true
            self.vel.add(Vector(0, -70))
            #jump_sound.play()a
            #jump_sound.rewind()
            self.is_jumping = True
            self.move_direction = 0.3 if inter.keyboard.right else -0.3 if inter.keyboard.left else 0
            inter.keyboard.jump = False
        if self.is_jumping and not self.on_ground():
            self.air_jump()
    
    def dash(self):
        self.move_direction = 1 if inter.keyboard.right else -1 if inter.keyboard.left else 0
        if self.dash_cooldown == 0:
            if self.is_jumping:
                self.vel.add(Vector(50*self.move_direction, -25))#counteract gravity
            else:
                self.vel.add(Vector(50*self.move_direction, 0)) # on ground
            inter.background.scroll_pos.add(Vector(-1*self.move_direction,0))
            self.dash_cooldown = 60 # 1 second cooldown 

    

    def air_jump(self):
        if self.jump_cooldown == 0: # if has touched ground set 0
            air_jump_smoke.position = spritesheet.position
            air_jump_smoke.call_once()
            self.vel.add(Vector(20*self.move_direction, -60))
            self.jump_cooldown = 1 # cannot be repeatde until touch ground again
            # add smoke sprite beneath and sfx
            # call when space pressed not permenant

            
        #if not self.on_ground() and self.is_jumping() and inter.keyboard.jump and not self.double_jump:
         #   self.double_jump = True
          #  self.vel.add(Vector(0, -100))
    
    def check_lives(self): # called when the player gets hit, if falls out then insta death if fell ino void true
        self.lives -= 1
        if self.lives == 0:
            self.die()
        
    def die(self): # when lives = 0
        # update sprite animation to change into mist??
        # call sound undertale heart rip sfx
        # call reset function - scroll to 0, spawn back in idk - recall class exit out osmehow
        pass
            
    def on_ground(self): # change to die when on ground, add new function to platform class to detect if its on them
        # center + rad = height -2
        return self.pos.y+self.radius >= HEIGHT-2
    
    def fell_into_void(self):
        return self.pos.y+self.radius >= HEIGHT
     
class Background:
    def __init__(self):
        self.layer1 = simplegui.load_image(os.path.join(directory, 'assets/background', 'bg_forest.png'))
      
        self.layer3 = simplegui.load_image('http://www.cs.rhul.ac.uk/courses/CS1830/sprites/background_clouds.png')
        self.scroll_pos = Vector(WIDTH/2, HEIGHT/2)
        
        #self.layer_position = [Vector(WIDTH/2,0), Vector(WIDTH/2,0), Vector(WIDTH/2,0), Vector(WIDTH/2,0)]
        self.speed = 0.3  # speed of auto scroll
 
    
    def update(self):
        self.scroll_pos.subtract(Vector(self.speed, 0)) # move right to left
        if self.scroll_pos.x <= 0:
            self.scroll_pos.x = WIDTH/2
            
    def draw(self, canvas):
        canvas.draw_image(self.layer1, 
                          (self.layer1.get_width() / 2, self.layer1.get_height() / 2), # center of image
                          (self.layer1.get_width(), self.layer1.get_height()), # size of original
                          (self.scroll_pos.x, self.scroll_pos.y), # where image is drawn on canvas
                          (self.layer1.get_width(), HEIGHT)) # size of drawn image 
        canvas.draw_image(self.layer1, 
                          (self.layer1.get_width() / 2, self.layer1.get_height() / 2), # center of image
                          (self.layer1.get_width(), self.layer1.get_height()), # size of original
                          (self.scroll_pos.x+WIDTH, self.scroll_pos.y), # where image is drawn on canvas
                          (self.layer1.get_width(), HEIGHT)) # size of drawn image 
        canvas.draw_image(self.layer3, 
                          (self.layer3.get_width() / 2, self.layer3.get_height() / 2), # center of image
                          (self.layer3.get_width(), self.layer3.get_height()), # size of original
                          (self.scroll_pos.x*1.4, self.scroll_pos.y-350), # where image is drawn on canvas
                          (WIDTH, HEIGHT/2)) # size of drawn image 
     
        
class Keyboard:
    def __init__(self):
        self.right = False
        self.left = False
        self.jump = False
        self.dash = False
        self.duck = False

    def keyDown(self, key):
        if key == simplegui.KEY_MAP['d']:
            self.right = True
        if key == simplegui.KEY_MAP['a']:
            self.left = True
        if key == simplegui.KEY_MAP['space'] or key == simplegui.KEY_MAP['w']:
            self.jump = True
        if key == simplegui.KEY_MAP['s'] :
            self.duck = True
        if key == simplegui.KEY_MAP['shift']:
            self.dash = True

    def keyUp(self, key):
        if key == simplegui.KEY_MAP['d']:
            self.right = False
        if key == simplegui.KEY_MAP['a']:
            self.left = False
        if key == simplegui.KEY_MAP['space'] or key == simplegui.KEY_MAP['w']:
            self.jump = False
        if key == simplegui.KEY_MAP['s']:
            self.duck = False
        if key == simplegui.KEY_MAP['shift']:
            self.dash = False
            
class Interaction:
    def __init__(self, Player, keyboard, background, tile):
        self.Player = Player
        self.keyboard = keyboard
        self.background = background
        self.tile = tile

        # platforms
        self.Platforms = []
        self.frame = 0
        self.lastY = HEIGHT/2
        self.lastChoice = 0
        self.delay = 60
        self.worldSpeed = Vector(-5,0)

    def update(self):
        dash_lines.position = spritesheet.position = tuple(t1 - t2 for t1, t2 in zip(self.Player.pos.get_p(), (0,50))) # counters the height of sprite, could be made better 
        #dash_lines.position = tuple(t1 - t2 for t1, t2 in zip(self.Player.pos.get_p(), (0,50)))
        # updates dash sprite to current position
        if not (self.keyboard.right or self.keyboard.left or self.keyboard.jump or self.keyboard.duck or self.keyboard.dash):
            self.Player.sprite.frame = (0,self.Player.sprite.frame[1]) # idle animation
        if self.keyboard.jump:
            self.Player.jump()
            self.Player.sprite.frame = (3,self.Player.sprite.frame[1])

        if self.keyboard.left:
            self.Player.vel.add(Vector(-1, 0)) 
            self.background.scroll_pos.add(Vector(1.2,0))
            self.Player.sprite.frame = (1,self.Player.sprite.frame[1])
        if self.keyboard.right:
            self.Player.vel.add(Vector(1, 0))
            self.background.scroll_pos.add(Vector(-0.6,0)) # moves bg with player
            self.Player.sprite.frame = (2,self.Player.sprite.frame[1]) # changes row of sheet to reflect direction
        if self.keyboard.duck:
            self.Player.sprite.frame = (4,self.Player.sprite.frame[1])
            # ADD MOVEMENT DOWN THROUGH PLATFORMS and the sprite
        if self.keyboard.dash:
            self.Player.dash()
            #self.background.scroll_pos.add(Vector(-1*self.Player.move_direction,0)) # holding down key issue
            # remove ability to hold for background
        # if self.player.hit enemy and self.lives > 1then 
            #self.lives -=1 IMPLEMENT ONCE OTHER TEAM DONE
        if self.Player.lives == 0 or self.Player.fell_into_void():
            # ran out of lives or fell down then die and restart
            self.Player.die()
        # change this logic, the function handles most of it die()
            
        # platform class
        self.frame += 1
        self.delay -= 1
        for i in self.Platforms:
            i.update()
            if i.end.x <= 0 and i.start.x <= 0:
                self.Platforms.remove(i)
        if self.delay == 0:
            self.addPlatform()
            #print(self.Platforms)

            

        if self.Player.pos.x+self.Player.radius >= WIDTH: # right to left block
            self.Player.pos.x = WIDTH-1-self.Player.radius
        if self.Player.pos.x-self.Player.radius <= 0: # left to right block
            self.Player.pos.x = 1+self.Player.radius

    def addPlatform(self):
        choice = random.randint(1,4)
        Y = self.lastY
        self.delay = 60
        if choice == 1 or self.lastY >= 350: #basic platform
            if self.lastChoice == 2:
                Y = random.randint(50,350)
            else: 
                Y = random.randint(100,400)
            self.Platforms.append(Platform(Vector(600,Y),Vector(700,Y),5,self.worldSpeed,Vector(0,0),"red")) 
            self.delay = 70
        elif choice == 2: #wall
            Y = random.randint(200,350)
            self.delay = 60
            self.Platforms.append(Platform(Vector(600,Y),Vector(600,Y+100),5,self.worldSpeed,Vector(0,0),"red"))
        elif choice == 3: #spinner
            Y = random.randint(200,350)
            self.delay = 30
            self.Platforms.append(Platform(Vector(600,Y),Vector(600,Y+100),5,self.worldSpeed,Vector(10,-10),"red"))
        else:
            preset = random.randint(1,3)
            if preset == 1:
                Y = random.randint(200,300)
                self.addPreset1(Y)
            elif preset == 2:
                Y = random.randint(100,300)
                self.addPreset2(Y)
            else:
                pass
        
        
        self.lastY = Y
        self.lastChoice = choice

    def addPreset1(self,Y): #3 platforms
            self.Platforms.append(Platform(Vector(600,Y),Vector(650,Y),5,self.worldSpeed,Vector(0,0),"red")) 
            self.Platforms.append(Platform(Vector(600,Y+50),Vector(650,Y+50),5,self.worldSpeed,Vector(0,0),"red"))
            self.Platforms.append(Platform(Vector(600,Y-50),Vector(650,Y-50),5,self.worldSpeed,Vector(0,0),"red"))
            self.delay = 60
            
    def addPreset2(self,Y):
        pass


spritesheet = Spritesheet(os.path.join(directory, 'assets/mabel', 'mabelsprite.png'), 
                          3,5, (200,200)) # test

#new sprite not final mabel pokemon temp
spritesheet = Spritesheet(os.path.join(directory, 'assets/mabel', 'playersprite.png'), 
                          4,4, (200,200)) 

healthbar = Spritesheet(os.path.join(directory, 'assets/menu', 'healthbar.png'), 
                          4,4, (200,200)) 

air_jump_smoke = Spritesheet(os.path.join(directory, 'assets/mabel', 'air_jump_smoke.png'), 
                          1,1, (150,100), 2, (-200,-200)) 

dash_lines = Spritesheet(os.path.join(directory, 'assets/mabel', 'dash_sprite.png'), 
                          1,1, (200,200)) 

# load sound files
#jump_sound = simplegui.load_sound(os.path.join(directory, 'assets/sound', 'jumpsound.webm'))
# use watergirl jump sfx bookmarked 
# smoke sfx for double jump or dash terraria?



# progress track
level_1 = False
level_2 = False
level_3 = False


kbd = Keyboard()
mabel = Player(Vector(WIDTH/2-450, HEIGHT-40), 40, spritesheet)
background = Background()

# start and end platforms
start_podium = [[1] * 6 for _ in range(10)]
tile = Tile(start_podium, (WIDTH/2, HEIGHT/2))

inter = Interaction(mabel, kbd, background, tile)

def draw(canvas):
    inter.update()
    mabel.update()
    background.update()
    background.draw(canvas)

    for i in inter.Platforms:
        i.draw(canvas)
    spritesheet.draw(canvas)
    air_jump_smoke.draw(canvas)
    mabel.draw(canvas)
    #tile.draw(canvas) start and end podiums

def start_game(): # frame arg add and #out first line
    frame = simplegui.create_frame("Mabel's Mayhem", WIDTH, HEIGHT)
    frame.set_draw_handler(draw)
    frame.set_keydown_handler(kbd.keyDown)
    frame.set_canvas_background('#7393B3')
    frame.set_keyup_handler(kbd.keyUp)
    frame.start()

start_game()