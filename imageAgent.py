import base64
from pathlib import Path
from uuid import uuid4

from openai import OpenAI

client = OpenAI()

AGENT_INSTRUCTIONS = """
You are a synthetic-image production agent.

Convert each request into a precise visual specification:
- subject and environment
- composition and camera angle
- lighting and color palette
- visual style
- important constraints

Always generate a new image. Avoid unwanted text, logos, watermarks,
and recognizable real people unless explicitly requested.
"""


def create_synthetic_image(
    brief: str,
    output_directory: str = "generated_images",
) -> dict:
    response = client.responses.create(
        model="gpt-5.5",
        instructions=AGENT_INSTRUCTIONS,
        input=f"Draw the following synthetic image:\n\n{brief}",
        tools=[
            {
                "type": "image_generation",
                "model": "gpt-image-2.5-flare",
                "action": "generate",
                "size": "1024x1024",
                "quality": "high",
                "background": "opaque",
            }
        ],
        # Ensures the request produces an image rather than only text.
        tool_choice={"type": "image_generation"},
    )

    image_calls = [
        item
        for item in response.output
        if item.type == "image_generation_call" and item.result
    ]

    if not image_calls:
        raise RuntimeError("The agent did not return an image.")

    image_call = image_calls[-1]

    directory = Path(output_directory)
    directory.mkdir(parents=True, exist_ok=True)

    output_path = directory / f"{uuid4().hex}.png"
    output_path.write_bytes(base64.b64decode(image_call.result))

    return {
        "path": str(output_path),
        "response_id": response.id,
        "revised_prompt": image_call.revised_prompt,
    }


if __name__ == "__main__":
    result = create_synthetic_image(
        """
        A photorealistic warehouse inspection scene containing three
        cardboard boxes on a conveyor belt. One box has a visibly crushed
        upper-left corner. Neutral background, overhead industrial lighting,
        camera positioned 2 meters away, no people, labels, or logos.
        """
    )

    print(result)