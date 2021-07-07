from typing import Any
from pydub import AudioSegment
import os, datetime


recordings = {}

## Get list of all .wav files in folder
for file in os.listdir("./"):
    if file.endswith(".wav"):
        name = file.split("_")[0]
        # Group files by name
        records_for_name = []
        if(name in recordings.keys()):
            records_for_name = recordings[name]
        records_for_name.append(file)
        recordings[name] = records_for_name

print("Found {} different peoples audio".format(len(recordings)))

## Break groups into intervals

# Sort each list
for name in recordings.keys():
    files = recordings[name]
    files.sort()
    recordings[name] = files



# Split list by times
for name in recordings.keys():
    for i in range(len(recordings[name])):
        prev = None
        if i >= 1:
            prev = recordings[name][i-1]
        curr = recordings[name][i]

        # If there is nothing beforehand
        if prev == None:
            # Start a new recording
            pass
        # If more than 30 minutes have passed
        elif int(curr.split("_")[2].split(".")[0]) - int(prev.split("_")[2].split(".")[0]) > 1800:
            # Start a new recording
            pass
        else:
            # Keep recording
            pass

# epoch_time = int(file.split("_")[2].split('.')[0])
# datetime_time = datetime.datetime.fromtimestamp(epoch_time)

# Check if interval already exists on S3

# If not upload to S3


# Audio Merge Example
# sound1 = AudioSegment.from_wav("/path/to/file1.wav")
# sound2 = AudioSegment.from_wav("/path/to/file2.wav")

# combined_sounds = sound1 + sound2
# combined_sounds.export("/output/path.wav", format="wav")