
import os
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

directory = os.path.dirname(os.path.abspath(__file__)) 
# Load the tile image
tile_image = simplegui.load_image(os.path.join(directory, 'assets/platform_tiles', 'tile1.png'))

tile_width = 50
tile_height = 50


class Tile:
    def __init__(self, layout, position):
        self.layout = layout
        self.position = position

    def draw(self, canvas):
        for y, row in enumerate(self.layout):
            for x, tile in enumerate(row):
                if tile == 1:
                    canvas.draw_image(tile_image, 
                                    (tile_width/2, tile_height / 2), 
                                    (tile_width, tile_height), 
                                    (x * tile_width + tile_width / 2, y * tile_height + tile_height / 2), 
                                    #1*50 + 25, 
                                    (tile_width, tile_height))
