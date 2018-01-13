from quokka import *
from BattleStuff import *

# 8 is client1 dedicated, 10 is client2 dedicated, 14 is everything else
# Let's make everything run on channel 14
channel = 14

radio.config(channel=14)
radio.enable()

unaddressed_msg_queue = []
connected_clients = []

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
    def __init__(self, client_id):
        self.id = client_id
        self.pokemon = []
        self.current_pokemon = 0
        self.radio_buffer = []
        self.message_buffer = ""

    def send_message(self, message):
        if len(message) > 250:
            raise Exception('The message is too long and we need to rewrite this code. :\'(')
        radio.send("{}:{}".format(self.id, message))
        sleep(50)

    def recv_message(self):
        if len(self.radio_buffer) > 0:
            return self.radio_buffer.pop(0)
        return None

    def handle_message(self, msg):
        client_id, msg = msg.split(":", 1)
        try:
            client_id = int(client_id)
        except ValueError:
            return False
        if client_id == self.id:
            print("Client {} handled {}".format(self.id, msg))
            self.radio_buffer.append(msg)
            return True
        return False

def poll_clients():
    '''
    Poll for incoming connections from clients
    '''
    global channels
    global connected_clients
    global state

    # Listen for connecting clients
    if len(unaddressed_msg_queue) > 0:
        msg = unaddressed_msg_queue.pop(0)
        # If a client is trying to connect
        if msg == "connect":
            client_id = len(connected_clients)
            radio.send("confirm:{}".format(client_id))
            sleep(50) # Give the client time to receive the message
            connected_clients.append(Client(client_id))

    # Once two clients have connected, start the game with the first two who connected
    if len(connected_clients) >= 2:
        # start the game
        state = CLIENT_SETUP
        radio.send("server_ready")

def client_setup():
    '''
    Poll for setup data from the clients
    '''
    global state
    global connected_clients
    # If all clients have connected and confirmed their pokemon lists
    # we move on to BATTLE
    if all([bool(client.pokemon) for client in connected_clients]):
        sleep(50) # wait for confirm to be received
        state = POLL_BATTLE
        radio.send("start_battle")
        sleep(50)
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
    global state
    global connected_clients

    for c, client in enumerate(connected_clients):
        msg = client.recv_message()
        if msg is None:
            continue
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
    global state
    pokemon = []

    # process the message data
    for c, client in enumerate(connected_clients):
        move, id = client.message_buffer.split('|')
        move = int(move)
        id = int(id)
        pokemon.append(get_pokemon_by_id(id))
        pokemon[-1].moveIndex = move

    # calculate the battle
    pokemon, messages = Battle_calc(*pokemon)

    # and store the results in the client message buffer
    for c, client in enumerate(connected_clients):
        poke = pokemon[c]
        if messages[-1] == 'game_over':
            if all([p.fainted for p in client.pokemon]):
                messages[-1] += '$You lost!'
            else:
                messages[-1] += '$You won!'
        connected_clients[c].message_buffer = '{}|{}'.format(poke.hp, '|'.join(messages))

    # get the pokemon data for the battle sim
    # and store the results back in the message_buffer
    state = TRANSFER_BATTLE

def transfer_battle():
    '''
    Transfer the buffered messages to the clients
    '''
    global state
    global connected_clients

    game_over = False

    for c, client in enumerate(connected_clients):
        if not client.message_buffer:
            continue
        # Check for game over
        if not game_over and 'game_over' in client.message_buffer:
            game_over = True

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
        if game_over:
            state = GAME_FINISH
        # otherwise, go back to polling for actions
        else:
            state = POLL_BATTLE

def game_finish():
    global state
    # TODO MVP+1/2 Handle the spectating screen as required here
    state = RESET

last_print = running_time()
while True:
    state_actions = {
                     POLL_CLIENTS : poll_clients,
                     CLIENT_SETUP : client_setup,
                     POLL_BATTLE : poll_battle,
                     RUN_BATTLE : run_battle,
                     TRANSFER_BATTLE : transfer_battle,
                     GAME_FINISH : game_finish,
                     RESET : machine.soft_reset
                    }

    if last_print+1000 < running_time():
        last_print = running_time()
        print(state, unaddressed_msg_queue, connected_clients)

    # Check if we have received a message and assign it to a client
    msg = radio.receive()
    if msg is not None:
        if ":" in msg:
            for client in connected_clients:
                if client.handle_message(msg):
                    break
            else:
                unaddressed_msg_queue.append(message)
        else:
            unaddressed_msg_queue.append(msg)

    # Run the corresponding function for the current state
    state_actions[state]()
