# information on LORA adapters to maintain similar bg on generated images: https://docs.studio.nebius.com/ai-models-inference/image-lora
from openai import OpenAI
import os
import base64
import subprocess

NEBIUS_KEY = "eyJhbGciOiJIUzI1NiIsImtpZCI6IlV6SXJWd1h0dnprLVRvdzlLZWstc0M1akptWXBvX1VaVkxUZlpnMDRlOFUiLCJ0eXAiOiJKV1QifQ.eyJzdWIiOiJnb29nbGUtb2F1dGgyfDExNTU3NzQzMTY1MjA4OTY3MjQ5NCIsInNjb3BlIjoib3BlbmlkIG9mZmxpbmVfYWNjZXNzIiwiaXNzIjoiYXBpX2tleV9pc3N1ZXIiLCJhdWQiOlsiaHR0cHM6Ly9uZWJpdXMtaW5mZXJlbmNlLmV1LmF1dGgwLmNvbS9hcGkvdjIvIl0sImV4cCI6MTkxNzQ5MDMzOSwidXVpZCI6IjAxOTliY2RlLWNlMGUtNzU0ZS1iNTAyLTJmMTQwMGFlYjkzYSIsIm5hbWUiOiJLZXlGcmFtZSIsImV4cGlyZXNfYXQiOiIyMDMwLTEwLTA2VDA0OjEyOjE5KzAwMDAifQ.lbqGwpNFwCZG4RwUp1T6r1q09fOYW4YUH5UdWR8woBA"

def invoke_nebius_image_generation(NEBIUS_KEY, prompt):
    client = OpenAI(
        base_url="https://api.studio.nebius.com/v1",
        api_key=NEBIUS_KEY,
    )

    # This API call does not support batch imaging in a single request. In order to generate multiple images the request would have to be placed in a loop.
    completion = client.images.generate(
        model="black-forest-labs/flux-schnell", # specify which Nebius model to use.
        prompt=prompt,
        response_format="b64_json",  # other option is url which returns a link to the images.
        extra_body={    # All of these parameters are optional.
            "response_extension": "png",
            "width": 512,
            "height": 512,
            "num_inference_steps": 16,  # max number of 16. Higher values take longer but produce better results.
            "seed": -1,     # controls the randomness of the image generation process. Use -1 to produce random image. Using a specific number with the same prompt and other parameters will produce the same image.
            "negative_prompt": "night sky"    # specify what you don't want in the image.
        }
    )

    return completion   # returns an object of ImagesResponse. Could also alter to return json: json.loads(completion.to_json())

def decode_b64_images(completion, i):
    image_bytes = base64.b64decode(completion.data[0].b64_json)
    with open(f"generated_images/image_{i}.png", "wb") as f:
        f.write(image_bytes)

def create_video():
    # FFmpeg command to create a video from images. Need to install ffmpeg on system (macOS): brew install ffmpeg
    command = [
        "ffmpeg",
        "-framerate", "1", # frames per second
        "-pattern_type", "glob",
        "-i", "generated_images/*.png",  # use all png files stored in specified folder
        "-c:v", "libx264",  # video codec
        "-pix_fmt", "yuv420p",  # pixel format
        "generated_images/video.mp4"   # output file path
    ]

    # Run the command
    subprocess.run(command, check=True)


def main():
    prompt = "A picture of a comic book about 2 superheros flying over a city and rescuing people."

    os.makedirs("generated_images", exist_ok=True)
    for i in range(3):
        completion = invoke_nebius_image_generation(NEBIUS_KEY, prompt)
        print(f"{i}: {completion.to_json()}")   # debug

        decode_b64_images(completion, i)    # saves the image to a file.
    
    create_video()  # creates a video from all images in the specified folder.

    

if __name__ == "__main__":
    main()
