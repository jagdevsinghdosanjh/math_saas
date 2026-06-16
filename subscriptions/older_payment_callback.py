from utils.payment import verify_payment_signature
from subscriptions.core import (
    get_subscription_by_order,
    activate_subscription,
    log_payment,
)
from subscriptions.plans import PLANS


def handle_payment_callback(order_id: str, payment_id: str, signature: str):
    if not verify_payment_signature(order_id, payment_id, signature):
        return {"success": False, "error": "Invalid payment signature"}

    sub_res = get_subscription_by_order(order_id)
    subscription = sub_res.data

    if not subscription:
        return {"success": False, "error": "Subscription not found"}

    subscription_id = subscription["id"]
    plan_code = subscription["plan_code"]
    plan_days = PLANS[plan_code]["duration_days"]
    amount = subscription["amount"]

    activate_subscription(subscription_id, plan_days)

    log_payment(subscription_id, order_id, payment_id, signature, amount)

    return {"success": True}

# from math_saas.utils.payment import verify_payment_signature
# from math_saas.subscriptions.core import (
#     get_subscription_by_order,
#     activate_subscription,
#     log_payment,
# )
# from math_saas.subscriptions.plans import PLANS


# def handle_payment_callback(order_id: str, payment_id: str, signature: str):
#     """Verify payment and activate subscription."""

#     # 1. Verify Razorpay signature
#     if not verify_payment_signature(order_id, payment_id, signature):
#         return {"success": False, "error": "Invalid payment signature"}

#     # 2. Fetch subscription
#     sub_res = get_subscription_by_order(order_id)
#     subscription = sub_res.data

#     if not subscription:
#         return {"success": False, "error": "Subscription not found"}

#     subscription_id = subscription["id"]
#     plan_code = subscription["plan_code"]
#     plan_days = PLANS[plan_code]["duration_days"]
#     amount = subscription["amount"]

#     # 3. Activate subscription
#     activate_subscription(subscription_id, plan_days)

#     # 4. Log payment
#     log_payment(subscription_id, order_id, payment_id, signature, amount)

#     return {"success": True}
