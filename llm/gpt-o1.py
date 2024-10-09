from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

base_url = "https://api.aimlapi.com/v1"

system_prompt = "Tu es un super agent ! "
user_prompt = "Comment vas-tu ? Combien fait 1+1 ?"

api = OpenAI(api_key = "addec44c7fd642b693c4ef21d1efa9af", base_url=base_url)

def main():
    completion = api.chat.completions.create(
        model="o1-mini",
        messages=[
            {"role": "user", "content": "Comment vas-tu ? Combien fait 1+1 ?"},
        ],
        max_tokens=256,
    )

    response = completion.choices[0].message.content

    # print("User:", user_prompt)
    print("AI:", completion)

# class LLM:
#     def __init__():
#         pass

#     def inference(input : str) -> str :
#         pass



if __name__ == '__main__':
    main()