
import os
import subprocess
import boto3
from time import sleep

# AWS S3 Configuration
s3_bucket_name = 'caproject1'  # Replace with your S3 bucket name
s3_prefix = 'hls/'  # S3 prefix (directory in your bucket)

# Input RTMP stream URL
input_stream = "rtmp://<RTMP Server ip address>/live/my_stream"

# Base path for HLS segments
hls_base_path = "/tmp/hls"

# Resolution configurations for 240p, 360p, and 480p
resolutions = {
    "240p": {"scale": "426:240", "bitrate": "500k"},
    "360p": {"scale": "640:360", "bitrate": "800k"},
    "480p": {"scale": "854:480", "bitrate": "1200k"},
}

# Initialize S3 client
s3_client = boto3.client('s3')
os.makedirs(hls_base_path, exist_ok=True)

# Create subprocesses for each resolution
processes = []

for res, config in resolutions.items():
    res_path = os.path.join(hls_base_path, res)
    os.makedirs(res_path, exist_ok=True)  # Create directory for resolution

    hls_output = os.path.join(res_path, "index.m3u8")

    # FFmpeg command for transcoding and generating HLS
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", input_stream,
        "-vf", f"scale={config['scale']}",
        "-c:v", "libx264",
        "-b:v", config["bitrate"],
        "-g", "50",
        "-hls_time", "3",
        "-hls_playlist_type", "event",
        "-hls_flags", "delete_segments",
        "-hls_segment_filename", os.path.join(res_path, "segment_%03d.ts"),
        hls_output,
    ]

    # Start FFmpeg process
    print(f"Starting transcoding for {res} resolution...")
    proc = subprocess.Popen(ffmpeg_cmd)
    processes.append((proc, res, res_path, hls_output))  # Track process, resolution, and output path

# Upload segments to S3 as they are created
uploaded_segments = {"240p": set(), "360p": set(), "480p": set()}

while processes:
    for proc, res, res_path, hls_output in list(processes):
        # If process is done, remove it from the list
        if proc.poll() is not None:
            processes.remove((proc, res, res_path, hls_output))
            continue

        # Upload index.m3u8 if it exists
        if os.path.exists(hls_output):
            print(f"Uploading {hls_output} to S3 for {res} resolution...")
            s3_client.upload_file(hls_output, s3_bucket_name, s3_prefix + res + "/index.m3u8")

        # Upload .ts segment files for current resolution
        for segment in os.listdir(res_path):
            if segment.endswith('.ts') and segment not in uploaded_segments[res]:
                segment_path = os.path.join(res_path, segment)
                print(f"Uploading {segment_path} to S3 for {res} resolution...")
                s3_client.upload_file(segment_path, s3_bucket_name, s3_prefix + res + "/" + segment)
                
                # Add the segment to the uploaded set
                uploaded_segments[res].add(segment)
                
                # Clean up local segment file after upload
                print(f"Cleaning up {segment_path} for {res} resolution...")
                os.remove(segment_path)

    sleep(2)  # Sleep for 2 seconds to prevent too frequent upload checks

# Wait for all processes to finish and clean up
for proc, res, res_path, hls_output in processes:
    proc.wait()

# Clean up local files after processing
for res in resolutions:
    res_path = os.path.join(hls_base_path, res)
    hls_output = os.path.join(res_path, "index.m3u8")
    if os.path.exists(hls_output):
        print(f"Removing local {hls_output} file for {res} resolution...")
        os.remove(hls_output)

# Clean up the S3 bucket (delete all .ts files and index.m3u8)
s3_objects = s3_client.list_objects_v2(Bucket=s3_bucket_name, Prefix=s3_prefix)
if 'Contents' in s3_objects:
    for obj in s3_objects['Contents']:
        print(f"Deleting {obj['Key']} from S3...")
        s3_client.delete_object(Bucket=s3_bucket_name, Key=obj['Key'])

print("Transcoding completed for all resolutions. Cleanup completed.")