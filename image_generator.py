import requests
from PIL import Image
import io
import time
import base64

def generate_motivational_image(analysis_data, horde_api_key):
    summary = analysis_data.get('summary', '')
    strengths = ', '.join(analysis_data.get('strengths', []))
    emotions = ', '.join(analysis_data.get('emotions', []))
    image_prompt = (
        f"A realistic, inspiring scene representing personal growth and {emotions} emotions. "
        f"Scene showing someone with {strengths} in a natural setting. "
        "Warm lighting, motivational atmosphere, golden hour, professional photography, hopeful mood."
    )
    API_URL = "https://stablehorde.net/api/v2/generate/async"
    headers = {
        "apikey": horde_api_key,
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
    status_url = f"https://stablehorde.net/api/v2/generate/status/{req_id}"
    for _ in range(30):  # now polls for 2.5 minutes
        status_resp = requests.get(status_url, headers=headers)
        status_data = status_resp.json()
        gens = status_data.get("generations")
        if gens and isinstance(gens, list) and len(gens) > 0:
            img_b64 = gens[0].get("img")
            if img_b64:
                try:
                    image_bytes = base64.b64decode(img_b64)
                    image = Image.open(io.BytesIO(image_bytes))
                    return image, image_prompt
                except Exception as e:
                    raise Exception(f"Stable Horde returned invalid image data ({str(e)}).")
            else:
                raise Exception("Stable Horde did not return an image (empty 'img' field).")
        # also check for failure state
        if status_data.get("faulted") or status_data.get("done", False) and not gens:
            raise Exception("Stable Horde unable to generate an image (no valid worker, or job faulted).")
        time.sleep(5)
    raise Exception("Image generation timed out (waited too long for a result).")
