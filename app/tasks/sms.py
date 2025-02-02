import africastalking
from celery import shared_task
from decouple import config

africastalking.initialize(
    config("AFRICASTALKING_USERNAME"), config("AFRICASTALKING_API_KEY")
)

sms = africastalking.SMS


@shared_task
def send_sms_notification(phone_number, message):
    """
    Sends an SMS notification using Africa's Talking API.

    Args:
        phone_number (str): Recipient's phone number (e.g., "+254701234567").
        message (str): SMS message content.
    Returns:
        dict: API response
    """
    try:
        formatted_phone = (
            f"+{phone_number}"
            if not phone_number.startswith("+")
            else phone_number
        )
        response = sms.send(message, [formatted_phone])
        return response
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return None
