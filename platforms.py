from vector import Vector
height = 900
width = 800
import random

class Platform:
    def __init__(self,start,end,width,speed,baseRotation,colour):
        self.name = "Platform"
        self.start = start
        self.end = end
        self.width = width 
        self.speed = speed #positive = right, negative = left / positive = down, negative = up
        self.colour = colour
        self.rotation = baseRotation

    def draw(self,canvas):
        canvas.draw_line((self.start.x,self.start.y),(self.end.x,self.end.y),self.width,self.colour)

    def spin(self,direction):
        if direction == 1:
            self.start += self.rotation
            self.end -= self.rotation
        
            
    def move(self):
        self.start.x += self.speed.x
        self.end.x += self.speed.x
        self.start.y += self.speed.y
        self.end.y += self.speed.y
                
    def update(self,):
        self.move()
        self.spin(-1)
        #print(self.startY,self.endY)

class main: 
    def __init__(self):
        self.Platforms = []
        self.frame = 0
        self.lastY = height/2
        self.lastChoice = 0
        self.delay = 60
        self.worldSpeed = Vector(-5,0)
        
    def update(self,canvas):
        self.frame += 1
        self.delay -= 1
        for i in self.Platforms:
            i.update(canvas)
            if i.end.x <= 0 and i.start.x <= 0:
                self.Platforms.remove(i)
        if self.delay == 0:
            self.addPlatform()
            #print(self.Platforms)
        
    def addPreset1(self,Y): #3 platforms
            self.Platforms.append(Platform(Vector(600,Y),Vector(650,Y),5,self.worldSpeed,Vector(0,0),"red")) 
            self.Platforms.append(Platform(Vector(600,Y+50),Vector(650,Y+50),5,self.worldSpeed,Vector(0,0),"red"))
            self.Platforms.append(Platform(Vector(600,Y-50),Vector(650,Y-50),5,self.worldSpeed,Vector(0,0),"red"))
            self.delay = 60
            
    def addPreset2(self,Y):
        pass
    
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
        
            
        
#Main = main()     
     
