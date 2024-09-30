import edge_tts
import asyncio

async def text_to_speech(text, output_file):
    # Initialize the TTS object with default settings
    print("Hello eawrhere")
    print(text)
    communicate = edge_tts.Communicate(text, voice='en-US-JennyNeural')  # You can change the voice if needed
    print("Hello here")
    # Save the audio to an output file
    await communicate.save(output_file)
    print("hi I passed here")
    print(f"Text-to-speech conversion completed. Audio saved as: {output_file}")

# Wrapper function to run the async function from synchronous code
def run_text_to_speech(text, output_file):
    asyncio.run(text_to_speech(text, output_file))

# Example usage
if __name__ == "__main__":
    text = "Hello! This is an example of text to speech using edge-tts in Python."
    output_file = "output.mp3"  # File where the audio will be saved
    run_text_to_speech(text, output_file)
