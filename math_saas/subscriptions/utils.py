from typing import Any, Dict


# -----------------------------
# Format currency
# -----------------------------
def format_inr(amount_paise: int) -> str:
    rupees = amount_paise / 100
    return f"₹{rupees:,.2f}"


# -----------------------------
# Safe dict getter
# -----------------------------
def safe_get(d: Dict[str, Any], key: str, default: Any = None) -> Any:
    value = d.get(key, default)
    return value if value is not None else default


# -----------------------------
# Convert plan code to readable name
# -----------------------------
def plan_name(plan_code: str) -> str:
    mapping = {
        "FREE": "Free Plan",
        "MONTHLY": "Monthly Plan",
        "ANNUAL": "Annual Plan",
    }
    return mapping.get(plan_code, plan_code)
