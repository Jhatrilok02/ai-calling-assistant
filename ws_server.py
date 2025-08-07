import asyncio
import websockets
import base64
import json
import wave
import io
import whisper
import uuid
import logging

logging.basicConfig(level=logging.INFO)
model = whisper.load_model("base")

async def handle_connection(websocket):
    session_id = str(uuid.uuid4())
    logger = logging.getLogger(session_id)
    logger.info("🔗 WebSocket connection established.")

    audio_buffer = b''

    try:
        async for message in websocket:
            data = json.loads(message)
            if data.get("event") == "media":
                payload = base64.b64decode(data["media"]["payload"])
                audio_buffer += payload

            elif data.get("event") == "stop":
                logger.info("🛑 Stop received. Processing final transcription...")

                audio_file = io.BytesIO()
                with wave.open(audio_file, 'wb') as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(8000)
                    wf.writeframes(audio_buffer)

                audio_file.seek(0)
                result = model.transcribe(audio_file, language="en")
                logger.info(f"🗣 Caller said: {result['text']}")
                break

    except Exception as e:
        logger.error(f"WebSocket error: {e}")

    finally:
        logger.info("🚪 WebSocket connection closed.")

start_server = websockets.serve(handle_connection, host="0.0.0.0", port=9876)

if __name__ == "__main__":
    print("🔌 WebSocket server running on ws://0.0.0.0:9876/ws")
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()








# import asyncio
# import websockets
# import base64
# import json
# import wave
# import io
# import whisper
# import uuid
# import logging

# logging.basicConfig(level=logging.INFO)
# model = whisper.load_model("base")

# async def handle_connection(websocket):
#     session_id = str(uuid.uuid4())
#     logger = logging.getLogger(session_id)
#     logger.info("🔗 WebSocket connection established.")

#     audio_buffer = b''

#     try:
#         async for message in websocket:
#             data = json.loads(message)
#             if data.get("event") == "media":
#                 payload = base64.b64decode(data["media"]["payload"])
#                 audio_buffer += payload

#             elif data.get("event") == "stop":
#                 logger.info("🛑 Stop received. Processing final transcription...")

#                 audio_file = io.BytesIO()
#                 with wave.open(audio_file, 'wb') as wf:
#                     wf.setnchannels(1)
#                     wf.setsampwidth(2)
#                     wf.setframerate(8000)
#                     wf.writeframes(audio_buffer)

#                 audio_file.seek(0)
#                 result = model.transcribe(audio_file, language="en")
#                 logger.info(f"🗣 Caller said: {result['text']}")
#                 break

#     except Exception as e:
#         logger.error(f"WebSocket error: {e}")

#     finally:
#         logger.info("🚪 WebSocket connection closed.")

# start_server = websockets.serve(handle_connection, host="0.0.0.0", port=9876)

# if __name__ == "__main__":
#     print("🔌 WebSocket server running on ws://0.0.0.0:9876/ws")
#     asyncio.get_event_loop().run_until_complete(start_server)
#     asyncio.get_event_loop().run_forever()

