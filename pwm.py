import pigpio


gpio = pigpio.pi('192.168.1.10', 8888)

gpio.set_mode(18, pigpio.OUTPUT)
gpio.set_PWM_frequency(18, 8000)
gpio.set_PWM_dutycycle(18, 128)