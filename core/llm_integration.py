from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_ai_doc(code):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": f"Generate docstring:\n{code}"}]
        )
        return response.choices[0].message.content.strip()
    except:
        return '''"""Fallback docstring.

Args:
    params

Returns:
    result
"""'''