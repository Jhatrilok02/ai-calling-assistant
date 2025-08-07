from flask import Flask, request, send_file, abort
from twilio.twiml.voice_response import VoiceResponse, Gather
from tts2 import TTSService
from nlp import NLPProcessor
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
AUDIO_FOLDER = "tts_output"

tts = TTSService()
nlp = NLPProcessor()

# Get ngrok URL from environment variables
NGROK_URL = os.getenv("NGROK_URL")

@app.route("/audio/<filename>")
def serve_audio(filename):
    full_path = os.path.abspath(os.path.join(AUDIO_FOLDER, filename))
    print(f"🔊 Attempting to serve audio: {full_path}")
    
    if not os.path.exists(full_path):
        print(f"❌ Audio file not found: {full_path}")
        abort(404)
        
    print(f"✅ Serving audio file: {full_path}")
    return send_file(full_path)

@app.route("/outbound_call", methods=["POST"])
def outbound_call():
    resp = VoiceResponse()
    welcome_text = "Hello from Moonprenuer AI. How can I help you today?"
    welcome_path = tts.text_to_speech(welcome_text)

    if not welcome_path:
        print("❌ TTS generation failed for welcome message.")
        return "TTS generation failed", 500

    welcome_file = os.path.basename(welcome_path)
    audio_url = f"{NGROK_URL}/audio/{welcome_file}"
    print(f"🎙️ Generated audio URL: {audio_url}")

    gather = Gather(input="speech", action="/process_speech", method="POST", timeout=5)
    gather.play(audio_url)
    resp.append(gather)

    return str(resp)

@app.route("/process_speech", methods=["POST"])
def process_speech():
    user_input = request.values.get("SpeechResult", "").strip()
    resp = VoiceResponse()

    if not user_input:
        resp.say("Sorry, I didn't catch that. Goodbye!")
        resp.hangup()
        return str(resp)

    print(f"🗣 User said: {user_input}")
    ai_reply = nlp.generate_response(user_input)
    print(f"🤖 AI reply: {ai_reply}")

    reply_path = tts.text_to_speech(ai_reply)
    if not reply_path:
        print("❌ TTS generation failed for AI reply.")
        return "TTS generation failed", 500

    reply_file = os.path.basename(reply_path)
    audio_url = f"{NGROK_URL}/audio/{reply_file}"
    print(f"🎙️ Generated response audio URL: {audio_url}")

    gather = Gather(input="speech", action="/process_speech", method="POST", timeout=5)
    gather.play(audio_url)
    resp.append(gather)

    return str(resp)

@app.route("/call-status", methods=["POST"])
def call_status():
    print("📞 Call status update:", request.form)
    return ("", 204)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8765)





#**********************************************************************************************************

# from flask import Flask, request, send_file, abort
# from twilio.twiml.voice_response import VoiceResponse, Gather
# from tts2 import TTSService
# from nlp import NLPProcessor
# from dotenv import load_dotenv
# import os

# load_dotenv()

# app = Flask(__name__)
# AUDIO_FOLDER = "tts_output"

# tts = TTSService()
# nlp = NLPProcessor()

# @app.route("/audio/<filename>")
# def serve_audio(filename):
#     full_path = os.path.abspath(os.path.join(AUDIO_FOLDER, filename))
#     if os.path.exists(full_path):
#         print(f"✅ Serving: {full_path}")
#         return send_file(full_path)
#     print(f"❌ Not Found: {full_path}")
#     abort(404)

# @app.route("/outbound_call", methods=["POST"])
# def outbound_call():
#     resp = VoiceResponse()
#     welcome_text = "Hello from Moonprenuer AI. How can I help you today?"
#     welcome_path = tts.text_to_speech(welcome_text)

#     if not welcome_path:
#         print("❌ TTS generation failed for welcome message.")
#         return "TTS generation failed", 500

#     welcome_file = os.path.basename(welcome_path)
#     gather = Gather(input="speech", action="/process_speech", method="POST", timeout=5)
#     gather.play(f"{request.url_root}audio/{welcome_file}")
#     resp.append(gather)

#     resp.say("No input received. Goodbye!")
#     resp.hangup()
#     return str(resp)

# @app.route("/process_speech", methods=["POST"])
# def process_speech():
#     user_input = request.values.get("SpeechResult", "").strip()
#     resp = VoiceResponse()

#     if not user_input:
#         resp.say("Sorry, I didn't catch that. Goodbye!")
#         resp.hangup()
#         return str(resp)

#     print(f"🗣 User said: {user_input}")
#     ai_reply = nlp.generate_response(user_input)
#     print(f"🤖 AI reply: {ai_reply}")

#     reply_path = tts.text_to_speech(ai_reply)
#     if not reply_path:
#         print("❌ TTS generation failed for AI reply.")
#         return "TTS generation failed", 500

#     reply_file = os.path.basename(reply_path)
#     gather = Gather(input="speech", action="/process_speech", method="POST", timeout=5)
#     gather.play(f"{request.url_root}audio/{reply_file}")
#     resp.append(gather)

#     resp.say("No input received. Goodbye!")
#     resp.hangup()
#     return str(resp)

# @app.route("/call-status", methods=["POST"])
# def call_status():
#     print("📞 Call status update:", request.form)
#     return ("", 204)

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=9876)



#****************************************************************************************************

# from flask import Flask, send_file, abort
# import os

# app = Flask(__name__)
# AUDIO_FOLDER = "tts_output"

# @app.route("/audio/<filename>")
# def serve_audio(filename):
#     full_path = os.path.abspath(os.path.join(AUDIO_FOLDER, filename))
#     print(f"Serving file from absolute path: {full_path}")
#     if os.path.exists(full_path):
#         try:
#             return send_file(full_path)
#         except Exception as e:
#             print(f"Error sending file: {e}")
#             abort(404)
#     else:
#         print(f"File not found: {full_path}")
#         abort(404)

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=9876)
