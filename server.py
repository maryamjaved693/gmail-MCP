from mcp.server.fastmcp import FastMCP
import resend
import os
import sys
import traceback

# 🔹 HARD-CODED RESEND API KEY (replace with your actual key)
RESEND_API_KEY = "re_M7h9ZtTN_JPQAHHpwSPwxWAM1Mft8HMRv"  # <-- your real API key

# MCP server config
PORT = os.environ.get("PORT", 10000)
mcp = FastMCP("Resend Email Server", host="0.0.0.0", port=PORT)

# Store last sent emails in memory
sent_emails_log = []


@mcp.tool()
def send_email(subject: str, to: str, from_email: str = None, content: str = "", text_content: str = None) -> str:
    """Sends an email using the Resend API and logs it locally."""
    try:
        resend.api_key = RESEND_API_KEY
        if not resend.api_key or not resend.api_key.startswith("re_"):
            return "❌ Invalid or missing hardcoded Resend API key."

        # Force verified sender if Gmail/Yahoo detected
        verified_sender = "onboarding@resend.dev"
        if not from_email or from_email.lower().endswith("@gmail.com") or from_email.lower().endswith("@yahoo.com"):
            from_email = verified_sender

        params = {
            "bcc": [],
            "cc": [],
            "from": from_email,
            "reply_to": [],
            "subject": subject,
            "to": [to],
            "html": content,
            "text": text_content or "This is the plain text version of the email."
        }

        try:
            email = resend.Emails.send(params)
        except Exception as resend_err:
            return f"❌ Resend API call failed: {resend_err}"

        # Log the sent email in memory
        sent_emails_log.append({
            "subject": subject,
            "to": to,
            "from": from_email,
            "content": content
        })

        if len(sent_emails_log) > 5:
            sent_emails_log.pop(0)

        return f"✅ Email sent successfully from {from_email}"

    except ImportError as e:
        return f"❌ Import error: {e}. Make sure 'resend' package is installed."

    except Exception as e:
        return f"❌ Email sending failed: {str(e)}\n{traceback.format_exc()}"


@mcp.tool()
def get_last_emails() -> str:
    """Returns the last 5 sent emails."""
    if not sent_emails_log:
        return "ℹ️ No emails have been sent yet."

    result = "📧 Last Sent Emails:\n"
    for idx, email in enumerate(sent_emails_log[-5:], start=1):
        result += (
            f"\n{idx}. To: {email['to']}\n"
            f"   Subject: {email['subject']}\n"
            f"   From: {email['from']}\n"
        )
    return result


def run_test_email():
    """Send a test email without starting MCP server."""
    resend.api_key = RESEND_API_KEY
    try:
        response = resend.Emails.send({
            "bcc": [],
            "cc": [],
            "from": "onboarding@resend.dev",
            "reply_to": [],
            "subject": "Test Email Direct Run",
            "to": ["maryamrao01@gmail.com"],
            "html": "<p>This is a test email sent directly without Cursor.</p>",
            "text": "This is a test email."
        })
        print("✅ Test email sent successfully:", response)
    except Exception as e:
        print("❌ Test email failed:", e)


if __name__ == "__main__":
    # If you want to run a test email in terminal
    if "--test" in sys.argv:
        run_test_email()
        sys.exit(0)

    # Otherwise start MCP server for Cursor
    mcp.run(transport="stdio")
