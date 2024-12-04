import cv2
from cryptography.fernet import Fernet
import pywhatkit
import os
from datetime import datetime
from django.core.mail import EmailMessage
import glob
from industrial_safety_app import settings

glist={
    "alternator_nameplate",
    "battery",
    "cabel_entry_holes",
    "control_panel_bidding",
    "control_panel_number",
    "control_panel_qr",
    "coolant_tank",
    "cpcb_sticker",
    "danger_sticker",
    "do_and_dont_sticker",
    "document_folder",
    "door_bidding",
    "door_handle",
    "door_stopper",
    "earthing_stud",
    "earthing_wire",
    "efficient_power_sticker",
    "emergency_button",
    "engine_numberplate",
    "exhaust_pipe",
    "foam_sheets",
    "fuel_gauge",
    "fuel_tank",
    "genset_nameplate",
    "hinges",
    "lifting_hook",
    "mahindra_sticker",
    "mcb_sticker",
    "ok_tested",
    "phone_number",
    "powerol_sticker",
    "raingaurd",
    "shyam_global_sticker",
    "warning_sticker",
    "water_oil_level_check_sticker",
    "yellow_mark"
}
tasks = [
    {
        "model_name": "Helmet Detection",
        "detection_keyword": "no-helmet",
        "model_path": r'..\..\pt\helmet.pt',
    },
    {
        "model_name": "Shoes Detection",
        "detection_keyword": "no-shoes",
        "model_path": r'..\..\pt\shoes.pt',
    }
]

VIOLATION_MESSAGES = {
    "no-mask": {
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
    "no-shoes": {
        "email_subject": "⚠️ Safety Alert: Safety Shoes Missing",
        "email_message": (
            "⚠️ Safety Alert: Safety Shoes Missing\n\n"
            "A safety violation has been detected: Safety shoes are missing.\n"
            "Importance: Safety shoes prevent injuries from sharp objects"
            ", falling items, and slippery surfaces. "
            "Without proper footwear, there is a high risk of foot injuries, fractures, or slipping accidents.\n\n"
            "Action Required: Please ensure compliance immediately to maintain a safe working environment."
        ),
        "whatsapp_caption": (
            "⚠️ Safety Alert: Safety Shoes Missing\n"
            "A violation has been detected: Safety shoes are essential to prevent foot injuries and slipping accidents. "
            "Ensure compliance immediately to avoid serious risks."
        ),
    },
    "no-gloves": {
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
    "no-apron": {
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
    "no-helmet": {
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


def get_latest_image(folder_name):
    # Get all files in the folder
    folder_path = os.path.join(settings.MEDIA_ROOT, folder_name)
    files = glob.glob(os.path.join(folder_path, "*.*"))
    # Ensure files exist before finding the latest one
    if not files:
        raise FileNotFoundError(f"No files found in the folder: {os.path.abspath(folder_path)}")
    # Return the latest file path
    return max(files, key=os.path.getmtime)

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
