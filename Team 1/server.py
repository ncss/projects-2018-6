from microbit import *
import radio

# 8 is client1 dedicated, 10 is client2 dedicated, 14 is everything else
channels = [8, 10, 14]

radio.on()
radio.config(length=251)

connected_clients = []

# TODO Replace this
pokemans = ['venusaur']

# Setup states
POLL_CLIENTS = 0 # Connect the clients to the server
CLIENT_SETUP = 1 # Choose pokemon
POLL_BATTLE = 2 # Wait for moves to be chosen by the clients
RUN_BATTLE = 3 # Run a simulation of the battle with the chosen moves
TRANSFER_BATTLE = 4 # Transfer the results of the turn back to the clients
GAME_FINISH = 5 # Send game total results back to clients
RESET = 6 # Reset everything

state = POLL_CLIENTS

class Client:
    def __init__(self, channel):
        self.channel = channel
        self.pokemon = []
        self.current_pokemon = 0

    def send_message(self, message):
        if len(message) > 250:
            raise Exception('The message is too long and we need to rewrite this code. :\'(')
        radio.config(channel=self.channel)
        radio.send(message)

    def recv_message(self):
        radio.config(channel=self.channel)
        return radio.receive()

def poll_clients():
    '''
    Poll for incoming connections from clients
    '''
    global channels
    global connected_clients

    for channel in channels:
        radio.config(channel=channel)
        msg = radio.receive()
        if msg == "connect":
            # Handle the reception of a message here
            if channel in [client.channel for client in connected_clients]:
                client.send_message('confirm')
                continue
            connected_clients.append(Client(channel))
            connected_clients[-1].send_message('confirm')

    if len(connected_clients) >= 2:
        # start the game
        state = CLIENT_SETUP
        connected_clients = connected_clients[:2]
        for client in connected_clients:
            client.send_message('server_ready')

def client_setup():
    '''
    Poll for setup data from the clients
    '''
    if all([bool(client.pokemon) for client in connected_clients]):
        state = POLL_BATTLE
        for client in connected_clients:
            client.send_message('start_battle')
        return

    for c, client in enumerate(connected_clients):
        msg = client.recv_message()
        if msg and '|' in msg:
            if client.pokemon:
                client.send_message('confirm')
                continue

            pokemon = [pokemans[int(i)] for i in msg.split('|')]
            connected_clients[c].pokemon = pokemon
            client.send_message('confirm')

def poll_battle():
    pass

while True:
    state_actions = {
                     POLL_CLIENTS : poll_clients,
                     CLIENT_SETUP : client_setup,

                     RESET : reset
                    }
    # Run the corresponding function for the current state
    state_actions[state]()

    # if state == POLL_CLIENTS:
    #     poll_clients()
    #
    # elif state == CLIENT_SETUP:
    #     client_setup()
    #
    # elif state == POLL_BATTLE:
    #     pass
    #
    # elif state == RUN_BATTLE:
    #     pass
    #
    # elif state == TRANSFER_BATTLE:
    #     pass
    #
    # elif state == GAME_FINISH:
    #     pass
    #
    # elif state == RESET:
    #     reset()
