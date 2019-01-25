import pigpio
import time


RS = 13
E = 21
DB = [20, 26, 16, 19]
DISPLAY_CONTROL = 0x00

gpio = pigpio.pi('192.168.1.10', 8888)

gpio.set_mode(RS, pigpio.OUTPUT)
gpio.set_mode(E, pigpio.OUTPUT)
for dbx in DB:
    gpio.set_mode(dbx, pigpio.OUTPUT)


def write(data, rs=1):
    # Register select
    gpio.write(RS, rs)
    # Write MSB
    gpio.write(E, 1)
    gpio.write(DB[3], (data >> 7) & 1)
    gpio.write(DB[2], (data >> 6) & 1)
    gpio.write(DB[1], (data >> 5) & 1)
    gpio.write(DB[0], (data >> 4) & 1)
    gpio.write(E, 0)
    # Write LSB
    gpio.write(E, 1)
    gpio.write(DB[3], (data >> 3) & 1)
    gpio.write(DB[2], (data >> 2) & 1)
    gpio.write(DB[1], (data >> 1) & 1)
    gpio.write(DB[0], (data >> 0) & 1)
    gpio.write(E, 0)


def clear_display():
        """
        Clear entire display and sets DDRAM address 0 in address counter.
        :return:
        """
        write(1, 0)


def return_home():
    """
    Sets DDRAM address 0 in address counter.
    Also returns display from being shifted to original position.
    DDRAM contents remain unchanged.
    :return:
    """
    write(2, 0)
    time.sleep(2e-3)


def display(boolean):
    global DISPLAY_CONTROL
    if boolean:
        DISPLAY_CONTROL |= (boolean << 2)
    else:
        DISPLAY_CONTROL &= (~(boolean << 2) & 0xFF)
    return DISPLAY_CONTROL


write(240, 1)
print(bin(display(True)))

