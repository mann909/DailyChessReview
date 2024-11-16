import vonage
from dotenv import load_dotenv
import os

load_dotenv()

# Replace these with your own API key and secret
api_key = os.getenv('VONAGE_API_KEY')
api_secret = os.getenv('VONAGE_API_SECRET')
phone=os.getenv('MY_PHONE_NUMBER')

def sendSms(msg):
    client = vonage.Client(key=api_key, secret=api_secret)
    sms = vonage.Sms(client)

    responseData = sms.send_message(
        {
            "from": "Mann's Chess Review System",
            "to": str(phone),
            "text": msg,
        }
    )

    if responseData["messages"][0]["status"] == "0":
        print("Message sent successfully.")
    else:
        print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
