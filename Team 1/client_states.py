from quokka import *

from BattleStuff import *
from math import ceil
import random

pokemon_list = pokemans

class Client:
    def __init__(self):
        self.id = None
        self.pokemon = []
        self.win_status = None
        self.messages = []
        self.connected = False
        self.last_attempt_time = 0

    def send_msg(self, msg):
        s = random.randint(10, 100)
        sleep(s)
        print("Sending {} with delay {}".format(msg, s))
        radio.send("{}:{}".format(self.id, msg))

    def get_pokemon(self):
        for pokemon in self.pokemon:
            if not pokemon.fainted:
                return pokemon
        self.win_status = 'You lost!'
        return self.pokemon[0]

    def recv_msg(self):
        if len(self.messages) > 0:
            return self.messages.pop(0)
        return None

    def handle_receive(self, client_id, msg):
        if client_id != self.id:
            # Message is not for us
            return
        print("Message appended: {}".format(msg))
        self.messages.append(msg)


class ImprovedQuokkaDisplay(QuokkaDisplay):
    def __init__(self, spi):
        super().__init__(spi)

    def draw_image(self, image, pos):
        '''
        Draw a 2D array of pixel values to the screen
        '''
        for y in range(56):
            for x in range(7):
                try:
                    byte = image[y*7 + x]
                except IndexError:
                    print(y*7+x)
                for bit in range(8):
                    self.pixel(pos[0]+x*8+bit, pos[1]+y, (byte & (1 << (7-bit))) >> (7-bit))

image_bytes = open('images.dat', 'rb').read()
imgs = {
        'venusaur' : image_bytes[:392],
        'charizard' : image_bytes[392:392*2],
        'blastoise' : image_bytes[392*2:]
        }

display = ImprovedQuokkaDisplay(display.spi)

unaddressed_msg_queue = []

client = Client()

# Initialise the states
CALIBRATE = 0
CONNECT_SERVER = 1
CHOOSE_POKEMON = 2
CHOOSE_MOVE = 3
READ_ZMOVE = 4
TRANSFER_BATTLE = 5
DISPLAY_TURN = 6
RESULT_SCREEN = 7
RESET = 8

state = CALIBRATE

def radio_loop():
    msg = radio.receive()
    if msg is not None:
        if ":" in msg:
            client_id, msg = msg.split(":", 1)
            try:
                client_id = int(client_id)
            except ValueError:
                #Non-numeric client ids can be added to the unaddressed queue
                unaddressed_msg_queue.append("{}:{}".format(client_id, msg))
            client.handle_receive(client_id, msg)
        else:
            unaddressed_msg_queue.append(msg)

def calibrate(unaddressed_msg_queue, client):
    client.last_attempt_time = running_time()
    return CONNECT_SERVER

def connect_to_server(unaddressed_msg_queue, client):


    # Try and receive an unaddressed message
    if len(unaddressed_msg_queue) == 0:
        msg = None
    else:
        msg = unaddressed_msg_queue.pop(0)

    if client.connected:
        if msg == "server_ready":
            return CHOOSE_POKEMON

    if msg is not None and ":" in msg:
        status, client_id = msg.split(":", 1)
        if status == "confirm" and client.connected == False:
            client.connected = True
            client.id = int(client_id)
            # Draw the waiting message
            display.fill(1)
            display.text('Waiting for', 20, 22, 0)
            display.text('server...', 28, 34, 0)
            # Wait for server_ready
            return CONNECT_SERVER

    # If this client hasn't connected, attempt to connect every half second
    if not client.connected and running_time()-client.last_attempt_time > 500:
        display.fill(1)
        display.text('Connecting...', 12, 22, 0)

        client.last_attempt_time = running_time()
        radio.send('connect')

    display.show()

    return CONNECT_SERVER

def choose_pokemon(unaddressed_msg_queue, client):
    '''
    Draw the choose pokemon screen and handle the buttons
    '''
    global pokemon_list

    pokemon_indices = [0]
    selection = 0

    start = running_time()
    while True:
        radio_loop()
        if selection < 1:
            # Display is 128 x 64
            # button.a = A button
            # button.d = B button
            # button.b = C button
            # button.c = D button
            if buttons.a.was_pressed():
                pokemon_indices[selection]  = (pokemon_indices[selection]-1)%len(pokemon_list)
            if buttons.d.was_pressed():
                pokemon_indices[selection]  = (pokemon_indices[selection]+1)%len(pokemon_list)
            if buttons.b.was_pressed():
                selection += 1

        # Draw the screen
        display.fill(1)
        if selection < 1:
            # Draw pokemon
            display.draw_image(imgs[pokemon_list[pokemon_indices[selection]].name.lower()], [36, 4])

            # Draw the arrows and push them toward the edges if the button is held
            display.text('<', 10-5*int(buttons.a.is_pressed()), 28, 0)
            display.text('>', 110+5*int(buttons.d.is_pressed()), 28, 0)
        else:
            # Draw the waiting message
            display.text('Waiting for', 20, 22, 0)
            display.text('server...', 28, 34, 0)

            client.pokemon = [pokemon_list[a] for a in pokemon_indices]

            display.show()

            if len(unaddressed_msg_queue) > 0:
                msg = unaddressed_msg_queue.pop(0)
            else:
                msg = ""
            last_attempt_time = running_time()-500
            connected = False

            while msg != "start_battle":
                radio_loop()

                msg = client.recv_msg()
                if msg is not None:
                    if msg == "confirm":
                        connected = True

                if not connected and running_time()-last_attempt_time > 500:
                    last_attempt_time = running_time()
                    # Send the required information about the pokemon to the server
                    client.send_msg('|'.join([str(a) for a in pokemon_indices]))

                if len(unaddressed_msg_queue) > 0:
                    msg = unaddressed_msg_queue.pop(0)
                else:
                    msg = ""

            return CHOOSE_MOVE

        display.show()

        if running_time()-start < 33:
            sleep(int(33.34-(running_time()-start)))
    return CHOOSE_POKEMON

def choose_move(unaddressed_msg_queue, client):
    pokemon = client.get_pokemon()
    if pokemon is None:
        return RESULT_SCREEN
    moves = pokemon.moves

    move_selector = 0

    while True:
        radio_loop()
        display.fill(1)

        if len(unaddressed_msg_queue) > 0:
            msg = unaddressed_msg_queue.pop(0)
        else:
            msg = ""

        if msg == 'GAME_OVER':
            return RESULT_SCREEN

        # Iterate the possible moves, and draw them
        # Also draw an indicator of the current selection
        for l, line in enumerate([move.name for move in moves]):
            y = 10+18*l
            display.text('>'*int(l == move_selector)+' '+line, 20, y, 0)

        display.show()

        # If the A button is pressed, iterate the selector
        # If the C button is pressed, make the selection
        if buttons.a.was_pressed():
            move_selector = (move_selector+1)%len(moves)
        if buttons.b.was_pressed():
            # Store the move choice somewhere
            pokemon.moveIndex = move_selector

            display.fill(1)

            # Draw the waiting message
            display.text('Waiting for', 20, 22, 0)
            display.text('server...', 28, 34, 0)

            display.show()

            return READ_ZMOVE

def read_zmove(unaddressed_msg_queue, client):
    # TODO get the quality of the z-move in range 1-10
    print('here!!!')
    return TRANSFER_BATTLE

def transfer_battle(unaddressed_msg_queue, client):
    # Part 1, send the info
    # Send the move to the server
    message = str(client.get_pokemon().moveIndex)+'|'+str(client.get_pokemon())
    msg = client.recv_msg()
    last_attempt_time = running_time()-500

    while msg != "confirm":
        print(msg)
        radio_loop()
        if running_time()-last_attempt_time > 500:
            last_attempt_time = running_time()
            # Send the required information about the turn to the server
            client.send_msg('action:'+message)

        msg = client.recv_msg()

    # Part 2, receive the results back and send a confirmation
    msg = client.recv_msg()
    while True:
        radio_loop()
        print(msg)
        if msg is None:
            msg = client.recv_msg()
            continue
        hp, messages = msg.split("|", 1)
        try:
            hp = int(hp)
            break
        except ValueError:
            continue
        msg = client.recv_msg()


    print(msg)

    # Store the turn information messages, then send confirmation
    hp, *messages = msg.split('|')
    hp = int(hp)
    msg = ""
    while msg != "both_confirm":
        if client.recv_msg() is not None:
            client.send_msg('confirm')
        radio_loop()
        if len(unaddressed_msg_queue) > 0:
            msg = unaddressed_msg_queue.pop(0)
        else:
            msg = ""

    client.messages = messages
    client.get_pokemon().hp = hp

    # Set state as necessary
    return DISPLAY_TURN

def display_turn(unaddressed_msg_queue, client):
    # Display the battle actions however we want to
    # get messages
    messages = client.messages
    end_after = False

    # Determine if the game is over or not
    if client.pokemon[0].hp <= 0:
        end_after = True

    for message in messages:
        message = [message]
        display.fill(1)

        if len(message[0]) > 14:
            message = [message[0][a*14:(a+1)*14] for a in range(ceil(len(message)/14))]

        for m, msg in enumerate(message):
            # Calculate the coords for the text
            top_pos = 32-(8+12*(len(message)-1))//2
            y = top_pos+12*m #12 pixels per row #28 is middle
            x = (128-8*len(msg))//2
            display.text(msg, x, y, 0)

        hp  = 'Your HP: '+str(client.pokemon[0].hp)
        display.text(hp, 64-(4*len(hp)), 40, 0)

        display.show()
        sleep(500)

    return CHOOSE_MOVE if not end_after else RESULT_SCREEN

def result_screen(unaddressed_msg_queue, client):
    # get the actual result
    result = 'You lost!' if client.pokemon[0].hp < 0 else 'You won!'

    while not buttons.c.was_pressed():
        display.fill(1)

        display.text(result, (128-8*len(result))//2, 28, 0)

        display.show()

    return RESET
