import smtplib
from email.message import EmailMessage

from config import Config


def send_status_email(to_email: str, note_title: str, status: str) -> bool:
    """
    Sends a note-approved / note-rejected email to the uploader.
    Returns True on success, False on failure (never raises — a failed
    email should never break the approve/reject request itself).
    """
    if not to_email:
        print("EMAIL SKIPPED: no recipient email on this note")
        return False

    if not Config.SMTP_USER or not Config.SMTP_PASSWORD:
        print("EMAIL SKIPPED: SMTP_USER / SMTP_PASSWORD not configured in .env")
        return False

    if status == "approved":
        subject = f'Your note "{note_title}" has been approved'
        body = (
            f'Good news! Your uploaded note "{note_title}" has been reviewed '
            f"and approved by the admin. It is now visible to everyone on "
            f"the All Notes page.\n\n"
            f"— Notes Sharing Website"
        )
    else:  # rejected
        subject = f'Your note "{note_title}" was not approved'
        body = (
            f'Your uploaded note "{note_title}" was reviewed by the admin '
            f"and was not approved. Please check the file and try uploading "
            f"again if you believe this was a mistake.\n\n"
            f"— Notes Sharing Website"
        )

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f"{Config.SMTP_FROM_NAME} <{Config.SMTP_USER}>"
    msg["To"] = to_email
    msg.set_content(body)

    try:
        with smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT) as server:
            server.starttls()
            server.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
            server.send_message(msg)
        print(f"EMAIL SENT: {status} notice to {to_email}")
        return True
    except Exception as err:
        print(f"EMAIL ERROR: could not send to {to_email}: {err}")
        return False
