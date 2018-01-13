from microbit import *
import radio
radio.on()
radio.config(channel=7)
right_1 = 0
left_1 = 0
while True:
    msg = radio.receive()
    while pin1.read_digital() == 0:
        if (running_time() - left_1) > 300:
            pin16.write_digital(0)
        pin12.write_digital(1)
        pin0.write_digital(1)
        sleep(100)
        pin12.write_digital(0)
        pin0.write_digital(0)
    while pin2.read_digital() == 0:
        if (running_time() - right_1) > 300:
            pin12.write_digital(0)
        pin16.write_digital(1)
        pin8.write_digital(1)
        sleep(100)
        pin16.write_digital(0)
        pin8.write_digital(0)
    if msg == 'Left_1':
        pin16.write_digital(1)
        left_1 = running_time()
    if msg == 'Right_1':
        pin12.write_digital(1) 
        right_1 = running_time()
    if (running_time() - right_1) > 300:
        pin12.write_digital(0)
    if (running_time() - left_1) > 300:
        pin16.write_digital(0)
 