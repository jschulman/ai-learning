```markdown
# Daily Lesson Email Generator

This project consists of two Python scripts that work together to generate and send daily lesson emails. 

## Usage

1. Create a list of daily topics and place into the topics.txt file.
2. Update the prompt.txt to fit your topic and lessons you desire.
3. Follow the configuration steps below.
3. Run the create.py and it will show you lesson by lesson as it goes through your entire lesson set.

## Prerequisites

Before running the scripts, make sure you have the following dependencies installed:

- Python 3.x
- `openai` library
- `anthropic` library
- `mistralai` library
- `mistune` library

You can install the required libraries using pip:

```
pip install openai anthropic mistralai mistune
```

## Configuration

Before running the scripts, make sure to configure the following variables:

- `openai_api_key`: Your OpenAI API key.
- `anthropic_api_key`: Your Anthropic API key.
- `mistral_api_key`: Your Mistral API key.
- `openrouter_api_key`: Your OpenRouter API key.
- `SMTP_SERVER`: The SMTP server for sending emails.
- `SMTP_PORT`: The SMTP port for sending emails.
- `RECIPIENT_EMAIL`: The email address of the recipient.
- `lesson_dir`: The directory where the generated blog posts will be saved.
- `directory`: The directory where the files are located.

## Scripts

### 1. `create.py`

This script generates lessons using various AI APIs. It reads a base prompt from a file, retrieves lesson topics from another file, and generates posts for each topic using the Mistral and Claude APIs. The generated lessons are then saved as Markdown files in the specified directory.

### 2. `daily-email.py`

This script sends a daily email to the specified recipient. It searches for an email file with the current date in the specified directory, reads the content of the file, converts it from Markdown to HTML, and sends the email using the configured SMTP server.

It is recommended to use this script via Cron or another scheduler.

## License

This project is licensed under the [MIT License](LICENSE).
```

This README file provides an overview of your project, including the purpose of the scripts, prerequisites, configuration instructions, and usage guidelines. It also includes information about the required dependencies and how to install them using pip.

Make sure to replace the placeholders for API keys, SMTP server details, and directory paths with your actual values.
