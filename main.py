import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types
from constant import *
from functions.get_files_info import schema_get_files_info


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    
    verbose = "--verbose" in sys.argv
    flag = ""

    if len(sys.argv) < 2:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    user_prompt = " ".join(sys.argv[1:])

    if verbose:
        print (f"User prompt: {user_prompt}")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model = "gemini-2.0-flash-001",
        contents = messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )

    print("Response: ")
    if not response.function_calls == None:
        print (f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(response.text)

    if verbose:
        print (F"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print (F"Response tokens: {response.usage_metadata.candidates_token_count}")
    
if __name__ == "__main__":
    main()
