import resend
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set your API key
resend.api_key = os.getenv("RESEND_API")

try:
    # Send a test email
    params = {
        "from": "maryamjaved043@gmail.com",  # must be verified in Resend
        "to": ["maryamrao01@gmail.com"],     # recipient
        "subject": "Test Email from Resend",
        "html": "<p>Hello! This is a test email directly from Python.</p>",
    }

    email = resend.Emails.send(params)
    print("✅ Email sent successfully:", email)
except Exception as e:
    print("❌ Failed to send email:", e)
