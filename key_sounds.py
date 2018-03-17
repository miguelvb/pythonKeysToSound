# PLAY SOUNDS WHEN KEYS ARE PRESSED #####
#########################################

import pygame.mixer
from time import sleep
from sys import exit
import json
from pynput import keyboard

released = True
audio_sound = False

mixer_config_file = 'mixer_config.json'
config_file = 'files_config.json'

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
    print "Loading sound: " , s["name"]
    #s["sound"] = pygame.mixer.Sound(s["file"])
    s["channel"] = get_channel(s)

print("....... Samples Loaded ........")

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

def on_press(key):
    global time_pressed
    global released
    global audio_sound
    try:
        kk = key.char
        if released:
            print " -- Pressed "
            released = False
            sound = get_sounds_by_key(sounds, kk)
            if(sound):
                print("Playing sound", sound["name"])
                audio_sound = pygame.mixer.Sound(sound["file"])
                sound["channel"].play(audio_sound)
        else:
            pass

    except AttributeError:
        print "error--- "
        pass

def on_release(key):
    global released
    released = True
    try:
        print key, " Released "
        sound = get_sounds_by_key(sounds, key)
        if(sound):
            print("Stopping sound", sound["name"])
            sound["channel"].stop()
    except AttributeError:
        pass
    if key == keyboard.Key.esc:
        # Stop listener
        return False


def get_current_key_input():
    with keyboard.Listener(
        on_press=on_press, 
        on_release=on_release
        ) as listener:
        listener.join()


get_current_key_input()
