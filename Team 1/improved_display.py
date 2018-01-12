from quokka import *

class ImprovedQuokkaDisplay(QuokkaDisplay):
    def __init__(self, spi):
        super().__init__(spi)

    def draw_image(self, image, pos):
        '''
        Draw a 2D array of pixel values to the screen
        '''
        #TODO convert an image file to the 2D array
        for y in range(len(image)):
            for x in range(len(image[y])):
                if 0 < x+pos[0] < self.width and 0 < y+pos[1] < self.height:
                    self.pixel(x+pos[0], y+pos[1], image[y][x])
