from quokka import *

from client_states import *

CHANNEL = 14

radio.enable()
radio.config(channel=CHANNEL)

unaddressed_msg_queue = []

def setState(newState):
    global state

    prevState = state
    state = newState

last_print = running_time()
while True:
    state_actions = {
                    CALIBRATE : calibrate,
                    CONNECT_SERVER : connect_to_server,
                    CHOOSE_POKEMON : choose_pokemon,
                    CHOOSE_MOVE : choose_move,
                    READ_ZMOVE : read_zmove,
                    TRANSFER_BATTLE : transfer_battle,
                    DISPLAY_TURN : display_turn,
                    RESULT_SCREEN : result_screen,
                    RESET : machine.soft_reset
                    }

    if last_print+1000 < running_time():
        last_print = running_time()
        print(state, unaddressed_msg_queue, client.messages)

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

    setState(state_actions[state](unaddressed_msg_queue, client))
