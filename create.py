from openai import OpenAI
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import anthropic
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

# Set the API keys
openai_api_key = 'sk-key'
anthropic_api_key = 'sk-ant-key'
mistral_api_key = 'key'
openrouter_api_key = 'sk-key'

# Set the directory for posts
learn_dir = '/directory/email'

def query_gpt_api(prompt):
    """
    Query the GPT API using the provided prompt.

    Args:
        prompt (str): The prompt to send to the GPT API.

    Returns:
        str: The generated response from the GPT API.
    """
    client = OpenAI(api_key=openai_api_key)
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="gpt-4-0125-preview",
    )
    return chat_completion.choices[0].message.content

def query_claude(prompt):
    """
    Query the Claude API using the provided prompt.

    Args:
        prompt (str): The prompt to send to the Claude API.

    Returns:
        str: The generated response from the Claude API.
    """
    client = anthropic.Anthropic(api_key=anthropic_api_key)
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text

def query_mistral(prompt):
    """
    Query the Mistral API using the provided prompt.

    Args:
        prompt (str): The prompt to send to the Mistral API.

    Returns:
        str: The generated response from the Mistral API.
    """
    client = MistralClient(api_key=mistral_api_key)
    messages = [ChatMessage(role="user", content=prompt)]
    chat_response = client.chat(
        model='mistral-large-latest',
        messages=messages,
    )
    return chat_response.choices[0].message.content

def query_cmdr(prompt):
    """
    Query the CMDR API using the provided prompt.

    Args:
        prompt (str): The prompt to send to the CMDR API.

    Returns:
        str: The generated response from the CMDR API.
    """
    openrouter = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=openrouter_api_key)
    completion = openrouter.chat.completions.create(
        model="cohere/command-r",
        messages=[{"role": "user", "content": prompt}],
    )
    return completion.choices[0].message.content

def write_to_file(data, name, day):
    """
    Write the provided data to a file with the specified name and day.

    Args:
        data (str): The data to write to the file.
        name (str): The name to include in the filename.
        day (str): The day to include in the filename.
    """
    filename = f"{learn_dir}/{name}-{day}.md"
    with open(filename, 'w') as file:
        file.write(str(data))

def main():
    """
    The main function that orchestrates the post generation process.
    """
    with open(f"/directory/prompt.txt", 'r') as file:
        base_prompt = file.read().strip()
    with open('/directory/topiclist.txt', 'r') as file:
        lessons = file.read().strip()

# if you're going to send out a daily email, pick your start date here:
    day = '2024-05-15'
    dayx = datetime.strptime(day, '%Y-%m-%d')
    prior = "This is the first email on the 30 days of lessons."

    for line in lessons.splitlines():
        print(day + ": " + line)
        prompt = base_prompt + "\n\n" + line + "\n\n" + prior
        post1 = query_mistral(prompt)

        dcheck = "Double check the work of your competitor. I will provide the prompt and the output. Rewrite the output based upon the prompt and output to make it better. Make sure to properly format text in markdown and use bullets for better readability.\n\n"
        dcheck += "# PROMPT: \n\n" + prompt
        dcheck += "# OUTPUT: \n\n" + post1
        dcheck += "# YOUR IMPROVED VERSION: \n\n"

        final = query_claude(dcheck)
        write_to_file(final, "Topic-" + line, day)

        next_day = dayx + timedelta(days=1)
        day = next_day.strftime('%Y-%m-%d')
        dayx = datetime.strptime(day, '%Y-%m-%d')

if __name__ == "__main__":
    main()
