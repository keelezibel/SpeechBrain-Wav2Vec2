import os
import json
import pandas as pd
import ffmpeg

metadata_path = "data\\tigtag_brainhack2022_emotions\\manifest.json"
df = pd.read_json(metadata_path, lines=True)
print(df.head(5))

dest = "data"
for _, row in df.iterrows():
    label, audio = row["class"], row["audio_filepath"]
    audio_parts = audio.split("/")
    audio = os.path.sep.join(audio_parts)
    src_filepath = os.path.join("data\\tigtag_brainhack2022_emotions", audio)
    label = label[0].upper() + label[1:]
    dst_filepath = os.path.join(os.path.join(f"data\\{label}", audio_parts[-1]))
    print(src_filepath, dst_filepath)
    out, _ = (
        ffmpeg.input(src_filepath)
        .output(dst_filepath, acodec="pcm_s16le", ac=1, ar="16k")
        .overwrite_output()
        .run(capture_stdout=False)
    )
