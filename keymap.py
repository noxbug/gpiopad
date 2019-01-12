from evdev import ecodes as e
import json
import os


def gen_path():
    script_path = os.path.abspath(__file__)
    script_dir = os.path.split(script_path)[0]
    keymap_path = os.path.join(script_dir, 'keymap.json')
    return keymap_path


def parse(keymap_str_index):
    keymap = {}
    for key in keymap_str_index:
        int_key = int(key)
        keymap[int_key] = keymap_str_index[key]
        keymap[int_key]['ecode'] = eval('e.KEY_' + keymap[int_key]['keyboard'])
    return keymap


def default():
    keymap = {'13': {'controller': 'UP', 'keyboard': 'UP'},
              '19': {'controller': 'DOWN', 'keyboard': 'DOWN'},
              '6': {'controller': 'LEFT', 'keyboard': 'LEFT'},
              '26': {'controller': 'RIGHT', 'keyboard': 'RIGHT'},
              '12': {'controller': 'A', 'keyboard': 'X'},
              '16': {'controller': 'B', 'keyboard': 'Z'},
              '20': {'controller': 'X', 'keyboard': 'S'},
              '21': {'controller': 'Y', 'keyboard': 'A'},
              '23': {'controller': 'SELECT', 'keyboard': 'SPACE'},
              '22': {'controller': 'START', 'keyboard': 'ENTER'},
              '27': {'controller': 'L1', 'keyboard': 'Q'},
              '17': {'controller': 'R1', 'keyboard': 'W'}}
    keymap = parse(keymap)
    return keymap


def debug():
    keymap = {'27': {'controller': 'LEFT', 'keyboard': 'LEFT'},
              '23': {'controller': 'RIGHT', 'keyboard': 'RIGHT'},
              '22': {'controller': 'A', 'keyboard': 'X'},
              '17': {'controller': 'B', 'keyboard': 'Z'}}
    keymap = parse(keymap)
    return keymap


def save(keymap):
    keymap_path = gen_path()
    with open(keymap_path, 'w') as fid:
        json.dump(keymap, fid, indent=4, sort_keys=True, ensure_ascii=False)


def load():
    keymap_path = gen_path()
    with open(keymap_path, 'r', encoding='iso-8859-1') as fid:
        keymap = json.load(fid)
    keymap = parse(keymap)
    return keymap
