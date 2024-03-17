from openai import OpenAI
import os

api_key = os.getenv("API_KEY")

def generate_description(camera: dict):
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user",
         "content": f"Imagine that you are describing camera to a customer"
                    f" to sell it dont include your personal experience with camera"
                    f" and provide a concise and brief description of a  camera with"
                    f" specifications but without mentioning the price or detailed URL."
                    f"{str(camera)}"}
      ]
    )

    return dict(completion.choices[0].message)['content']