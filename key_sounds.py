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
pygame.mixer.init(freq, m_size, channels, m_buffer)

# init sounds from config
for s in sounds:
    s["sound"] = pygame.mixer.Sound(s["file"])
    s["channel"] = pygame.mixer.Channel(int(s["panel"]) - 1)

print("Sampler Ready.")

def get_sounds_by_key(sounds, key_):
    return [x for x in sounds if x["tecla"] == key_]

try:
    while 1:
        try:
            c = sys.stdin.read(1)
            sound = get_sounds_by_key(sounds, c)
            if(c != ""):
                print("KEY: ", c)
            for s in sound:
                print("Playing sound", s)
                s["channel"].play(s["sound"])
            sleep(.01)
        except IOError: 
          pass
finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
