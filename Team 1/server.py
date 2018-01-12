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
        self.message_buffer = None

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

    # Loop the channels, listening for connecting clients
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

    # If two (or more) clients have connected, start the game with the first two who connected
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
    # If all clients have connected and confirmed their pokemon lists
    if all([bool(client.pokemon) for client in connected_clients]):
        state = POLL_BATTLE
        for client in connected_clients:
            client.send_message('start_battle')
        return

    # Loop the connected clients, listening for the pokemon choices
    for c, client in enumerate(connected_clients):
        msg = client.recv_message()
        if msg and '|' in msg:
            # If the pokemon has already been sent, send another confirmation message back to the client
            if client.pokemon:
                client.send_message('confirm')
                continue

            pokemon = [pokemans[int(i)] for i in msg.split('|')]
            connected_clients[c].pokemon = pokemon
            client.send_message('confirm')

def poll_battle():
    '''
    Poll for incoming battle actions from clients
    '''
    global connected_clients

    for c, client in enumerate(connected_clients):
        msg = client.recv_message()
        if msg.startswith("action:"):
            # Handle the reception of a message here
            # if the action has already been received, skip it
            if client.message_buffer:
                client.send_message('confirm')
                continue
            # else, store in the buffer ready for the next state
            connected_clients[c].message_buffer = msg
            client.send_message('confirm')

    # If both clients have sent actions,
    # return a message and move to next state
    if all([client.message_buffer for client in connected_clients]):
        # start the battle simulation
        state = RUN_BATTLE

def run_battle():
    '''
    Run a simulation of the current turn of the pokemon battle
    '''
    # TODO calculate the battle
    # TODO and store the results in the client message buffer
    for c, client in enumerate(connected_clients):
        # TODO process the message data
        pass

    # TODO get the pokemon data for the battle sim
    # and store the results back in the message_buffer
    state = TRANSFER_BATTLE

def transfer_battle():
    '''
    Transfer the buffered messages to the clients
    '''
    global connected_clients

    for c, client in enumerate(connected_clients):
        if not client.message_buffer:
            continue
        client.send_message(client.message_buffer)
        msg.client.recv_message()
        # Clear the message buffer upon confirmation of transfer
        if msg == 'confirm':
            connected_clients[c].message_buffer = None

    # If both clients have sent confirmation,
    # return a message and move to next state
    if all([client.message_buffer is None for client in connected_clients]):
        # start the battle simulation
        # If the result is gameover,
        # state = GAME_FINISH

        # otherwise, go back to polling for actions
        state = POLL_BATTLE

def game_finish():
    # TODO MVP+1/2 Handle the spectating screen as required here
    state = RESET

while True:
    state_actions = {
                     POLL_CLIENTS : poll_clients,
                     CLIENT_SETUP : client_setup,
                     POLL_BATTLE : poll_battle,
                     RUN_BATTLE : run_battle,
                     TRANSFER_BATTLE : transfer_battle,
                     GAME_FINISH : game_finish,
                     RESET : reset
                    }
    # Run the corresponding function for the current state
    state_actions[state]()
