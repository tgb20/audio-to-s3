import botocore, boto3
from pydub import AudioSegment
import os, datetime


SEP_INTERVAL = 1800

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

exports = []

exportIndex = -1

for name in recordings.keys():
    for i in range(len(recordings[name])):
        prev = None
        if i >= 1:
            prev = recordings[name][i-1]
        curr = recordings[name][i]

        # If there is nothing beforehand
        if prev == None:
            # Start a new file
            exportIndex += 1
            exports.append([recordings[name][i]])
        # If more than 30 minutes have passed
        elif int(curr.split("_")[2].split(".")[0]) - int(prev.split("_")[2].split(".")[0]) > SEP_INTERVAL:
            # Start a new file
            exportIndex += 1
            exports.append([recordings[name][i]])
        else:
            # Keep same file
            exports[exportIndex].append(recordings[name][i])


for export in exports:
    firstFile = export[0]
    lastFile = export[len(export) - 1]
    name = firstFile.split("_")[0]

    firstTime = int(firstFile.split("_")[2].split(".")[0])
    lastTime = int(lastFile.split("_")[2].split(".")[0])

    firstDate = str(datetime.datetime.fromtimestamp(firstTime))
    lastDate = str(datetime.datetime.fromtimestamp(lastTime))

    recordingName = name + "_" + firstDate + "-" + lastDate + ".wav"
    
    audioTrack = None
    for track in export:
        sound = AudioSegment.from_wav(track)
        if audioTrack == None:
            audioTrack = sound
        else:
            audioTrack += sound
    audioTrack.export("./exports/" + recordingName, format="wav")
    print("Exported audio for " + name + " that was " + str(len(audioTrack)/1000/60) + " minutes long")

# Connect to S3
s3 = boto3.resource('s3')

# Upload to S3
for file in os.listdir('./exports'):
    try:
        s3.Object('galeforce-audio', file).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            # File does not exist on S3 yet
            print('Uploading audio ' + file)
            data = open('./exports/' + file, 'rb')
            s3.Bucket('galeforce-audio').put_object(Key=file, Body=data)
            print('Uploaded audio ' + file)
        else:
            print('Error when connecting to S3')
            raise
    else:
        # File is already on S3
        print(file + ' already uploaded, skipping')
