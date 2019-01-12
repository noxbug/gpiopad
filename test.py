from evdev import UInput, AbsInfo, ecodes as e
import keymap


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

ui = UInput(cap, name='gpio-pad', version=0x1)

# print device capabilities
print(ui)
print(ui.capabilities())

# move mouse cursor
ui.write(e.EV_ABS, e.ABS_X, 20)
ui.write(e.EV_ABS, e.ABS_Y, 20)
ui.syn()

print('Done!')