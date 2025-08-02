from openai import OpenAI

def analyze_conversation(messages, api_key):
    client = OpenAI(api_key=api_key)

    # Prepare conversation text
    conversation_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])

    prompt = f"""
    Analyze this conversation with a young adult (22–28) exploring life direction:

    {conversation_text}

    Provide:
    1. Summary (max 100 words, casual tone)
    2. Sentiment Analysis (emotions: optimistic, anxious, confused, determined, reflective, etc.)
    3. Strengths identified or shown
    4. Areas for growth/improvement
    5. Unique capabilities they might leverage
    6. One specific thing they seem naturally good at

    Format as JSON:
    {{
        "summary": "...",
        "emotions": ["emotion1", "emotion2"],
        "strengths": ["strength1", "strength2"],
        "growth_areas": ["area1", "area2"],
        "unique_capabilities": ["capability1"],
        "natural_talent": "..."
    }}
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # More cost-effective than GPT-4
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content
