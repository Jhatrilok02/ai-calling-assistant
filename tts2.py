# tts.py
import os
import requests
import logging
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tts")

class TTSService:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("MURF_API_KEY")
        self.base_url = "https://api.murf.ai/v1/speech/stream"
        os.makedirs("tts_output", exist_ok=True)

    def text_to_speech(self, text: str) -> str:
        try:
            # Generate unique filename for each TTS request
            filename = f"audio_{uuid.uuid4().hex}.wav"
            output_path = os.path.join("tts_output", filename)

            headers = {
                "api-key": self.api_key,
                "Content-Type": "application/json"
            }

            payload = {
                "text": text,
                "voiceId": "en-US-natalie",
                "format": "WAV"
            }

            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                stream=True
            )

            if response.status_code != 200:
                logger.error(f"Murf API returned {response.status_code}: {response.text}")
                return None

            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=4096):
                    if chunk:
                        f.write(chunk)

            logger.info(f"TTS audio saved to: {output_path}")
            print(f"🔊 Generated TTS file: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"TTS streaming error: {e}")
            return None




# import os
# import requests
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger("tts")

# class TTSService:
#     def __init__(self, api_key=None):
#         self.api_key = api_key or os.getenv("MURF_API_KEY")
#         self.base_url = "https://api.murf.ai/v1/speech/stream"
#         os.makedirs("tts_output", exist_ok=True)

#     def text_to_speech(self, text: str) -> str:
#         try:
#             headers = {
#                 "api-key": self.api_key,
#                 "Content-Type": "application/json"
#             }

#             payload = {
#                 "text": text,
#                 "voiceId": "en-US-natalie",
#                 "format": "WAV"
#             }

#             response = requests.post(
#                 self.base_url,
#                 headers=headers,
#                 json=payload,
#                 stream=True
#             )

#             if response.status_code != 200:
#                 logger.error(f"Murf API returned {response.status_code}: {response.text}")
#                 return None

#             output_path = os.path.join("tts_output", "greeting.wav")  # fixed filename for testing
#             with open(output_path, "wb") as f:
#                 for chunk in response.iter_content(chunk_size=4096):
#                     if chunk:
#                         f.write(chunk)

#             logger.info(f"TTS audio saved to: {output_path}")
#             print(f"🔊 Generated TTS file: {output_path}")
#             return output_path

#         except Exception as e:
#             logger.error(f"TTS streaming error: {e}")
#             return None




# # tts.py
# import os
# import requests
# import logging
# import subprocess

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger("tts")

# class TTSService:
#     def __init__(self, api_key=None):
#         self.api_key = api_key or os.getenv("MURF_API_KEY")
#         self.base_url = "https://api.murf.ai/v1/speech/stream"
#         os.makedirs("tts_output", exist_ok=True)

#     def convert_to_twilio_format(self, input_path: str, output_path: str):
#         try:
#             command = [
#                 "ffmpeg", "-y", "-i", input_path,
#                 "-ar", "8000", "-ac", "1", "-f", "wav", output_path
#             ]
#             subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#             return True
#         except Exception as e:
#             logger.error(f"FFmpeg conversion error: {e}")
#             return False

#     def text_to_speech(self, text: str) -> str:
#         try:
#             headers = {
#                 "api-key": self.api_key,
#                 "Content-Type": "application/json"
#             }

#             payload = {
#                 "text": text,
#                 "voiceId": "en-US-natalie",
#                 "format": "WAV"
#             }

#             response = requests.post(
#                 self.base_url,
#                 headers=headers,
#                 json=payload,
#                 stream=True
#             )

#             if response.status_code != 200:
#                 logger.error(f"Murf API returned {response.status_code}: {response.text}")
#                 return None

#             raw_path = os.path.join("tts_output", "greeting_raw.wav")
#             final_path = os.path.join("tts_output", "greeting.wav")

#             with open(raw_path, "wb") as f:
#                 for chunk in response.iter_content(chunk_size=4096):
#                     if chunk:
#                         f.write(chunk)

#             if not self.convert_to_twilio_format(raw_path, final_path):
#                 logger.error("Failed to convert audio to Twilio-compatible format.")
#                 return None

#             logger.info(f"TTS audio saved to: {final_path}")
#             print(f"🔊 Generated TTS file: {final_path}")
#             return final_path

#         except Exception as e:
#             logger.error(f"TTS streaming error: {e}")
#             return None
