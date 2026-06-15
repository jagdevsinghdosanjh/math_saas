import uuid
import razorpay
from typing import Any, Dict, Optional
from razorpay.errors import SignatureVerificationError

from math_saas.config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET


# -------------------------------------------------
# SINGLETON RAZORPAY CLIENT
# -------------------------------------------------
_client: Optional[razorpay.Client] = None


def get_razorpay_client() -> razorpay.Client:
    """
    Return a singleton Razorpay client.
    Ensures keys exist and prevents repeated client creation.
    """
    global _client

    if not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET:
        raise RuntimeError("Razorpay keys are not set in environment variables")

    if _client is None:
        _client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

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
    safe_notes = {}
    if notes:
        safe_notes = {str(k): str(v) for k, v in notes.items()}

    # --- FIX: Ensure receipt <= 40 chars ---
    if len(receipt) > 40:
        # Short, unique, Razorpay-safe fallback
        receipt = f"rcpt_{uuid.uuid4().hex[:20]}"

    client = get_razorpay_client()

    order = client.order.create(
        {
            "amount": amount_in_paise,
            "currency": "INR",
            "receipt": receipt,
            "payment_capture": 1,
            "notes": safe_notes,
        }
    )

    return order


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
        client.utility.verify_payment_signature(
            {
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
            }
        )
        return True

    except SignatureVerificationError:
        return False

# import uuid
# import razorpay
# from typing import Any, Dict, Optional
# from razorpay.errors import SignatureVerificationError  # type: ignore

# from math_saas.config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET


# # -------------------------------------------------
# # SINGLETON RAZORPAY CLIENT
# # -------------------------------------------------
# _client: Optional[razorpay.Client] = None


# def get_razorpay_client() -> razorpay.Client:
#     """
#     Return a singleton Razorpay client.
#     Ensures keys exist and prevents repeated client creation.
#     """
#     global _client

#     if not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET:
#         raise RuntimeError("Razorpay keys are not set in environment variables")

#     if _client is None:
#         _client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

#     return _client


# # -------------------------------------------------
# # ORDER CREATION
# # -------------------------------------------------
# def create_order(
#     amount_in_paise: int,
#     receipt: str,
#     notes: Optional[Dict[str, Any]] = None
# ) -> Dict[str, Any]:
#     """
#     Create a Razorpay order.
#     Ensures:
#     - amount is integer
#     - amount >= 100 paise
#     - notes are stringified
#     - receipt <= 40 chars (Razorpay requirement)
#     """

#     # --- Validate amount ---
#     if not isinstance(amount_in_paise, int):
#         raise ValueError("amount_in_paise must be an integer")

#     if amount_in_paise < 100:
#         raise ValueError("amount_in_paise must be >= 100 paise")

#     # --- Ensure notes are strings ---
#     safe_notes = {}
#     if notes:
#         safe_notes = {str(k): str(v) for k, v in notes.items()}

#     # --- FIX: Ensure receipt <= 40 chars ---
#     if len(receipt) > 40:
#         # Short, unique, Razorpay-safe fallback
#         receipt = f"rcpt_{uuid.uuid4().hex[:20]}"

#     client = get_razorpay_client()

#     order = client.order.create(  # type: ignore
#         {
#             "amount": amount_in_paise,
#             "currency": "INR",
#             "receipt": receipt,
#             "payment_capture": 1,
#             "notes": safe_notes,
#         }
#     )

#     return order


# # -------------------------------------------------
# # SIGNATURE VERIFICATION
# # -------------------------------------------------
# def verify_payment_signature(
#     order_id: str,
#     payment_id: str,
#     signature: str
# ) -> bool:
#     """
#     Verify Razorpay payment signature.
#     Returns True if valid, False otherwise.
#     """

#     client = get_razorpay_client()

#     try:
#         client.utility.verify_payment_signature(  # type: ignore
#             {
#                 "razorpay_order_id": order_id,
#                 "razorpay_payment_id": payment_id,
#                 "razorpay_signature": signature,
#             }
#         )
#         return True

#     except SignatureVerificationError:  # type: ignore
#         return False
