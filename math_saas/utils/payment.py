import razorpay
from math_saas.config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET

_client = None

def get_razorpay_client():
    global _client
    if _client is None:
        if not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET:
            raise RuntimeError("Razorpay keys not configured")
        _client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
    return _client
