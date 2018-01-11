from microbit import *
import random
import radio
moves = ['wip', 'nay-nay', 'dab', 'shakkas']
speed = 1000
n = len(moves)
time = 5000
# play the game
while True:
  choice = random.randrange(n)
  display.scroll(moves[choice], wait=False, loop=True)
  if choice == 0:
    pass
  if choice == 1:
    pass
  if choice == 2:
    pass
  if choice == 3:
    pass
  sleep(time)
  time -= 100
