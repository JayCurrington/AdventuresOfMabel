try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector
import os 
WIDTH = 1500
HEIGHT = 900
script_dir = os.path.dirname(os.path.abspath(__file__))   

class Spritesheet:
    def __init__(self, url, rows, columns, size, currentRow = 0, position = (0,0)):
        self.image = simplegui.load_image(url)
        self.rows = rows
        self.columns = columns
        self.position = position
        self.currentRow = currentRow
        self.size = size
        # x = columns across, y = rows down
        self.frame = (0,0)
        self.dimensions = (self.image.get_width(), self.image.get_height()) # total image
        self.frame_dimensions = (self.dimensions[0]/self.columns, self.dimensions[1]/self.rows) 
        # one frame dimension x and y

    def draw(self, canvas):
        clock.tick()
        x = self.frame[1] * self.frame_dimensions[0] + self.frame_dimensions[0] / 2
        # columns: current increment times the 
        y = self.frame[0] * self.frame_dimensions[1] + self.frame_dimensions[1] / 2
        # rows
        
        canvas.draw_image(self.image, 
                          (x, y), # center of that frame
                          self.frame_dimensions, #frame positions
                          self.position, #position in canvas
                          self.size) # size of image
        
        
        if not clock.transition(13): # holds the frame for arg ticks
            clock.time = 0
            self.next_frame()
        

    def next_frame(self):
        self.frame = (self.frame[0], (self.frame[1]+1) % self.columns) 
        # % changes back to zero), repeats the whole row
        
        # lines if you want to go down a row>>>>>
        #if self.frame[1] == 0: # if reached end of row
           
            #self.frame = ((self.frame[0] + 1) % self.rows, 0)
            #increment new row and set column to 0
            #sets row to 0 when it reaches num of rows (restart)
        
    def call_once(self):
        if self.frame[1] != self.columns+1:
            self.frame = (self.frame[0], (self.frame[1]+1))

class Clock:
    def __init__(self):
        self.time = 0
    
    def tick(self):
        self.time += 1
    
    def transition(self, frame_duration):
        return self.time < frame_duration 
clock = Clock()   
    
''' 
spritesheet = Spritesheet(os.path.join(script_dir, 'assets', 'mabelsprite.png'), 
                          3,5, 10)



explosions = []

frame = simplegui.create_frame('Sprite Mabel', WIDTH, HEIGHT)
frame.set_draw_handler(spritesheet.draw)
frame.set_canvas_background('White')
frame.start()'''