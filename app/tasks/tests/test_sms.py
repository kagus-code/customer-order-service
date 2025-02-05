from unittest.mock import patch

import pytest

from app.tasks.sms import send_sms_notification  # Replace with the actual path


@pytest.mark.django_db
class TestSendSmsNotification:

    @patch(
        "africastalking.SMSService.send"
    )  # Mock the Africa's Talking API send method
    def test_send_sms_notification_success(self, mock_send_sms):
        # Define the mock response that we expect from Africa's Talking API
        mock_response = {
            "SMSMessageData": {"Recipients": [{"status": "Success"}]}
        }
        mock_send_sms.return_value = mock_response

        # Call the send_sms_notification function
        phone_number = "+254701234567"
        message = "Test message"
        response = send_sms_notification(phone_number, message)

        # Assert the mock send method was called with the correct arguments
        mock_send_sms.assert_called_once_with(message, [phone_number])

        # Assert that the response from the function matches the mock response
        assert response == mock_response

    @patch("africastalking.SMSService.send")
    def test_send_sms_notification_no_plus_prefix(self, mock_send_sms):
        # Define the mock response
        mock_response = {
            "SMSMessageData": {"Recipients": [{"status": "Success"}]}
        }
        mock_send_sms.return_value = mock_response

        # Call the send_sms_notification function without the '+' in the phone number
        phone_number = "254701234567"  # No '+' at the beginning
        message = "Test message"
        response = send_sms_notification(phone_number, message)

        # Assert the mock send method was called with the formatted phone number
        mock_send_sms.assert_called_once_with(message, ["+254701234567"])

        # Assert the response matches the mock response
        assert response == mock_response

    @patch("africastalking.SMSService.send")
    def test_send_sms_notification_exception(self, mock_send_sms):
        # Simulate an error by making the mock raise an exception
        mock_send_sms.side_effect = Exception("Error sending SMS")

        # Call the send_sms_notification function
        phone_number = "+254701234567"
        message = "Test message"
        response = send_sms_notification(phone_number, message)

        # Assert the response is None in case of error
        assert response is None

    @patch("africastalking.SMSService.send")
    def test_send_sms_notification_without_plus_prefix(self, mock_send_sms):
        # Define the mock response
        mock_response = {
            "SMSMessageData": {"Recipients": [{"status": "Success"}]}
        }
        mock_send_sms.return_value = mock_response

        # Call the send_sms_notification function with a phone number missing the '+' prefix
        phone_number = "254701234567"  # Phone number without '+'
        message = "Test message"
        response = send_sms_notification(phone_number, message)

        # Assert the phone number was formatted correctly by the function
        mock_send_sms.assert_called_once_with(message, ["+254701234567"])

        # Assert the correct response was returned
        assert response == mock_response
