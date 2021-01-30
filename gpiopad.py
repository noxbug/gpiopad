import subprocess
import pigpio
import signal
import evdev
import time


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

# keymap configuration
keymap = {19: {'controller': 'LEFT', 'keyboard': 'LEFT'},
			26: {'controller': 'RIGHT', 'keyboard': 'RIGHT'},
			16: {'controller': 'A', 'keyboard': 'X'},
			20: {'controller': 'B', 'keyboard': 'Z'}}

# create uinput device
keys = []
for pin in keymap:
	keymap[pin]['ecode'] = eval('evdev.ecodes.KEY_' + keymap[pin]['keyboard'])
	keys.append(keymap[pin]['ecode'])

cap = {evdev.ecodes.EV_KEY: keys}
ui = evdev.UInput(cap, name='gpio-pad', version=0x1)

# callback function
# 0: falling edge
# 1: rising edge
# 2: watchdog timeout
inv = {0: 1, 1: 0}
def gpio_callback(pin, level, tick):
    ui.write(evdev.ecodes.EV_KEY, keymap[pin]['ecode'], inv[level])
    ui.syn()
    print('pin: ' + str(pin) + ' button: ' + keymap[pin]['keyboard'] + ' level: ' + str(inv[level]) + ' tick: ' + str(tick))

# gpio setup
deglitch_time = round(1/10*1000)  # 10 FPS
for pin in keymap:
	# set pull up resistor
	gpio.set_pull_up_down(pin, pigpio.PUD_UP)
	# configure as input
	gpio.set_mode(pin, pigpio.INPUT)
	# glitch filter
	gpio.set_glitch_filter(pin, deglitch_time)
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
