import pickle
from .utils import send_email, send_whatsapp_message, send_website_notification  # Assuming you have these functions

# Function to check all safety precautions
def check_safety(input_data):
    """
    Check all safety precautions using the five models.
    Returns a tuple (is_safe, violations).
    """
    violations = []

    # Predict for each safety item
    if not mask_model.predict([input_data])[0]:  # Assuming 0 = not detected, 1 = detected
        violations.append("Mask not detected")
    if not apron_model.predict([input_data])[0]:
        violations.append("Apron not detected")
    if not shoes_model.predict([input_data])[0]:
        violations.append("Shoes not detected")
    if not hand_gloves_model.predict([input_data])[0]:
        violations.append("Hand gloves not detected")
    if not helmet_model.predict([input_data])[0]:
        violations.append("Helmet not detected")

    # If no violations, safety is true
    is_safe = len(violations) == 0
    return is_safe, violations

# Function to handle the workflow
def process_safety_check(input_data, user_contact):
    """
    Process the safety check and take actions based on the results.
    input_data: The data to pass to the models for prediction.
    user_contact: Dictionary containing user contact info (email, phone, etc.).
    """
    # Check all safety precautions
    is_safe, violations = check_safety(input_data)

    if is_safe:
        # All precautions are met, redirect to success page
        return True, None  # True indicates safety precautions are not violated
    else:
        # Safety precautions violated, send notifications
        message = "Safety violation detected:\n" + "\n".join(violations)
        send_email("Safety Violation Alert", message, user_contact['email'])
        send_whatsapp_message(message, user_contact['phone'])
        send_website_notification(message)

        # Return False and violations
        return False, violations
