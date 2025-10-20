#!/usr/bin/env python3
"""
Quick test script - creates video from existing images
No user input required, just runs with default settings
"""

import os
import glob
from main import build_video

def quick_test():
    #  create video from existing images
    
    print("🎬 Quick Video Test")
    
    # Check for images
    image_files = glob.glob("generated_images/*.png")
        
    # Create video with default settings
    output_file = "./generated_videos/quick_test.mp4"
    duration = 3  # 3 seconds per image
    
    print(f"Creating video: {output_file}")
    print(f"Duration per image: {duration} seconds")
    
    success = build_video(image_files, duration, output_file)
    
    if success:
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"Video created")
            print(f"Check the generated_videos folder for your video!")
        else:
            print(f"Video file not found:")
    else:
        print(f"Failed to create video")
    
    return success

if __name__ == "__main__":
    quick_test()
