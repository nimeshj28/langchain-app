import openai
from PIL import Image
import requests
import io

def generate_motivational_image(analysis_data, openai_api_key):
    summary = analysis_data.get('summary', '')
    strengths = ', '.join(analysis_data.get('strengths', []))
    emotions = ', '.join(analysis_data.get('emotions', []))
    image_prompt = (
        f"A realistic, inspiring scene representing personal growth and {emotions} emotions. "
        f"Scene showing someone with {strengths} in a natural setting. "
        "Warm lighting, motivational atmosphere, golden hour, professional photography, hopeful mood."
    )

    client = openai.OpenAI(api_key=openai_api_key)

    response = client.images.generate(
        model="dall-e-2",
        prompt=image_prompt,
        n=1,
        size="512x512",
        response_format="url"
    )

    img_url = response.data[0].url

    # Get image content
    img_response = requests.get(img_url)
    if img_response.status_code != 200:
        raise Exception(f"Failed to fetch image from OpenAI URL: {img_response.status_code}")
    image = Image.open(io.BytesIO(img_response.content))

    return image, image_prompt
