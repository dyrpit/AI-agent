import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")



def main():

    print("Hello from ai-agent!")

    if not api_key:
      raise RuntimeError("Missing api key for open router")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()


    messages = [
      {"role": "system", "content": system_prompt},
      {"role": "user", "content": args.user_prompt},
    ]

    client = OpenAI(
      base_url="https://openrouter.ai/api/v1",
      api_key=api_key,
    )

    for _ in range(20):
      response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
      )

      message = response.choices[0].message
      messages.append(message)
      
      if not message.tool_calls:
        print(message.content)
        break
      else:
        for tool_call in message.tool_calls:
          result_message = call_function(tool_call, verbose=args.verbose)
          messages.append(result_message)
          
          if not result_message["content"]:
            raise Exception("Empty content")
          
          if args.verbose:
            print(f"-> {result_message['content']}")
    
      usage = response.usage

      if usage == None:
          raise RuntimeError("OpenAi error, unable to get usage")
      else:
        if args.verbose:
          print(f"User prompt: {args.user_prompt}")
          print(f"Prompt tokens: {response.usage.prompt_tokens}")
          print(f"Response tokens: {response.usage.completion_tokens}")
    else:
      print("Error: agent hit the 20-iteration limit without producing a final response.")
      sys.exit(1)
          
    
        
    
    
  


if __name__ == "__main__":
    main()
