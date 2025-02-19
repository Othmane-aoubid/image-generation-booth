from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import base64
import io
from PIL import Image

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

SD_API_URL = "https://16e9dcbb5efb6c24e0.gradio.live/sdapi/v1/img2img"

def image_to_base64(image_data):
    # Convert PIL Image to base64
    buffered = io.BytesIO()
    image_data.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def generate_image(prompt, image_data, model_id=""):
    # Convert the image data to base64
    image_base64 = image_to_base64(image_data)
    
    # Customize settings based on model_id
    settings = {
        "model1": {  # Style Transfer
            "steps": 20,
            "guidance_start": 0.3,
            "guidance_end": 0.7,
            "weight": 1.0
        },
        "model2": {  # Portrait Effects
            "steps": 15,
            "guidance_start": 0.4,
            "guidance_end": 0.8,
            "weight": 1.1
        },
        "model3": {  # Artistic Filter
            "steps": 25,
            "guidance_start": 0.2,
            "guidance_end": 0.9,
            "weight": 1.3
        }
    }
    
    model_settings = settings.get(model_id, settings["model1"])
    
    payload = {
        "model": "DreamShaper_3.32_baked_vae_clip_fix",
        "prompt": prompt,
        "steps": model_settings["steps"],
        "save_images": True,
        "negative_prompt": "",
        "init_images": [f"data:image/jpeg;base64,{image_base64}"],
        "alwayson_scripts": {
            "ControlNet": {
                "args": [
                    {
                        "enabled": True,
                        "model": "control_sd15_canny [fef5e48e]",
                        "module": "canny",
                        "image": {"image": f"data:image/jpeg;base64,{image_base64}"},
                        "guidance_start": model_settings["guidance_start"],
                        "guidance_end": model_settings["guidance_end"],
                        "weight": model_settings["weight"],
                        "control_mode": "Balanced",
                        "resize_mode": "Just Resize"
                    }
                ]
            }
        }
    }
    
    try:
        response = requests.post(SD_API_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        # Extract the generated image from the response
        if "images" in result and len(result["images"]) > 0:
            return {"success": True, "image_data": result["images"][0]}
        else:
            return {"success": False, "error": "No image generated"}
            
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}

@app.route('/generate', methods=['POST'])
def handle_generate():
    try:
        if 'image' not in request.files:
            return jsonify({"success": False, "error": "No image file provided"}), 400
            
        image_file = request.files['image']
        model_id = request.form.get('model_id', 'model1')
        prompt = request.form.get('prompt', '')
        
        # Open and process the image
        image = Image.open(image_file)
        
        # Generate the image
        result = generate_image(prompt, image, model_id)
        
        if result["success"]:
            return jsonify({
                "success": True,
                "image_url": f"data:image/png;base64,{result['image_data']}"
            })
        else:
            return jsonify({"success": False, "error": result["error"]}), 500
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
