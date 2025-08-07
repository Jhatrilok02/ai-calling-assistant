import os
from dotenv import load_dotenv
from call_handler2 import CallHandler
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def main():
    twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
    twilio_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
    ngrok_url = os.getenv("NGROK_URL")  # e.g. https://xxxx.ngrok.io

    call_handler = CallHandler(twilio_sid, twilio_token, twilio_number, ngrok_url)

    to_number = input("Enter phone number (+CountryCode...): ").strip()
    call_sid = call_handler.make_call(to_number)
    if call_sid:
        logger.info(f"Call started successfully, SID: {call_sid}")
    else:
        logger.error("Failed to start call")

if __name__ == "__main__":
    main()



# # # main.py
# import os
# import logging
# from dotenv import load_dotenv
# from tts2 import TTSService
# from call_handler2 import CallHandler

# load_dotenv()
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class AICallingAgent:
#     def __init__(self):
#         self.tts = TTSService(api_key=os.getenv("MURF_API_KEY"))
#         self.call_handler = CallHandler(
#             account_sid=os.getenv("TWILIO_ACCOUNT_SID"),
#             auth_token=os.getenv("TWILIO_AUTH_TOKEN"),
#             twilio_number=os.getenv("TWILIO_PHONE_NUMBER"),
#             ngrok_url=os.getenv("NGROK_URL")  # Set your ngrok https URL here in .env
#         )
#         self.greeting = "Hello from Moonprenuer AI. How can I help you today?"

#     def start_call(self, phone_number: str):
#         audio_file = self.tts.text_to_speech(self.greeting)
#         if not audio_file:
#             logger.error("❌ Failed to generate TTS audio. Aborting call.")
#             return False

#         tts_filename = os.path.basename(audio_file)
#         logger.info(f"Using TTS audio file: {tts_filename}")

#         call_sid = self.call_handler.make_call(
#             to_number=phone_number,
#             tts_filename=tts_filename
#         )

#         if call_sid:
#             logger.info(f"Call started with SID: {call_sid}")
#             return True
#         else:
#             logger.error("❌ Failed to initiate call.")
#             return False

# if __name__ == "__main__":
#     agent = AICallingAgent()
#     number = input("Enter phone number (+CountryCode...): ").strip()
#     if agent.start_call(number):
#         print("Call started successfully!")
#     else:
#         print("Call failed.")

