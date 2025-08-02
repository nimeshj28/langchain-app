import requests
from PIL import Image
import io

def generate_motivational_image(analysis_data, hf_token):
    # Extract key themes for image prompt
    summary = analysis_data.get('summary', '')
    strengths = ', '.join(analysis_data.get('strengths', []))
    emotions = ', '.join(analysis_data.get('emotions', []))
    
    # Create prompt
    image_prompt = (
        f"A realistic, inspiring scene representing personal growth and {emotions} emotions. "
        f"Scene showing someone with {strengths} in a natural setting. "
        "Warm lighting, motivational atmosphere, golden hour, professional photography, hopeful mood."
    )
    
    # ✅ Replace model with a free, working one
    API_URL = "https://api-inference.huggingface.co/models/prompthero/openjourney"
    headers = {"Authorization": f"Bearer {hf_token}"}

    payload = {
        "inputs": image_prompt,
        "parameters": {
            "num_inference_steps": 20,
            "guidance_scale": 7.5
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload, timeout=60)

    if response.status_code == 200:
        try:
            image = Image.open(io.BytesIO(response.content))
            return image, image_prompt
        except Exception as e:
            raise Exception(f"Image parsing error: {str(e)}")
    else:
        raise Exception(f"HuggingFace API Error: {response.status_code} - {response.text}")
