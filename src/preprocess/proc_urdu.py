import os
import ffmpeg
from glob import glob

data_path = "data\\URDU\\**\\*.wav"
files = glob(data_path)

dest = "data"
for f in files:
    filename = os.path.basename(f)
    label = f.split(os.path.sep)[-2]

    audio_filename = f.split(os.path.sep)[-1]
    dst_filepath = os.path.join(
        os.path.join(f"data\\{label}", "urdu2020_" + audio_filename)
    )
    out, _ = (
        ffmpeg.input(f)
        .output(dst_filepath, acodec="pcm_s16le", ac=1, ar="16k")
        .overwrite_output()
        .run(capture_stdout=False)
    )
