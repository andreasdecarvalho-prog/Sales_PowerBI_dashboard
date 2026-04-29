import smtplib
from email.message import EmailMessage
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

def send_data_email(files):
    """
    Send an email with given files attached.

    Args:
        files (list[Path]): List of file paths to attach.
    """

    from_address = os.getenv("FROM_ADDRESS")
    to_address = os.getenv("TO_ADDRESS")
    password = os.getenv("PASSWORD")

    msg = EmailMessage()
    msg["Subject"] = "ETL Data Delivery"
    msg["From"] = from_address
    msg["To"] = to_address
    msg.set_content(
        "Hello,\n\nAttached are the latest datasets:\n"
        "- Sales (CSV)\n- Dummy products (CSV)\n- Fakestore products (CSV)\n"
        "- Products database (SQLite)\n\n"
        "You can choose whether to use CSV or SQL.\n\nBest regards,\nAndreas"
    )

    # Attach each file
    for file in files:
        file = Path(file)
        with open(file, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="octet-stream",
                filename=file.name
            )

    # Send email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(from_address, password)
            server.send_message(msg)
        print("Email sent successfully to", to_address)
    except Exception as e:
        print("Failed to send email:", e)
