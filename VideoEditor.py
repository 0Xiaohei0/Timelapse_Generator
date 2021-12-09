from genericpath import isfile
from moviepy.editor import *
from os import listdir
import os
from datetime import datetime
import configparser

# Config
mypath="D:/video/drawing"
fileExtension=".mkv"
speed=4

os.chdir(os.path.dirname(os.path.realpath(__file__)))
if isfile("config.txt"):
    parser = configparser.ConfigParser()
    parser.read("config.txt")
    mypath=parser.get("config", "path")
    fileExtension=parser.get("config", "fileExtension")
    speed=int(parser.get("config", "speed"))

# Find files
os.chdir(mypath)
print("Searching for " + fileExtension + " in " + os.getcwd())
filtered = [f for f in listdir(mypath) if f.endswith(fileExtension)]
if len(filtered) != 0:
    print("Files found: ")
    print('\n'.join(filtered))
else:
    print("No files found.")
tmpFileNames = []
tmpClips = []

# User input confirm
r=input("Confirm (Y/N)")
if r != "Y":
    quit()

# Process files
print("Speeding up to " + str(speed) + "x")
for idx,file in enumerate(filtered): # speed up clips
    clip = VideoFileClip(file)
    clip_speed = clip.fx(vfx.speedx, speed)
    tempFileName = "tmp" + str(idx) + ".mp4"
    clip_speed.write_videofile(tempFileName)
    tmpFileNames.append(tempFileName)
    tmpClips.append(VideoFileClip(tempFileName))
final_clip = concatenate_videoclips(tmpClips) # concatenate 
final_clip.write_videofile("Final render " + datetime.today().strftime("%m-%d-%Y %H-%M-%S") + ".mp4" )
for file in tmpFileNames: # delete
    os.remove(file)
print("Finished!")