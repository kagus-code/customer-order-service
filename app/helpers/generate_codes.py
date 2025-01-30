import datetime
import secrets
import uuid

from django.apps import apps


def generate_unique_customer_code():
    """Generates a unique customer code in the format CYYYYMM-RANDOM."""
    today = datetime.date.today()
    date_prefix = today.strftime("C%Y%m")  # Example: C202501

    while True:
        random_part = secrets.token_hex(4).upper()  # Generates 8-character hex
        code = f"{date_prefix}-{random_part}"

        # Check uniqueness
        Customer = apps.get_model("customerorders", "Customer")
        if not Customer.objects.filter(code=code).exists():
            return code


def generate_unique_code():
    return str(uuid.uuid4())[:8]
