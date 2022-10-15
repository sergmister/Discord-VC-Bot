import os
import openai
# requires pip install python-dotenv
from dotenv import load_dotenv
load_dotenv()


def parse(input, temp=0.5, max_tokens=30, tone="mean-spirited", voice="informal"):
    # Load your API key from an environment variable or secret management service
    openai.api_key = os.environ.get("gpt-api-key")

    responseJSON = openai.Completion.create(
        model="text-curie-001", prompt="create an " + voice + " and " + tone + " response to the following text: " + input, temperature=temp, max_tokens=max_tokens)

    responseText = responseJSON.get("choices")[0].get("text")
    return(responseText)


print(parse("what is 9 + 10",
      tone="agressively hostile", voice="slang-filled"))
