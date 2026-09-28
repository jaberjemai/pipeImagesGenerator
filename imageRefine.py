response = client.responses.create(
    model="gpt-5.5",
    previous_response_id=result["response_id"],
    input="Edit the image: make the crushed corner more pronounced.",
    tools=[
        {
            "type": "image_generation",
            "model": "gpt-image-2.5-sunburst",
            "action": "edit",
            "quality": "high",
        }
    ],
    tool_choice={"type": "image_generation"},
)