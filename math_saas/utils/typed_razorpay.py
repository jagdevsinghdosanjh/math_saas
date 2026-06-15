# math_saas/utils/typed_razorpay.py

from typing import Any, Dict, Protocol


class OrderAPI(Protocol):
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        ...


class UtilityAPI(Protocol):
    def verify_payment_signature(self, data: Dict[str, str]) -> None:
        ...


class TypedRazorpayClient(Protocol):
    order: OrderAPI
    utility: UtilityAPI
