# This program should take in the user input: I want a story based on ________.
# Feed this into the LLM along with instructions to create a 10 line script for a short video based on this story.
# We have a set of booleans for all 15 scenes which the llm decides to have true or false for … like an audio effect or a shake, and so on
# Use each line of the script to produce an image related to that line.
# API reference: https://platform.openai.com/docs/quickstart?desktop-os=macOS&language=python
# Compare OpenAI models: https://platform.openai.com/docs/models/compare
# OpenAI pricing: https://openai.com/api/pricing/

from openai import OpenAI
import image_generation

OPEN_API_KEY = ""

def invoke_openai(user_prompt):
    client = OpenAI(api_key = OPEN_API_KEY)

    response = client.responses.create(
        model="gpt-4.1-nano",   # default is gpt-5. gpt-4.1-nano is cheaper. I haven't really noticed a big difference in output quality.
        input=f"Create a 10 line script for a short video based on this story: {user_prompt}\n Label each line with a number. Don't include any additional text besides the script of 10 lines.",
    )

    return response.output_text

def main():
    user_prompt = input("What type of video would you like to create and about what? ")  # This is what the user enters on the website.
    
    response = invoke_openai(user_prompt)
    script_line = response.split('\n')
    
    print(f"\n{response}\n")  # debug
    print(script_line) # debug

    for i, line in enumerate(script_line):
        completion = image_generation.invoke_nebius_image_generation(line)  # generates an image for each line in the script.

        image_generation.decode_b64_images(completion, i)    # saves the image to a file.



if __name__ == "__main__":
    main()

