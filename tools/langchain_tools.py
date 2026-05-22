from langchain.tools import tool

@tool
def send_email(recipient: str, body: str):
    return {
        "status": "sent",
        "recipient": recipient,
        "body": body
    }