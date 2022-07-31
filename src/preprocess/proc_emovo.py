import os
import ffmpeg
from glob import glob

data_path = "data\\EMOVO\\**\\*.wav"
files = glob(data_path)

dest = "data"
for f in files:
    filename = os.path.basename(f)
    file_parts = filename.split("-")

    label = file_parts[0]
    if label == "gio":
        label = "Happy"
    elif label == "pau":
        label = "Fearful"
    elif label == "rab":
        label = "Angry"
    elif label == "sor":
        label = "Surprise"
    elif label == "tri":
        label = "Sad"
    elif label == "neu":
        label = "Neutral"
    else:
        continue

    audio_filename = f.split(os.path.sep)[-1]
    dst_filepath = os.path.join(
        os.path.join(f"data\\{label}", "emovo2014_" + audio_filename)
    )

    out, _ = (
        ffmpeg.input(f)
        .output(dst_filepath, acodec="pcm_s16le", ac=1, ar="16k")
        .overwrite_output()
        .run(capture_stdout=False)
    )
