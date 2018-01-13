from quokka import *

from client_states import *

CHANNEL = 14

radio.enable()
radio.config(channel=CHANNEL, power=7)

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

    radio_loop()

    setState(state_actions[state](unaddressed_msg_queue, client))
