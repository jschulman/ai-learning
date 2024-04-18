import os
import re
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import mistune

# Create a Markdown instance
markdown = mistune.create_markdown()

# SMTP server configuration
SMTP_SERVER = 'yourmailserver'
SMTP_PORT = 25
RECIPIENT_EMAIL = 'youremail@domain.com'
SENDER_EMAIL = 'youremail@domain.com'

# Directory path for email files
directory = "/directory/email"

# Get the current date formatted as 'Monday, April 01, 2025'
date = datetime.now().strftime('%A, %B %d, %Y')

def send_email(html_content):
    """
    Send an email with the provided HTML content.

    Args:
        html_content (str): The HTML content of the email.
    """
    # Image path for the header image
    image_path = '/directory/header.png'

    # Create the email message with the API response
    msg = MIMEMultipart('related')
    msg['Subject'] = f"Daily Lessons for {date}."
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg.preamble = 'This is a multi-part message in MIME format.'

    # Create an alternative part for the message body
    msg_alternative = MIMEMultipart('alternative')
    msg.attach(msg_alternative)

    # Attach HTML content with reference to the header image's CID
    html_content_with_header_image = f"""\
    <html>
      <head></head>
      <body>
        <img src="cid:header_image" style="width: 600px; height: auto;">
        {html_content}
      </body>
    </html>
    """
    msg_html = MIMEText(html_content_with_header_image, 'html')
    msg_alternative.attach(msg_html)

    # Add the header image
    with open(image_path, 'rb') as image_file:
        msg_image = MIMEImage(image_file.read())

    # Define the image's ID
    msg_image.add_header('Content-ID', '<header_image>')
    msg.attach(msg_image)

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()  # Upgrade the connection to secure
        smtp.sendmail(f"Daily Lessons <{SENDER_EMAIL}>", RECIPIENT_EMAIL, msg.as_string())

def main():
    """
    The main function that finds the email file for the current date and sends the email.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    pattern = re.compile(r"(\d{4}-\d{2}-\d{2})")

    file_path = None
    for file_name in os.listdir(directory):
        match = pattern.search(file_name)
        if match:
            date_str = match.group(1)
            if date_str == today:
                file_path = os.path.join(directory, file_name)
                break

    if file_path:
        with open(file_path, 'r') as file:
            email = file.read().strip()
        email_fm = markdown(email)
        send_email(email_fm)
    else:
        print(f"No email file found for today's date: {today}")

if __name__ == "__main__":
    main()
