
import wave
import json
from yt_dlp import YoutubeDL, utils
import random 
import os
import subprocess
from datetime import timedelta


from vosk import Model, KaldiRecognizer, SetLogLevel



mc_url = "https://www.youtube.com/watch?v=n_Dv4JMiwK8"

def filename_hook(d):
    # print(d)
    if d["status"] == "finished":
        # print(d)

        os.rename(d["filename"], f"videos/outfile.mp4")


    


model_path = "vosk-model-en-us-0.42-gigaspeech"

audio_file = "test.wav"

model = Model(model_path)

wf = wave.open(audio_file, "rb")
rec = KaldiRecognizer(model,wf.getframerate())
rec.SetWords(True)

results = []
while True:
    data = wf.readframes(4000)
    if(len(data)==0):
        break
    if rec.AcceptWaveform(data):
        print('reading')
        part_result = json.loads(rec.Result())
        results.extend(part_result["result"])
#part_result =  json.loads(rec.FinalResult())
#results.append(part_result)
# print(results)


with open("subtitles.srt", "w") as f:
    f.write("")
with open("subtitles.srt", "a") as subt:
    print(results)

    for i,word in enumerate(results):
        print("WORD: ", word)
        start = str(timedelta(seconds=word["start"]))
        end = str(timedelta(seconds=word["end"]))
        txt = word["word"]
        stri = f"{i+1}\n{start} --> {end}\n\n{txt}\n\n"
        print(stri)
        subt.write(stri)



opts = {
    "default_search":"ytsearch",
}

with YoutubeDL(opts) as infograb:
    info = infograb.extract_info(mc_url, download=False)
    print(info["duration"])
    end = results[-1]["end"]
    start = random.uniform(0, info["duration"]- end)
    
    ydl_opts = {
        "paths": {"home": "videos"},
        "format": "mp4",
        "concurrent_fragment_downloads":5,
        "progress_hooks": [filename_hook],
        "default_search":"ytsearch",
        "download_ranges":utils.download_range_func(None, [(start, end+start)]),  
        "force_keyframes_at_cuts": True, 
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(mc_url)
        
        ffmpeg_cmd = ['ffmpeg', '-i','videos/outfile.mp4', '-vf', 'subtitles=subtitles.srt', 'videos/outfilesubtitled.mp4']
        subprocess.run(ffmpeg_cmd)
            
