import razorpay
from typing import Any, Dict, Optional
from razorpay.errors import SignatureVerificationError  # type: ignore

from math_saas.config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET


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
    """

    if not isinstance(amount_in_paise, int):
        raise ValueError("amount_in_paise must be an integer")

    if amount_in_paise < 100:
        raise ValueError("amount_in_paise must be >= 100 paise")

    # Razorpay requires all notes to be strings
    safe_notes = {}
    if notes:
        safe_notes = {str(k): str(v) for k, v in notes.items()}

    client = get_razorpay_client()

    order = client.order.create(  # type: ignore
        {
            "amount": amount_in_paise,
            "currency": "INR",
            "receipt": receipt,
            "payment_capture": 1,
            "notes": safe_notes,
        }
    )

    return order


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
        client.utility.verify_payment_signature(  # type: ignore
            {
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
            }
        )
        return True

    except SignatureVerificationError:  # type: ignore
        return False

# import razorpay
# from typing import Any, Dict, Optional
# from razorpay.errors import SignatureVerificationError  # type: ignore

# from math_saas.config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET


# _client: Optional[razorpay.Client] = None


# def get_razorpay_client() -> razorpay.Client:
#     """Return a singleton Razorpay client."""
#     global _client

#     if RAZORPAY_KEY_ID is None or RAZORPAY_KEY_SECRET is None:
#         raise RuntimeError("Razorpay keys are not set in environment variables")

#     if _client is None:
#         _client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

#     return _client


# def create_order(
#     amount_in_paise: int,
#     receipt: str,
#     notes: Optional[Dict[str, Any]] = None
# ) -> Dict[str, Any]:
#     """Create a Razorpay order."""
#     client = get_razorpay_client()

#     order = client.order.create(  # type: ignore
#         {
#             "amount": amount_in_paise,
#             "currency": "INR",
#             "receipt": receipt,
#             "payment_capture": 1,
#             "notes": notes or {},
#         }
#     )

#     return order


# def verify_payment_signature(
#     order_id: str,
#     payment_id: str,
#     signature: str
# ) -> bool:
#     """Verify Razorpay payment signature."""
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

# # import razorpay
# # from razorpay.errors import SignatureVerificationError  # type: ignore
# # from math_saas.config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET

# # _client = None

# # def get_razorpay_client():
# #     global _client
# #     if _client is None:
# #         _client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
# #     return _client


# # def create_order(amount_in_paise: int, receipt: str, notes=None):
# #     client = get_razorpay_client()
# #     return client.order.create(   # type: ignore
# #         {
# #             "amount": amount_in_paise,
# #             "currency": "INR",
# #             "receipt": receipt,
# #             "payment_capture": 1,
# #             "notes": notes or {},
# #         }
# #     )


# # def verify_payment_signature(order_id: str, payment_id: str, signature: str) -> bool:
# #     client = get_razorpay_client()
# #     try:
# #         client.utility.verify_payment_signature(   # type: ignore
# #             {
# #                 "razorpay_order_id": order_id,
# #                 "razorpay_payment_id": payment_id,
# #                 "razorpay_signature": signature,
# #             }
# #         )
# #         return True
# #     except SignatureVerificationError:  # type: ignore
# #         return False
