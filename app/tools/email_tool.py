import uuid


class EmailTool:
    def send_email(self, to_email: str, subject: str, body: str):
        return {
            "success": True,
            "message_id": f"msg_{uuid.uuid4().hex[:8]}",
            "to": to_email,
            "subject": subject,
        }