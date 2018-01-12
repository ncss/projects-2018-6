from microbit import *
def if_shaking_left_right():
    run_start_ms = running_time()
    clock = running_time() - run_start_ms
    thresh = 1000
    shaka_time = 3000
    shaka_flag = False
    while clock < shaka_time:
        clock = running_time() - run_start_ms
        if accelerometer.is_gesture("left") or accelerometer.is_gesture("right") and clock < thresh:
            display.show(Image.HEART)
            sleep(1000)
            shaka_flag = True
            break
        else:
            display.clear()
            shaka_flag = False
    
     display.clear()
     if shaka_flag:
         sleep(shaka_time -  thresh)
         return True
     else:
         sleep(shaka_time - thresh)
         return False
