#!/usr/bin/python
# -*- coding: utf-8 -*-

# convert.py
# 2016 July jhobbs

import os
import argparse

from pydub import AudioSegment

remove_mp3 = True # if we want to eliminate the mp3 files.
formats_to_convert = ['.mp3']
dir_ = "./sounds/mp3/"

for (dirpath, dirnames, filenames) in os.walk(dir_):
    for filename in filenames:
        if filename.endswith(tuple(formats_to_convert)):

            filepath = dirpath + '/' + filename
            (path, file_extension) = os.path.splitext(filepath)
            file_extension_final = file_extension.replace('.', '')
            try:
                track = AudioSegment.from_file(filepath,
                        file_extension_final)
                wav_filename = filename.replace(file_extension_final, 'wav')
                wav_path = dirpath + '/' + wav_filename
                print 'CONVERTING: ' + str(filepath)
                file_handle = track.export(wav_path, format='wav')
                if(remove_mp3):
                    os.remove(filepath)
            except:
                print "ERROR CONVERTING " + str(filepath)