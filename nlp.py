# nlp.py (FOR OPENAI SDK >= 1.0.0)
import os
from openai import OpenAI
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("nlp")

class NLPProcessor:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)

    def generate_response(self, user_input: str) -> str:
        try:
            completion = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an AI voice assistant helping users over a call."},
                    {"role": "user", "content": user_input}
                ]
            )
            response = completion.choices[0].message.content.strip()
            logger.info(f"Generated NLP response: {response}")
            return response
        except Exception as e:
            logger.error(f"NLP error: {e}")
            return "I'm sorry, something went wrong."



# import openai
# import os

# class NLPProcessor:
#     def __init__(self, api_key=None):
#         self.api_key = api_key or os.getenv("OPENAI_API_KEY")
#         openai.api_key = self.api_key

#     def generate_response(self, prompt: str) -> str:
#         try:
#             response = openai.ChatCompletion.create(
#                 model="gpt-4o",  # or gpt-4
#                 messages=[
#                     {"role": "system", "content": "You are a helpful AI assistant."},
#                     {"role": "user", "content": prompt}
#                 ]
#             )
#             return response.choices[0].message["content"].strip()
#         except Exception as e:
#             print(f"NLP error: {e}")
#             return "I'm sorry, something went wrong."
