import math
import ffmpeg
import os
from django.conf import settings

def split_video(video_path, split_minutes):
    probe = ffmpeg.probe(video_path)
    duration = float(probe['format']['duration'])
    total_splits = math.ceil(duration / (split_minutes * 60))
    output_files = []

    for i in range(total_splits):
        start_time = i * split_minutes * 60
        output_file = os.path.join(
            settings.MEDIA_ROOT, f"splits/part_{i+1}.mp4"
        )
        ffmpeg.input(video_path, ss=start_time, t=split_minutes * 60).output(output_file).run()
        output_files.append(output_file)

    return output_files