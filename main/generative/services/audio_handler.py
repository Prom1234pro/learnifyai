from edge_tts import list_voices, Communicate
import asyncio

class AudioService:
    def __init__(self, voice):
        self.voice = voice

    async def print_voices(self):
        """Print all available voices."""
        voices = await list_voices()
        return voices

    async def run_text_to_speech(self, text, output_file):
        """Execute text-to-speech conversion."""
        communicate = Communicate(text, voice=self.voice)
        await communicate.save(output_file)


    # Wrapper function to handle text-to-speech conversion
    def execute(self, text, output_file, voice="en-AU-WilliamNeural"):
        # Run the async function from synchronous code
        asyncio.run(self.run_text_to_speech(text, output_file))


if __name__ == "__main__":
    # Example usage
    service = AudioService("en-AU-WilliamNeural")
    service.run_text_to_speech("Taiye is a stubborn boy", "output2.mp3")
