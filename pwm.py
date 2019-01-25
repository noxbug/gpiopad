import pigpio


pin = 18
gpio = pigpio.pi()
gpio.set_mode(pin, pigpio.OUTPUT)
gpio.set_PWM_frequency(pin, 8000)
gpio.set_PWM_dutycycle(pin, 128)  # FS = 255