from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import replicate
import requests
import os

app = Flask(__name__)

API_TOKEN = 'r8_TEWKUO0yazE3Ujr2WuFwa6TZ6UrSc5K1uukZw' 
client = replicate.Client(api_token=API_TOKEN)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    image_available = False
    if request.method == 'POST':
        prompt = request.form['prompt']
        if prompt:
            generate_image_from_text(prompt)
            message = "Processing your request, please wait..."
            image_available = True  
    return render_template('index.html', message=message, image_available=image_available)

def generate_image_from_text(prompt, width=1024, height=1024, output_file='output_image.png'):
    input_data = {"prompt": prompt, "width": width, "height": height}
    output = client.run("ai-forever/kandinsky-2.2:ad9d7879fbffa2874e1d909d1d37d9bc682889cc65b31f7bb00d2362619f194a", input=input_data)
    image_url = output[0]
    image_response = requests.get(image_url)
    with open(os.path.join('static', output_file), 'wb') as file:
        file.write(image_response.content)
    print("Image successfully saved.")

@app.route('/static/<filename>')
def uploaded_file(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
