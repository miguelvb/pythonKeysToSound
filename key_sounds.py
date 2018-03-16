# PLAY SOUNDS WHEN KEYS ARE PRESSED #####
#########################################

import termios, fcntl, sys, os
import pygame.mixer
from time import sleep
from sys import exit
import json

mixer_config_file = 'mixer_config.json'
config_file = 'files_config.json'


## Keys config
fd = sys.stdin.fileno()
oldterm = termios.tcgetattr(fd)
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
termios.tcsetattr(fd, termios.TCSANOW, newattr)
oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

## json config read

with open(config_file) as json_data:
    sounds = json.load(json_data)

with open(mixer_config_file) as json_data:
    mixer_config = json.load(json_data)


freq = mixer_config["mixer"]["frequency"]
channels = mixer_config["mixer"]["channels"]
m_size = mixer_config["mixer"]["size"]
m_buffer  = mixer_config["mixer"]["buffer"]

## pygame sounds init 
pygame.mixer.init(freq, m_size, 2, m_buffer)
pygame.mixer.set_num_channels(channels)

def get_channel(s):
    return pygame.mixer.Channel(int(s["track"]) - 1)

print("Getting Samples Ready......")

# init sounds from config
for s in sounds:
    s["sound"] = pygame.mixer.Sound(s["file"])
    s["channel"] = get_channel(s)

print("Sampler Ready.")

# dirty hard coded : 
musicas_panel = {
    "1": {"total": 5, "last_played": 4},
    "2": {"total": 5, "last_played": 4},
    "3": {"total": 7, "last_played": 6},
    "4": {"total": 6, "last_played": 5},
    "5": {"total": 5, "last_played": 4},
    "6": {"total": 6, "last_played": 5},
    "7": {"total": 7, "last_played": 6},
    "8": {"total": 8, "last_played": 7}
}

def get_sounds_by_key(sounds, key_):
    selection = [x for x in sounds if x["tecla"] == key_]
    print "selection", [ {"name": s["name"], "track": s["track"], "uid": s["uid"]} for s in selection]
    if(selection):
        s0 = selection[0] # si son musicas
        if(s0["ismusic"]):
            print "MUSIC", len(selection), s0["panel"]
            # ver en cual se quedo:
            last = musicas_panel[s0["panel"]]["last_played"]
            total = len(selection)
            musicas_panel[s0["panel"]]["total"] = total #adjust total
            next_ = last + 1
            if(next_ >= total):
                next_ = 0
            print last, total, next_
            musicas_panel[s0["panel"]]["last_played"] = next_
            return selection[next_]
        else:
            return selection[0] # no es musicas
    else:
        return []



### MAIN PROGRAM ####
try:
    while 1:
        try:
            c = sys.stdin.read(1)
            sound = get_sounds_by_key(sounds, c)
            if(c != ""):
                print("KEY: ", c)
            if(sound):
                print("Playing sound", sound["name"])
                sound["channel"].play(sound["sound"])
            sleep(.01)
        except IOError: 
          pass
finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
