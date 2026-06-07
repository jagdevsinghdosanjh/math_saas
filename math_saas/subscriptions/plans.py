from typing import Dict, Any

PLANS: Dict[str, Dict[str, Any]] = {
    "FREE": {
        "name": "Free Plan",
        "price_inr": 0,
        "duration_days": 3650,  # effectively lifetime
    },
    "MONTHLY": {
        "name": "Monthly Plan",
        "price_inr": 99,
        "duration_days": 30,
    },
    "ANNUAL": {
        "name": "Annual Plan",
        "price_inr": 499,
        "duration_days": 365,
    },
}

# PLANS = {
#     "FREE": {
#         "name": "Free Plan",
#         "price_inr": 0,
#         "duration_days": 3650,  # effectively lifetime
#     },
#     "MONTHLY": {
#         "name": "Monthly Plan",
#         "price_inr": 99,
#         "duration_days": 30,
#     },
#     "ANNUAL": {
#         "name": "Annual Plan",
#         "price_inr": 499,
#         "duration_days": 365,
#     },
# }
