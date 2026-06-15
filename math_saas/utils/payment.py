import uuid
import razorpay
from typing import Any, Dict, Optional
from razorpay.errors import SignatureVerificationError

from math_saas.config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET
from .typed_razorpay import TypedRazorpayClient


# -------------------------------------------------
# SINGLETON RAZORPAY CLIENT (TYPED)
# -------------------------------------------------
_client: Optional[TypedRazorpayClient] = None


def get_razorpay_client() -> TypedRazorpayClient:
    """
    Return a singleton Razorpay client.
    Ensures keys exist and prevents repeated client creation.
    """
    global _client

    if not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET:
        raise RuntimeError("Razorpay keys are not set in environment variables")

    if _client is None:
        raw_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        _client = raw_client  # type: ignore[assignment]

    assert _client is not None
    return _client


# -------------------------------------------------
# ORDER CREATION
# -------------------------------------------------
def create_order(
    amount_in_paise: int,
    receipt: str,
    notes: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a Razorpay order.
    Ensures:
    - amount is integer
    - amount >= 100 paise
    - notes are stringified
    - receipt <= 40 chars (Razorpay requirement)
    """

    # --- Validate amount ---
    if not isinstance(amount_in_paise, int):
        raise ValueError("amount_in_paise must be an integer")

    if amount_in_paise < 100:
        raise ValueError("amount_in_paise must be >= 100 paise")

    # --- Ensure notes are strings ---
    safe_notes = {str(k): str(v) for k, v in (notes or {}).items()}

    # --- Ensure receipt <= 40 chars ---
    if len(receipt) > 40:
        receipt = f"rcpt_{uuid.uuid4().hex[:20]}"

    client = get_razorpay_client()

    return client.order.create({
        "amount": amount_in_paise,
        "currency": "INR",
        "receipt": receipt,
        "payment_capture": 1,
        "notes": safe_notes,
    })


# -------------------------------------------------
# SIGNATURE VERIFICATION
# -------------------------------------------------
def verify_payment_signature(
    order_id: str,
    payment_id: str,
    signature: str
) -> bool:
    """
    Verify Razorpay payment signature.
    Returns True if valid, False otherwise.
    """

    client = get_razorpay_client()

    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature,
        })
        return True

    except SignatureVerificationError:
        return False
