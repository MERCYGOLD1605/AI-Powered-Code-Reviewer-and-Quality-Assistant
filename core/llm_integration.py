import os
from openai import OpenAI


def generate_ai_doc(code):
    api_key = os.getenv("OPENAI_API_KEY")

    # If no API key is found, return a fallback docstring
    if not api_key:
        return '''"""Generated Docstring

Args:
    params

Returns:
    result
"""'''

    try:
        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"Generate a professional Python docstring for:\n\n{code}"
                }
            ]
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f'''"""Fallback Docstring

AI generation failed:
{str(e)}

Args:
    params

Returns:
    result
"""'''