from twilio.rest import Client
import logging
import os

logger = logging.getLogger(__name__)

class CallHandler:
    def __init__(self, account_sid, auth_token, twilio_number, ngrok_url):
        self.client = Client(account_sid, auth_token)
        self.twilio_number = twilio_number
        self.ngrok_url = ngrok_url.rstrip('/')

    def make_call(self, to_number):
        try:
            twiml_url = f"{self.ngrok_url}/outbound_call"
            call = self.client.calls.create(
                url=twiml_url,
                to=to_number,
                from_=self.twilio_number,
                record=True,
                status_callback=f"{self.ngrok_url}/call-status",
                status_callback_event=['initiated', 'ringing', 'answered', 'completed']
            )
            logger.info(f"Call initiated: SID {call.sid}")
            return call.sid
        except Exception as e:
            logger.error(f"Failed to make call: {e}")
            return None





# # call_handler.py
# from twilio.rest import Client
# import logging
# import os

# logger = logging.getLogger(__name__)

# class CallHandler:
#     def __init__(self, account_sid: str, auth_token: str, twilio_number: str, ngrok_url: str):
#         self.client = Client(account_sid, auth_token)
#         self.twilio_number = twilio_number
#         self.ngrok_url = ngrok_url.rstrip('/')
#         os.makedirs("call_logs", exist_ok=True)

#     def make_call(self, to_number: str, tts_filename: str) -> str:
#         try:
#             audio_url = f"{self.ngrok_url}/audio/{tts_filename}"
#             twiml_response = f"""
#             <Response>
#                 <Play>{audio_url}</Play>
#                 <Pause length="3600"/>
#                 <Say voice="Polly.Joanna">Thank you for your time. Goodbye!</Say>
#             </Response>
#             """
#             logger.info(f"TwiML: {twiml_response.strip()}")

#             call = self.client.calls.create(
#                 twiml=twiml_response,
#                 to=to_number,
#                 from_=self.twilio_number,
#                 record=True,
#                 status_callback='https://your-server.com/call-status',  # Replace accordingly
#                 status_callback_event=['initiated', 'ringing', 'answered', 'completed']
#             )
#             logger.info(f"Call initiated to {to_number}, SID: {call.sid}")
#             return call.sid
#         except Exception as e:
#             logger.error(f"Failed to make call: {e}")
#             return None
