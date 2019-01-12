from evdev import UInput, AbsInfo, ecodes as e
import subprocess
import signal
import time
import pigpio
import keymap


try:
    # check if pigpio daemon running
    pid = subprocess.check_output(['pgrep', 'pigpiod']).decode('ascii')
    print(pid)
except:
    # start if needed
    print('Starting pigpio daemon...')
    subprocess.call(['sudo', 'pigpiod'])
    # wait before creating pigpio instance
    time.sleep(1)

# create pigpio instance
gpio = pigpio.pi()

# load keymap configuration
gpio_keymap = keymap.debug()

# set device capabilities
cap_key = []
for key in gpio_keymap:
    cap_key.append(gpio_keymap[key]['ecode'])

cap = {
    e.EV_KEY: cap_key,
    e.EV_ABS: [
        (e.ABS_X, AbsInfo(0, 0, 255, 0, 0, 0)),
        (e.ABS_Y, AbsInfo(0, 0, 255, 0, 0, 0))]}

# create uinput device
ui = UInput(cap, name='gpio-pad', version=0x1)

# callback function
# 0: falling edge
# 1: rising edge
# 2: watchdog timeout
level_conversion = {0: 1, 1: 0}
def gpio_callback(pin, level, tick):
    ui.write(e.EV_KEY, gpio_keymap[pin]['ecode'], level_conversion[level])
    ui.syn()
    print('pin: ' + str(pin) + ' button: ' + gpio_keymap[pin]['keyboard'] + ' level: ' + str(level_conversion[level]) + ' tick: ' + str(tick))


# setup gpio
glitch_filter_time = round(1/10*1000)  # 10 FPS
for pin in gpio_keymap:
    # set pull up resistor
    gpio.set_pull_up_down(pin, pigpio.PUD_UP)
    # configure as input
    gpio.set_mode(pin, pigpio.INPUT)
    # glitch filter
    gpio.set_glitch_filter(pin, glitch_filter_time)
    # callback
    gpio.callback(pin, pigpio.EITHER_EDGE, gpio_callback)

# main loop
try:
    print('Press Ctrl+C to exit')
    signal.pause()
except KeyboardInterrupt:
    # clean up
    gpio.stop()
    subprocess.call(['sudo', 'pkill', 'pigpiod'])
    ui.close()
