import os
import requests
import base64
import subprocess
from dotenv import load_dotenv


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEBIUS_API_KEY = os.getenv("NEBIUS_API_KEY")

# Step 1: Generate Script

def generate_script(prompt, max_tokens=200, delimiter="|||"):
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
                "Each line should describe a visual scene for an AI-generated image."
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


# Step 2: Generate Images via Nebius

def generate_images_from_script(script_text, delimiter="|||", size="512x512"):
    print("Generating images...")
    lines = [line.strip() for line in script_text.split(delimiter) if line.strip()]

    url = "https://api.studio.nebius.ai/v1/image-generation"
    headers = {
        "Authorization": f"Bearer {NEBIUS_API_KEY}",
        "Content-Type": "application/json"
    }

    image_paths = []

    for idx, line in enumerate(lines):
        print(f"Scene {idx+1}/{len(lines)}: {line}")
        payload = {
            "model": "black-forest-labs/FLUX.1-schnell",
            "prompt": f"{line}, cinematic lighting, ultra-realistic",
            "size": size
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            print(f"Nebius API Error (line {idx+1}):", response.text)
            continue

        data = response.json()
        img_bytes = base64.b64decode(data["data"][0]["b64_json"])
        img_path = f"scene_{idx+1}.png"
        with open(img_path, "wb") as f:
            f.write(img_bytes)
        image_paths.append(img_path)
        print(f"✅ Saved {img_path}\n")

    return image_paths


# Step 3: Build Video with FFmpeg

def build_video(image_files, duration=3, output_file="output.mp4"):
    """
    Uses FFmpeg to create a slideshow video from images.
    Each image stays on screen for `duration` seconds.
    """
    print("🎬 Building video with FFmpeg...")

    # Create the slideshow file
    with open("slideshow.txt", "w") as f:
        for img in image_files:
            f.write(f"file '{img}'\n")
            f.write(f"duration {duration}\n")

    # FFmpeg command
    cmd = [
        "ffmpeg", "-f", "concat", "-safe", "0", "-i", "slideshow.txt",
        "-vf", "scale=1280:720,format=yuv420p", "-pix_fmt", "yuv420p",
        "-y", output_file
    ]

    subprocess.run(cmd, check=True)
    print(f"Video created successfully: {output_file}")


# Step 4: Run the Whole Flow

if __name__ == "__main__":
    
    user_prompt = input("Enter your video topic: ")

    script = generate_script(user_prompt)
    if script:
        image_files = generate_images_from_script(script)
        if image_files:
            build_video(image_files)
            print("\nAll done! Check output.mp4 in your folder.")
