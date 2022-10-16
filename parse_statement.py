import os
import openai

# requires pip install python-dotenv
from dotenv import load_dotenv

load_dotenv()


def parse(input, temp=0.5, max_tokens=100, tone="nice", voice="informal"):
    # Load your API key from an environment variable or secret management service
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    responseJSON = openai.Completion.create(
        model="text-davinci-002",
        prompt="create an " + voice + " and " + tone + " response to the following text: " + input,
        temperature=temp,
        max_tokens=max_tokens,
    )

    responseText = responseJSON.get("choices")[0].get("text")
    return responseText
