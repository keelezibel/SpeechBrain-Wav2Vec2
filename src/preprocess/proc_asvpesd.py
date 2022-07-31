import os
import ffmpeg
from glob import glob

data_path = "data\\ASVP-ESD-Update\\Audio\\**\\*.wav"
files = glob(data_path)

dest = "data"
for f in files:
    filename = os.path.basename(f)
    file_parts = filename.split("-")

    if file_parts[1] == "02":
        continue

    label = file_parts[2]
    if label == "02":
        label = "Neutral"
    elif label == "03":
        label = "Happy"
    elif label == "04":
        label = "Sad"
    elif label == "05":
        label = "Angry"
    elif label == "06":
        label = "Fearful"
    elif label == "08":
        label = "Surprise"
    else:
        continue

    audio_filename = f.split(os.path.sep)[-1]
    dst_filepath = os.path.join(
        os.path.join(f"data\\{label}", "asvp-esp-2021_" + audio_filename)
    )
    out, _ = (
        ffmpeg.input(f)
        .output(dst_filepath, acodec="pcm_s16le", ac=1, ar="16k")
        .overwrite_output()
        .run(capture_stdout=False)
    )
