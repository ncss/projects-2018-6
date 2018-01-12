import serial
import pygame

pygame.init()

size = list(pygame.display.list_modes()[-1])
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

scale_size = [size[0], (size[0]*2)//3]

ser = serial.Serial()
ser.baudrate = 115200

ser.port = 'a'#input('Port of Quokka/Microbit: ')

# ser.open()

SPLASH = 0
WAITING = 1
BATTLE_WAITING = 2
BATTLE_RUNNING = 3
GAME_OVER = 4

state = SPLASH

#TODO Find a way to read serial data nicely

# Load the resources
end_font = font = pygame.font.SysFont(None, 10)

backround_img = pygame.transform.scale(pygame.image.load('resources/background.png'), scale_size).convert()
splash = pygame.image.load('resources/splash.png').convert_alpha()
scale = [size[0], int((size[0]/splash.get_width())*splash.get_height())]
splash = pygame.transform.scale(splash, scale)

clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ser.close()
            pygame.quit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            ser.close()
            pygame.quit()

    screen.fill((0, 0, 0))

    if state == SPLASH:
        screen.blit(backround_img, [0, (size[1]-scale_size[1])//2])
        screen.blit(splash, [0, (size[1]+(size[1]-scale_size[1])-splash.get_height())//2])

    elif state == GAME_OVER:
        screen.blit(backround_img, [0, (size[1]-scale_size[1])//2])

        winner = 1

        text = end_font.render('Player {} won!'.format(winner), True, (0, 0, 0))

    pygame.display.flip()
