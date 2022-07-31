import os
import ffmpeg
from glob import glob

data_path = "data\\Mexican Emotional Speech Database (MESD)\\*.wav"
files = glob(data_path)

dest = "data"
for f in files:
    filename = os.path.basename(f)
    label = filename.split("_")[0]
    if label == "Anger":
        label = "Angry"
    elif label == "Fear":
        label = "Fearful"
    elif label == "Happiness":
        label = "Happy"
    elif label == "Sadness":
        label = "Sad"
    elif label == "Disgust":
        continue
    audio_filename = f.split(os.path.sep)[-1]
    dst_filepath = os.path.join(
        os.path.join(f"data\\{label}", "mesd2022_" + audio_filename)
    )
    out, _ = (
        ffmpeg.input(f)
        .output(dst_filepath, acodec="pcm_s16le", ac=1, ar="16k")
        .overwrite_output()
        .run(capture_stdout=False)
    )
