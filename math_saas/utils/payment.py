import razorpay
from razorpay.errors import SignatureVerificationError  # type: ignore
from math_saas.config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET

_client = None

def get_razorpay_client():
    global _client
    if _client is None:
        _client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
    return _client


def create_order(amount_in_paise: int, receipt: str, notes=None):
    client = get_razorpay_client()
    return client.order.create(   # type: ignore
        {
            "amount": amount_in_paise,
            "currency": "INR",
            "receipt": receipt,
            "payment_capture": 1,
            "notes": notes or {},
        }
    )


def verify_payment_signature(order_id: str, payment_id: str, signature: str) -> bool:
    client = get_razorpay_client()
    try:
        client.utility.verify_payment_signature(   # type: ignore
            {
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
            }
        )
        return True
    except SignatureVerificationError:  # type: ignore
        return False
