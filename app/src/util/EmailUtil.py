import requests

EMAIL_API_KEY = "28088e5dce5be5ad7b7923fe8b60964e-69210cfc-2c1b9726"
EMAIL_API_URL = "https://api.mailgun.net/v3/sandbox599c19b194984900830ae3ce6b567dc5.mailgun.org"

class EmailUtil:
    
    def send_reset_password_email(email: str):
        return requests.post(
            EMAIL_API_URL+"/messages",
            auth=("api", EMAIL_API_KEY),
            data={
                "from": "Publisto <mailgun@sandbox599c19b194984900830ae3ce6b567dc5.mailgun.org>",
                "to": ["hkntgrl1928@gmail.com", email],
                "subject": "Reset Password",
                "text": "Your verification code: 348956"
            })
