from mistralai import Mistral
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.environ["MISTRAL_API_KEY"]
client = Mistral(api_key=api_key)

def load_image(image_path):
    """Convert image to base64 data URI."""
    try:
        import base64
        with open(image_path, "rb") as image_file:
            base64_encoded = base64.b64encode(image_file.read()).decode('utf-8')

        base64_url = f"data:image/png;base64,{base64_encoded}"
        print(f"Generated base64 URL starts with: {base64_url[:50]}...")  # Debug
        return base64_url
    except Exception as e:
        print(f"Error in load_image: {str(e)}")
        return None



messages = [
  {
    "role": "user",
    "content": [
      {
        "type": "text",
        "text": "Explain this document in detail to someone who doesn't have a technical background",
      },
      {
        "type": "image_url",
        "image_url": load_image("test.png"),
      },
    ],
  }
]
chat_response = client.chat.complete(
  model="mistral-small-latest",
  messages=messages,
)
print(chat_response.choices[0].message.content)