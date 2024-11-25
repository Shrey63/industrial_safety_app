
from cryptography.fernet import Fernet
import pywhatkit
import os
from datetime import datetime
from django.core.mail import EmailMessage

from industrial_safety_app import settings

VIOLATION_MESSAGES = {
    "mask": {
        "email_subject": "⚠️ Safety Alert: Mask Missing",
        "email_message": (
            "⚠️ Safety Alert: Mask Missing\n\n"
            "A safety violation has been detected: Mask is missing.\n"
            "Importance: Masks provide crucial protection against airborne particles, "
            "chemicals, and dust. Not wearing a mask can lead to serious health risks such as respiratory problems, "
            "allergic reactions, or exposure to harmful substances.\n\n"
            "Action Required: Please ensure compliance immediately to maintain a safe working environment."
        ),
        "whatsapp_caption": (
            "⚠️ Safety Alert: Mask Missing\n"
            "A mask violation has been detected. Masks are vital to protect against dust and harmful chemicals. "
            "Ensure compliance immediately to avoid health risks such as respiratory issues or allergic reactions."
        ),
    },
    "shoes": {
        "email_subject": "⚠️ Safety Alert: Safety Shoes Missing",
        "email_message": (
            "⚠️ Safety Alert: Safety Shoes Missing\n\n"
            "A safety violation has been detected: Safety shoes are missing.\n"
            "Importance: Safety shoes prevent injuries from sharp objects, falling items, and slippery surfaces. "
            "Without proper footwear, there is a high risk of foot injuries, fractures, or slipping accidents.\n\n"
            "Action Required: Please ensure compliance immediately to maintain a safe working environment."
        ),
        "whatsapp_caption": (
            "⚠️ Safety Alert: Safety Shoes Missing\n"
            "A violation has been detected: Safety shoes are essential to prevent foot injuries and slipping accidents. "
            "Ensure compliance immediately to avoid serious risks."
        ),
    },
    "gloves": {
        "email_subject": "⚠️ Safety Alert: Gloves Missing",
        "email_message": (
            "⚠️ Safety Alert: Gloves Missing\n\n"
            "A safety violation has been detected: Gloves are missing.\n"
            "Importance: Gloves protect hands from cuts, burns, and chemical exposure. "
            "Working without gloves can lead to severe hand injuries, contamination, or long-term skin damage.\n\n"
            "Action Required: Please ensure compliance immediately to maintain a safe working environment."
        ),
        "whatsapp_caption": (
            "⚠️ Safety Alert: Gloves Missing\n"
            "A violation has been detected: Gloves are vital to protect against cuts, burns, and harmful chemicals. "
            "Ensure compliance immediately to avoid serious risks."
        ),
    },
    "apron": {
        "email_subject": "⚠️ Safety Alert: Apron Missing",
        "email_message": (
            "⚠️ Safety Alert: Apron Missing\n\n"
            "A safety violation has been detected: Apron is missing.\n"
            "Importance: Aprons safeguard against spills, splashes, and chemical burns. "
            "Not wearing an apron increases the risk of skin irritation or severe burns from hazardous materials.\n\n"
            "Action Required: Please ensure compliance immediately to maintain a safe working environment."
        ),
        "whatsapp_caption": (
            "⚠️ Safety Alert: Apron Missing\n"
            "A violation has been detected: Aprons protect against spills and chemical burns. "
            "Ensure compliance immediately to avoid potential injuries."
        ),
    },
    "helmet": {
        "email_subject": "⚠️ Safety Alert: Helmet Missing",
        "email_message": (
            "⚠️ Safety Alert: Helmet Missing\n\n"
            "A safety violation has been detected: Helmet is missing.\n"
            "Importance: Helmets are critical for head protection against falling objects, impacts, and head injuries. "
            "Not wearing a helmet can lead to severe head trauma, fractures, or life-threatening injuries.\n\n"
            "Action Required: Please ensure compliance immediately to maintain a safe working environment."
        ),
        "whatsapp_caption": (
            "⚠️ Safety Alert: Helmet Missing\n"
            "A violation has been detected: Helmets are crucial for head protection. "
            "Ensure compliance immediately to avoid severe head injuries or trauma."
        ),
    },
}


def send_email(subject, message, recipient,path):
    """Send email notifications."""
    try:
        email = EmailMessage(
            subject,
            message,
            from_email='srushti.johari@cumminscollege.in',
            to=[recipient],
        )


        # Attach the image
        with open(path, 'rb') as f:
            email.attach(os.path.basename(path), f.read(), 'image/jpeg')

        # Send the email
        email.send(fail_silently=False)
        print(f"Email sent to {recipient}")

    except Exception as e:
        print(f"Error sending email: {e}")


def encrypt_recipient(recipient, key):
    """Encrypt the recipient string."""
    fernet = Fernet(key)
    encrypted = fernet.encrypt(recipient.encode())
    return encrypted


def decrypt_recipient(encrypted_recipient, key):
    """Decrypt the recipient string."""
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_recipient).decode()
    return decrypted


def get_current_time():
    """Get the current time for scheduling messages."""
    current_time = datetime.now()
    hour = current_time.hour
    minute = current_time.minute + 1  # Schedule message for the next minute
    return hour, minute


def generate_key():
    """Generate an encryption key."""
    return Fernet.generate_key()


def send_whatsapp_message(recipient, caption, image_filename, key):
    """Send WhatsApp notification."""
    try:
        # Decrypt the recipient before using it
        decrypted_recipient = decrypt_recipient(recipient, key)

        # Get the current time for sending the message
        hour, minute = get_current_time()

        # Build the path to the static image
        image_path = os.path.join(settings.BASE_DIR, 'industrial_safety_app', 'static', 'industrial_safety_app',
                                  image_filename)

        # Send the WhatsApp image with the caption
        pywhatkit.sendwhats_image(decrypted_recipient, image_path, caption, hour, minute)

        print(f"WhatsApp image sent to {decrypted_recipient} with caption: {caption}")

    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")
