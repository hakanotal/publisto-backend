from email.message import EmailMessage
import ssl
import smtplib
import os

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

class EmailUtil:
    
    def send_reset_password_email(email_receiver: str):
        
        SUBJECT = "Reset Password"
        BODY = "Your verification code: 348956"
        BCC = ["otal18@itu.edu.tr", "cetini18@itu.edu.tr", "karagozh18@itu.edu.tr"]
        
        msg = EmailMessage()
        msg['from'] = EMAIL_SENDER
        msg['to'] = email_receiver
        msg['bcc'] = ", ".join(BCC)
        msg['subject'] = SUBJECT
        msg.set_content(BODY)

        ctx = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

        
