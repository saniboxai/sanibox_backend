import os
import math
import subprocess
import cloudinary
import cloudinary.uploader
import cloudinary.api

# -----------------------------
# 🧩 CONFIGURE CLOUDINARY HERE
# -----------------------------
cloudinary.config( 
    cloud_name = "dc7kcreln", 
    api_key = 459418188258399, 
    api_secret = "jsLkoOrD3LllyHlSH1cMLxyDvOw",
    secure = True
)


def get_video_duration(video_path):
    """Get total duration of video in seconds using ffprobe"""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_path
    ]
    result = subprocess.check_output(cmd).strip()
    return float(result)


def split_video(video_path, split_duration, upload_to_cloud=True):
    """Split a video file and upload parts to Cloudinary"""
    output_dir = "split_parts"
    os.makedirs(output_dir, exist_ok=True)

    total_duration = get_video_duration(video_path)
    total_parts = math.ceil(total_duration / split_duration)
    print(f"\n🎬 Total Duration: {total_duration:.2f} seconds")
    print(f"⏱ Splitting every {split_duration} seconds ({total_parts} parts total)\n")

    uploaded_urls = []

    for i in range(total_parts):
        start_time = i * split_duration
        output_file = os.path.join(output_dir, f"split_part_{i+1}.mp4")

        # Split using FFmpeg
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-ss", str(start_time),
            "-t", str(split_duration),
            "-c", "copy",
            output_file
        ]
        subprocess.run(cmd, check=True)

        # Upload to Cloudinary
        if upload_to_cloud:
            print(f"⬆️  Uploading part {i+1}/{total_parts} to Cloudinary...")
            upload_result = cloudinary.uploader.upload(output_file, resource_type="video")
            uploaded_urls.append(upload_result['secure_url'])
            os.remove(output_file)  # remove local split file
        else:
            uploaded_urls.append(os.path.abspath(output_file))

    print("\n✅ Splitting complete!")
    print(f"Total parts: {total_parts}")

    return uploaded_urls


def main():
    print("=== Video Splitter Script ===")
    video_path = input("Enter video file path: ").strip()

    if not os.path.exists(video_path):
        print("❌ Error: File not found.")
        return

    duration = input("Enter duration (in seconds) for each split: ").strip()

    try:
        duration = int(duration)
        urls = split_video(video_path, duration)
        print("\n🌐 Uploaded video parts:")
        for idx, url in enumerate(urls, start=1):
            print(f"Part {idx}: {url}")
    except ValueError:
        print("❌ Invalid duration. Please enter an integer value.")


if __name__ == "__main__":
    main()
