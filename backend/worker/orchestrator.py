#This will run the full ai pipeline
import os
from app import app
from celery import Task
import database
import script
import images_generated
import voice_over
import assemble
import storage

def create_silent_audio(job_id):
    """Create a silent audio file for testing without AWS"""
    import subprocess
    temp_dir = f'/tmp/keyframe_job_{job_id}'
    os.makedirs(temp_dir, exist_ok=True)  # ADD THIS LINE
    audio_path = f'{temp_dir}/silent.mp3'
    
    # create 60 seconds of silence
    subprocess.run([
        'ffmpeg', '-y', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo',
        '-t', '60', '-q:a', '9', '-acodec', 'libmp3lame', audio_path
    ], check=True)
    
    return audio_path
    
@app.task(bind=True)
def process_video_job(self,job_data):
    """
    Main task that processes a video generation job
    Takes job_data dict with: { id, prompt, style }
    """
    job_id=job_data['id']
    prompt =job_data['prompt']
    style=job_data['style']
    
    try:
        print(f"Starting job {job_id}-Style:{style}")
        #updates status to processing
        database.update_job_status(job_id,'processing')

        # step 1:generate the script using openai
        print(f"Job {job_id}: Generating script...")
        script_data = script.generate_script(prompt,style)
        
        # step 2:generate images for each slide using nebius
        print(f"Job {job_id}: Generating images...")
        image_paths = images_generated.generate_images(script_data, job_id)
        
        #need to ass the actual video api later for amazon polly
        # step 3: TEMPORARY - skip voiceover (no AWS keys yet)
        print(f"Job {job_id}: Skipping voiceover (no AWS keys)...")
        audio_path = create_silent_audio(job_id)
        
        # step 4:stitch everything together with ffmpeg
        print(f"Job {job_id}: Assembling video...")
        video_path = assemble.stitch_video(image_paths, audio_path, script_data['timings'], job_id)
        
            # step 5:TEMPORARY - skip upload for testing
        print(f"Job {job_id}: Skipping upload (testing locally)...")
        video_url = f"LOCAL: {video_path}"
        thumbnail_url = f"LOCAL: {video_path}"
        
        print(f"Video created at: {video_path}")
        
        # step 6: mark job as complete in database
        database.update_job_completed(job_id, video_url, thumbnail_url)
        
        print(f"Job {job_id} completed successfully!")
        return {
            'status': 'success',
            'job_id': job_id,
            'video_url': video_url,
            'thumbnail_url': thumbnail_url
        }
        

    except Exception as e:
        # if anything fails, mark the job as failed
        print(f"Job {job_id} failed with error: {str(e)}")
        database.update_job_status(job_id, 'failed')
        
        # raise the exception so celery knows it failed
        raise e