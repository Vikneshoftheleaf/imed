from flask import Flask, request, render_template, send_file, jsonify
from google import genai
from google.genai import types
import os
import requests
import mimetypes
import os
from IPython.display import display, Markdown, Image
import pathlib
import PIL
import io
import base64



def display_response(response):
  for part in response.candidates[0].content.parts:
    if part.text is not None:
      display(Markdown(part.text))
    elif part.inline_data is not None:
      mime = part.inline_data.mime_type
      print(mime)
      data = part.inline_data.data
      display(Image(data=data))

def save_image(response):
  for part in response.candidates[0].content.parts:
    if part.text is not None:
      continue
    elif part.inline_data is not None:
      mime = part.inline_data.mime_type
      data = part.inline_data.data
      #pathlib.Path(path).write_bytes(data)
      return data
      


# Initialize Gemini API client
client = genai.Client(api_key="AIzaSyCIYdBLuJe97rNB3gtcsI4RHGUumiioD8Y")


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/edit', methods=['POST'])
def edit_image():
    text = request.form.get('message') 
    image = request.files.get('image')  

    if image:
        """
        image_path = os.path.join('static', image.filename)
        image.save(image_path)  # Save the image
        """
        MODEL_ID = "gemini-2.0-flash-exp"
        try:
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=[
                    text,
                    PIL.Image.open(image)
                ],
                config=types.GenerateContentConfig(
                    response_modalities=['Text', 'Image'],
                    safety_settings=[
                
                
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                ),
                
                ]
                )
            )
            
            #display_response(response)
            #save_image(response, 'static/newgen.png')
            image_data=save_image(response)
            encoded_image = base64.b64encode(image_data).decode('utf-8')
            
            return jsonify({
                "image_url": encoded_image
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
if __name__ == "__main__":
    
    app.run(debug=True)
