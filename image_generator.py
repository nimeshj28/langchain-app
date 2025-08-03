import requests
from PIL import Image
import io
import time
import base64

def generate_motivational_image(analysis_data, horde_api_key):
    # Prepare the prompt from your analysis_data
    summary = analysis_data.get('summary', '')
    strengths = ', '.join(analysis_data.get('strengths', []))
    emotions = ', '.join(analysis_data.get('emotions', []))

    image_prompt = (
        f"A realistic, inspiring scene representing personal growth and {emotions} emotions. "
        f"Scene showing someone with {strengths} in a natural setting. "
        "Warm lighting, motivational atmosphere, golden hour, professional photography, hopeful mood."
    )

    # Submit generation request
    API_URL = "https://stablehorde.net/api/v2/generate/async"
    headers = {
        "apikey": "sqxv_vIcDsXsl8D9bADrng",  # Use '0000000000' for public/free or your own key for better speed
        "Client-Agent": "streamlit-motivation-app/1.0"
    }
    payload = {
        "prompt": image_prompt,
        "params": {
            "n": 1,
            "width": 512,
            "height": 512,
            "steps": 20
        },
        "models": ["stable_diffusion"]
    }

    response = requests.post(API_URL, json=payload, headers=headers)
    if response.status_code != 202:
        raise Exception(f"Stable Horde API error: {response.status_code} - {response.text}")

    req_id = response.json()["id"]

    # Poll for completion
    status_url = f"https://stablehorde.net/api/v2/generate/status/{req_id}"
    for _ in range(24):  # ~2 minutes
        status_resp = requests.get(status_url, headers=headers)
        status_data = status_resp.json()
        if "generations" in status_data and status_data["generations"]:
            img_b64 = status_data["generations"][0]["img"]
            image = Image.open(io.BytesIO(base64.b64decode(img_b64)))
            return image, image_prompt
        time.sleep(5)
    raise Exception("Image was not ready. Please try again later.")

