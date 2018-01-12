from quokka import *
import framebuf

class ImprovedQuokkaDisplay(QuokkaDisplay):
    def __init__(self, spi):
        super().__init__(spi)

    def draw_image(self, image, pos):
        '''
        Draw a 2D array of pixel values to the screen
        '''
        for y in range(len(image)):
            for x in range(len(image[y])):
                if 0 < x+pos[0] < self.width and 0 < y+pos[1] < self.height:
                    self.pixel(x+pos[0], y+pos[1], int(image[y][x]))

class SpecialFrameBuffer(framebuf.FrameBuffer):
    def __init__(self, buf, w, h, mode):
        super().__init__(buf, w, h, mode)
        self.width = w
        self.height = h

    def draw_image(self, image, pos):
        '''
        Draw a 2D array of pixel values to the framebuffer
        '''
        for y in range(len(image)):
            for x in range(len(image[y])):
                if 0 < x+pos[0] < self.width and 0 < y+pos[1] < self.height:
                    self.pixel(x+pos[0], y+pos[1], int(image[y][x]))
