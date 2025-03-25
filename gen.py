from google import genai
from google.genai import types
import requests
import mimetypes
import os
from IPython.display import display, Markdown, Image
import pathlib
import PIL
# Initialize Gemini API client
client = genai.Client(api_key="AIzaSyCIYdBLuJe97rNB3gtcsI4RHGUumiioD8Y")

contents = 'a yellow ferarai car'
MODEL_ID = "gemini-2.0-flash-exp"

response = client.models.generate_content(
    model=MODEL_ID,
    contents=[
        "change the car color to blue",
        PIL.Image.open('gen.png')
    ],
    config=types.GenerateContentConfig(
        response_modalities=['Text', 'Image']
    )
)



def display_response(response):
  for part in response.candidates[0].content.parts:
    if part.text is not None:
      display(Markdown(part.text))
    elif part.inline_data is not None:
      mime = part.inline_data.mime_type
      print(mime)
      data = part.inline_data.data
      display(Image(data=data))

def save_image(response, path):
  for part in response.candidates[0].content.parts:
    if part.text is not None:
      continue
    elif part.inline_data is not None:
      mime = part.inline_data.mime_type
      data = part.inline_data.data
      pathlib.Path(path).write_bytes(data)
      
      
display_response(response)
save_image(response, 'static/newgen.png')


