from microbit import *
import radio

SIDE_LENGTH = 2
PREFIX = "btn:"
OUT_PINS = [pin0, pin1]
IN_PINS = [pin3, pin4]

buttons = [[False] * SIDE_LENGTH for _ in range(SIDE_LENGTH)]

display.off()
#radio.on()
#radio.config(channel=6)

def init():
	# Set output pins to high initially
	for pin in OUT_PINS:
		pin.write_digital(1)
	# Set pullup on input pins
	for pin in IN_PINS:
		pin.set_pull(pin.PULL_UP)

while True:
	for i, out_pin in enumerate(OUT_PINS):
		# Iterate through each output pin
		out_pin.write_digital(0)

		row_states = []
		for j, in_pin in enumerate(IN_PINS):
			row_states.append(not in_pin.read_digital())

			# Check if any buttons have changed states
			if buttons[i][j] != row_states[j]:
				msg = PREFIX + str(i) + "," + str(j)
				#radio.send(msg)
				print(msg)

		buttons[i] = row_states

		# Set pin back to high after scanning
		out_pin.write_digital(1)