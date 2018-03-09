# PLAY SOUNDS WHEN KEYS ARE PRESSED #####
#########################################

import termios, fcntl, sys, os
import pygame.mixer
from time import sleep
from sys import exit
import json

## default vaues and constants

config_file = 'config.json'

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
    config = json.load(json_data)
    print("json configuration")
    print(json.dumps(config, sort_keys=True, indent=2))

freq = config["mixer"]["frequency"]
channels = config["mixer"]["channels"]
m_size = config["mixer"]["size"]
m_buffer  = config["mixer"]["buffer"] 
sounds = config["sounds"] 

## pygame sounds init 
pygame.mixer.init(freq, m_size, channels, m_buffer)

# init sounds from config
for s in sounds:
    s["sound"] = pygame.mixer.Sound(s["path"])
    s["channel"] = pygame.mixer.Channel(s["channel_num"])

#test sound:

print("Sampler Ready.")

def get_sounds_by_key(sounds, key_):
    return [x  for x in sounds if x["key"] == key_]

try:
    while 1:
        try:
            c = sys.stdin.read(1)
            sound = get_sounds_by_key(sounds, c)
            for s in sound:
                 print("Playing sound", s)
                 s["channel"].play(s["sound"])
            sleep(.01)
        except IOError: 
          pass
finally:
   termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
   fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
