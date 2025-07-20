"""
Custom image generation tool that directly calls OpenAI's DALL-E API.
Returns actual image URLs instead of descriptions.
"""

from typing import Literal, cast
from agents import function_tool
from openai import OpenAI
from utils.config import config

# Initialize OpenAI client using config
client = OpenAI(api_key=config.OPENAI_API_KEY)


@function_tool
def generate_image(
    prompt: str,
    size: Literal["1024x1024", "1024x1792", "1792x1024"] = "1024x1024",
    quality: Literal["standard", "hd"] = "standard",
    style: Literal["vivid", "natural"] = "vivid",
    n: int = 1
) -> str:
    """
    Generate an image using OpenAI's DALL-E API.

    Args:
        prompt: The text prompt to generate an image from
        size: Size of the image (1024x1024, 1024x1792, or 1792x1024)
        quality: Quality of the image (standard or hd)
        style: Style of the image (vivid or natural)
        n: Number of images to generate (1-10)

    Returns:
        URL of the generated image
    """
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality=quality,
            style=style,
            n=n,
            response_format="url"
        )

        # Return the URL of the first generated image
        if response.data and len(response.data) > 0:
            return cast(str, response.data[0].url)
        else:
            return "Error: No image data returned"

    except Exception as e:
        return f"Error generating image: {str(e)}"


@function_tool
def generate_image_with_metadata(
    prompt: str,
    size: Literal["1024x1024", "1024x1792", "1792x1024"] = "1024x1024",
    quality: Literal["standard", "hd"] = "standard",
    style: Literal["vivid", "natural"] = "vivid"
) -> dict:
    """
    Generate an image and return both URL and metadata.

    Args:
        prompt: The text prompt to generate an image from
        size: Size of the image (1024x1024, 1024x1792, or 1792x1024)
        quality: Quality of the image (standard or hd)
        style: Style of the image (vivid or natural)

    Returns:
        Dictionary with url, revised_prompt, and metadata
    """
    try:
        # Call DALL-E API
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality=quality,
            style=style,
            n=1
        )

        # Extract response data
        if response.data and len(response.data) > 0:
            image_data = response.data[0]
            return {
                "url": cast(str, image_data.url),
                "revised_prompt": getattr(image_data, 'revised_prompt', None),
                "size": size,
                "quality": quality,
                "style": style,
                "model": "dall-e-3"
            }
        else:
            return {
                "url": None,
                "error": "No image data returned",
                "revised_prompt": None
            }

    except Exception as e:
        return {
            "url": None,
            "error": str(e),
            "revised_prompt": None
        }