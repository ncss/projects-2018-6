from quokka import *

from client_states import *

CHANNEL = 8

radio.enable()
radio.config(channel=CHANNEL)

def setState(newState):
    global state

    prevState = state
    state = newState

while True:
    state_actions = {
                    CALIBRATE : calibrate,
                    CONNECT_SERVER : connect_to_server,
                    CHOOSE_POKEMON : choose_pokemon,
                    CHOOSE_MOVE: choose_move,
                    READ_ZMOVE = read_zmove,
                    TRANSFER_BATTLE : transfer_battle,
                    DISPLAY_TURN : display_turn,
                    RESULT_SCREEN : result_screen,
                    RESET : machine.soft_reset
                    }

    setState(state_actions[state]())
