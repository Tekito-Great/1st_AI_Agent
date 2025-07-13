import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types
from constant import *
from functions.get_files_info import *
from call_functions import *



load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    
    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if len(sys.argv) < 2:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    user_prompt = " ".join(args)

    if verbose:
        print (f"User prompt: {user_prompt}")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]



    generate_content(client, messages, verbose,available_functions)


def generate_content(client, messages, verbose,available_functions):
    response = client.models.generate_content(
        model = "gemini-2.0-flash-001",
        contents = messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt),
    )

    print("Response:")
    
    if verbose:
        print (F"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print (F"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    if not response.function_calls:
        return response.text
        
    for call in response.function_calls:
        function_call_result = call_function(call, verbose = verbose)
        # エラーハンドリング: .parts[0].function_response.response が存在しない場合
        try:
            response_data = function_call_result.parts[0].function_response.response
        except (AttributeError, IndexError) as e:
            raise RuntimeError("Fatal: No valid function response returned from call_function") from e
        
        # verbose の場合、結果を表示
        if verbose:
            print(f"-> {response_data}")
    
        print("**********************************************")
        print(f"CHECK1 call.name :{call.name}")
        print(f"CHECK2 call.arg  :{call.args}")
        print(f"CHECK3 call      :{call}")



  


if __name__ == "__main__":
    main()
