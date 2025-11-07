# FFmpeg will be used to process the audio and images to connect it tg
import os
import subprocess

def stitch_video(image_paths, audio_path, timings, job_id):
    """
    Stitch images and audio together into a video using FFmpeg
    Returns the path to the final video file
    """
    
    # creates a temp directory for this job if it doesn't exist
    temp_dir = f'/tmp/keyframe_job_{job_id}'
    os.makedirs(temp_dir, exist_ok=True)
    
    # outputs video path
    output_path = os.path.join(temp_dir, 'final_video.mp4')
    
    print(f"Stitching video with {len(image_paths)} images and audio...")
    
    try:
        # verifies we have 10 images and 10 timings for each video
        if len(image_paths) != 10 or len(timings) != 10:
            raise ValueError(f"Expected 10 images and 10 timings, got {len(image_paths)} images and {len(timings)} timings")
        
        # creates a concat file for ffmpeg
        concat_file_path = os.path.join(temp_dir, 'concat_list.txt')
        
        with open(concat_file_path, 'w') as f:
            for i, (image_path, duration) in enumerate(zip(image_paths, timings)):
                f.write(f"file '{image_path}'\n")
                f.write(f"duration {duration}\n")
            
            f.write(f"file '{image_paths[-1]}'\n")
        
        # constructs the ffmpeg command
        # this command creates a video from images and syncs it with audio

        FFMPEG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'bin', 'ffmpeg.exe'))

        ffmpeg_command = [
            FFMPEG_PATH,
            '-y',  # overwrite output file if it exists
            '-f', 'concat',  # use concat demuxer
            '-safe', '0',  # allow absolute paths
            '-i', concat_file_path,  # input concat file with images
            '-i', audio_path,  # input audio file
            '-vsync', 'vfr',  # variable frame rate to match timings
            '-pix_fmt', 'yuv420p',  # pixel format for compatibility
            '-c:v', 'libx264',  # video codec
            '-preset', 'medium',  # encoding preset 
            '-crf', '23',  # quality
            '-c:a', 'aac',  # audio codec
            '-b:a', '192k',  # audio bitrate
            '-shortest',  # finish when shortest input ends
            output_path
        ]
        
        print(f"Running FFmpeg command...")
        
        # run the ffmpeg command
        result = subprocess.run(
            ffmpeg_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        
        print(f"FFmpeg completed successfully")
        
        # verify the output file exists
        if not os.path.exists(output_path):
            raise Exception("FFmpeg completed but output file was not created")
        
        # get file size for logging
        file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"Video created: {output_path} ({file_size_mb:.2f} MB)")
        
        return output_path
        
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e.stderr}")
        raise Exception(f"FFmpeg failed: {e.stderr}")
    except Exception as e:
        print(f"Error stitching video: {e}")
        raise

def get_video_info(video_path):
    """Helper function to get video information using ffprobe
    Useful for debugging
    """
    try:
        command = [
            'ffprobe',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            '-show_streams',
            video_path
        ]
        
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        
        import json
        info = json.loads(result.stdout)
        
        # FIXED - removed extra indentation
        duration = float(info['format'].get('duration', 0))
        size_mb = int(info['format'].get('size', 0)) / (1024 * 1024)
        
        print(f"Video info: {duration:.2f}s duration, {size_mb:.2f} MB")
        return info
        
    except Exception as e:
        print(f"Could not get video info: {e}")
        return None