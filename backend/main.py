import os
import requests
import base64
import subprocess
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEBIUS_API_KEY = os.getenv("NEBIUS_API_KEY")

#Generate Script
def generate_script(prompt, max_tokens=200, delimiter="|||", theme="educational"):
    print("Generating script with OpenAI...")

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You write short, cinematic scripts for slideshow videos."},
            {"role": "user", "content": (
                f"{prompt} "
                f"Write 5 distinct scene lines, separated by the delimiter '{delimiter}'. "
                f"Each line should describe a visual scene for an AI-generated image. The theme should be {theme}."
            )}
        ],
        "max_tokens": max_tokens
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        print("OpenAI API Error:", response.text)
        return None

    data = response.json()
    script = data["choices"][0]["message"]["content"].strip()
    print("Script generated!\n")
    print("Full Script:\n")
    print(script)
    print("\n" + "-"*50 + "\n")
    return script


#Generate Images via Nebius

#nebius api call
def invoke_nebius_image_generation(prompt):
    """Generate image using Nebius API with OpenAI client"""
    client = OpenAI(
        base_url="https://api.studio.nebius.com/v1",
        api_key=NEBIUS_API_KEY,
    )

    completion = client.images.generate(
        model="black-forest-labs/flux-schnell",
        prompt=prompt,
        response_format="b64_json",
        extra_body={
            "response_extension": "png",
            "width": 512,
            "height": 512,
            "num_inference_steps": 16,
            "seed": -1,
            "negative_prompt": "blurry, low quality, distorted"
        }
    )

    return completion

#generation from script
def generate_images_from_script(script_text, delimiter="|||"):
    print("Generating images...")
    lines = [line.strip() for line in script_text.split(delimiter) if line.strip()]
    
    if not lines:
        print("No lines found in script!")
        return []

    image_paths = []
    
    # Create generated_images directory if it doesn't exist
    os.makedirs("generated_images", exist_ok=True)

    for idx, line in enumerate(lines):
        print(f"Scene {idx+1}/{len(lines)}: {line}")
        
        try:
            completion = invoke_nebius_image_generation(line)
            
            # Decode and save the image
            image_bytes = base64.b64decode(completion.data[0].b64_json)
            img_path = f"generated_images/scene_{idx+1:02d}.png"
            
            with open(img_path, "wb") as f:
                f.write(image_bytes)
            
            image_paths.append(img_path)
            print(f"Saved {img_path}\n")
                
        except Exception as e:
            print(f"Error generating image for line {idx+1}: {str(e)}")
            continue

    print(f"Generated {len(image_paths)} images successfully")
    return image_paths


#Build Video with FFmpeg
#make sure ffmpeg is installed and in your path
def build_video(image_files, duration=3, output_file="./generated_videos/output.mp4"):
    print("Building video with FFmpeg...")
    
    if not image_files:
        print("No image files provided for video creation!")
        return False
    
    # Check if all image files exist
    missing_files = [f for f in image_files if not os.path.exists(f)]
    if missing_files:
        print(f"Missing image files: {missing_files}")
        return False
    
    # Create generated_videos directory if it doesn't exist
    os.makedirs("generated_videos", exist_ok=True)
    
    fps = str(1 / duration) #makes it duration amount of seconds per picture

    try:
        cmd = [
            "ffmpeg",
            "-framerate", fps, 
            "-i", "generated_images/scene_%02d.png",  # numbered images
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            # "-vf", "scale=1280:720", makes it into 1280:720, not ideal since the photos are made in 512 x 512, but can be good for final outputs.
            "-y",
            output_file
        ]

        print("Running FFmpeg command...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"Video created successfully: {output_file}")
        return True
        

    except Exception as e:
        print(f"Unexpected error during video creation: {e}")
        return False


# Step 4: Run the Whole Flow
if __name__ == "__main__":
    
    user_prompt = input("Enter your video topic: ")

    script = generate_script(user_prompt)
    if script:
        image_files = generate_images_from_script(script)
        if image_files:
            success = build_video(image_files)
            if success:
                print("\n🎉 Video created successfully!")
                print("Video saved in 'generated_videos' folder")
            else:
                print("\nVideo creation failed. Check the error messages above.")
        else:
            print("\nNo images were generated. Check the error messages above.")
    else:
        print("\nScript generation failed. Check your API key and try again.")
