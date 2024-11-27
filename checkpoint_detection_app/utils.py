
from cryptography.fernet import Fernet
import pywhatkit
import os
from datetime import datetime
from django.core.mail import EmailMessage
import glob
from industrial_safety_app import settings


import cv2
import os
# Usage


def extract_frames(video_path, output_dir, interval=1):
    # os.makedirs(output_dir, exist_ok=True)
    video = cv2.VideoCapture(video_path)
    fps = int(video.get(cv2.CAP_PROP_FPS))
    frame_count = 0
    saved_frame = 0

    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        # Save frame every 'interval' seconds
        if frame_count % (fps * interval) == 0:
            frame_name = f"frame_{saved_frame}.jpg"
            cv2.imwrite(os.path.join(output_dir, frame_name), frame)
            saved_frame += 1
        frame_count += 1

    video.release()
    print(f"Extracted {saved_frame} frames to {output_dir}")
    return

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
