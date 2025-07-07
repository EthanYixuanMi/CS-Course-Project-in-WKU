from datetime import datetime
import smtplib
from email.message import EmailMessage
import requests

def write_log(message):
    with open("log.txt", "a", encoding="utf-8") as file:
        file.write(f"{datetime.now()}: {message}\n")

def send_enrollment_email(to_email, message_body):
    # SMTP configuration for QQ email
    smtp_server = "smtp.qq.com"
    smtp_port = 587
    sender_email = "your_email_address@qq.com"
    sender_password = "your_password"

    msg = EmailMessage()
    msg['Subject'] = 'SmartCourse Enrollment Notification'
    msg['From'] = sender_email
    msg['To'] = to_email
    msg.set_content(message_body)

    smtp = smtplib.SMTP(smtp_server, smtp_port)
    smtp.starttls()
    smtp.login(sender_email, sender_password)
    smtp.send_message(msg)
    smtp.quit()

def send_grade_email(to_email, message_body):
    smtp_server = "smtp.qq.com"
    smtp_port = 587
    sender_email = "your_email_address@qq.com"
    sender_password = "your_password"

    msg = EmailMessage()
    msg['Subject'] = 'SmartCourse Grading Notification'
    msg['From'] = sender_email
    msg['To'] = to_email
    msg.set_content(message_body)

    smtp = smtplib.SMTP(smtp_server, smtp_port)
    smtp.starttls()
    smtp.login(sender_email, sender_password)
    smtp.send_message(msg)
    smtp.quit()


def ask_ai_question(prompt):
    # The model is using local deployment of deepseek-r1:1.5b, started by Ollama.
    try:
        # Send a request to the Ollama model running on localhost
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "deepseek-r1:1.5b",
                "prompt": prompt,
                "stream": False
            }
        )
        result = response.json()
        if "response" in result:
            # Only keep the answer part, discard the reasoning part
            full_text = result["response"]
            if "</think>" in full_text:
                return full_text.split("</think>")[-1].strip()
            else:
                return full_text.strip()
    except Exception as e:
        return f"AI model failed to respond: {e}"

