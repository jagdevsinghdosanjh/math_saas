import streamlit as st
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import json

from auth import require_admin
from utils.db import get_supabase


# ---------------------------------------------------------
# PLAN METADATA
# ---------------------------------------------------------
PLAN_META: Dict[str, Dict[str, Any]] = {
    "MTH99": {"name": "Monthly", "days": 30, "amount": 9900},
    "YR999": {"name": "Yearly", "days": 365, "amount": 99900},
}


def _get_plan_meta(plan_code: str) -> Dict[str, Any]:
    return PLAN_META.get(plan_code, PLAN_META["MTH99"])


# ---------------------------------------------------------
# SAFE HELPERS
# ---------------------------------------------------------
def _safe_dict(value: Any) -> Dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _safe_iso(dt: Any) -> datetime:
    if isinstance(dt, str):
        try:
            return datetime.fromisoformat(dt)
        except Exception:
            return datetime.utcnow()
    return datetime.utcnow()


def _safe_user_id(value: Any) -> str:
    return value if isinstance(value, str) and value.strip() else ""


def _current_admin_id() -> str:
    sb = get_supabase()
    res = sb.auth.get_user()
    user = res.user if res and res.user else None
    return getattr(user, "id", "") or ""


# ---------------------------------------------------------
# AUDIT LOGGING
# ---------------------------------------------------------
def _log_admin_action(
    sub_id: str,
    action: str,
    before: Dict[str, Any],
    after: Dict[str, Any],
) -> None:
    sb = get_supabase()
    admin_id = _current_admin_id()

    sb.table("subscription_audit").insert(
        {
            "subscription_id": sub_id,
            "admin_id": admin_id,
            "action": action,
            "before_state": json.dumps(before),
            "after_state": json.dumps(after),
        }
    ).execute()


def _fetch_last_audit(sub_id: str) -> Optional[Dict[str, Any]]:
    sb = get_supabase()
    res = (
        sb.table("subscription_audit")
        .select("id, before_state, after_state, action, created_at")
        .eq("subscription_id", sub_id)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )

    data = res.data if isinstance(res.data, list) else []
    return data[0] if data and isinstance(data[0], dict) else None


def _restore_from_audit(sub_id: str, audit_row: Dict[str, Any]) -> bool:
    sb = get_supabase()
    before_raw = audit_row.get("before_state") or "{}"

    try:
        before_state = json.loads(before_raw)
    except Exception:
        return False

    # Only restore fields we control
    fields_to_restore = {
        "status",
        "plan",
        "plan_code",
        "amount",
        "started_at",
        "expires_at",
    }

    update_payload = {
        k: v for k, v in before_state.items() if k in fields_to_restore
    }

    if not update_payload:
        return False

    sb.table("subscriptions").update(update_payload).eq("id", sub_id).execute()
    return True


# ---------------------------------------------------------
# FETCH SUBSCRIPTIONS (TYPE-SAFE)
# ---------------------------------------------------------
def _fetch_subscriptions(status_filter: str) -> List[Dict[str, Any]]:
    sb = get_supabase()

    query = (
        sb.table("subscriptions")
        .select(
            """
            id,
            user_id,
            plan,
            plan_code,
            status,
            amount,
            currency,
            razorpay_order_id,
            started_at,
            expires_at
            """
        )
        .order("started_at", desc=True)
    )

    if status_filter != "all":
        query = query.eq("status", status_filter)

    res = query.execute()
    raw = res.data if isinstance(res.data, list) else []

    return [row for row in raw if isinstance(row, dict)]


def _fetch_subscription(sub_id: str) -> Optional[Dict[str, Any]]:
    sb = get_supabase()
    res = (
        sb.table("subscriptions")
        .select("*")
        .eq("id", sub_id)
        .single()
        .execute()
    )
    return _safe_dict(res.data)


# ---------------------------------------------------------
# PLAN-AWARE ADMIN ACTIONS
# ---------------------------------------------------------
def admin_activate(sub_id: str, user_id: str) -> bool:
    sb = get_supabase()

    before = _fetch_subscription(sub_id)

    res = (
        sb.table("subscriptions")
        .select("plan_code")
        .eq("id", sub_id)
        .single()
        .execute()
    )
    data = _safe_dict(res.data)
    plan_code = data.get("plan_code", "MTH99")

    meta = _get_plan_meta(plan_code)

    now = datetime.utcnow()
    expires = now + timedelta(days=meta["days"])

    sb.table("subscriptions").update({
        "status": "active",
        "started_at": now.isoformat(),
        "expires_at": expires.isoformat(),
        "amount": meta["amount"],
        "plan": meta["name"],
    }).eq("id", sub_id).execute()

    sb.table("profiles").update({
        "subscription_status": "active"
    }).eq("id", user_id).execute()

    after = _fetch_subscription(sub_id)
    _log_admin_action(sub_id, "activate", before or {}, after or {})

    return True


def admin_expire(sub_id: str, user_id: str) -> bool:
    sb = get_supabase()
    before = _fetch_subscription(sub_id)

    now = datetime.utcnow().isoformat()

    sb.table("subscriptions").update({
        "status": "expired",
        "expires_at": now
    }).eq("id", sub_id).execute()

    sb.table("profiles").update({
        "subscription_status": "expired"
    }).eq("id", user_id).execute()

    after = _fetch_subscription(sub_id)
    _log_admin_action(sub_id, "expire", before or {}, after or {})

    return True


def admin_extend(sub_id: str, days: int) -> bool:
    sb = get_supabase()
    before = _fetch_subscription(sub_id)

    res = (
        sb.table("subscriptions")
        .select("expires_at")
        .eq("id", sub_id)
        .single()
        .execute()
    )

    data = _safe_dict(res.data)
    current_exp = _safe_iso(data.get("expires_at"))
    new_exp = current_exp + timedelta(days=days)

    sb.table("subscriptions").update({
        "expires_at": new_exp.isoformat()
    }).eq("id", sub_id).execute()

    after = _fetch_subscription(sub_id)
    _log_admin_action(sub_id, f"extend_{days}_days", before or {}, after or {})

    return True


def admin_change_plan(sub_id: str, new_plan: str, new_plan_code: str) -> bool:
    sb = get_supabase()
    before = _fetch_subscription(sub_id)

    meta = _get_plan_meta(new_plan_code)

    sb.table("subscriptions").update({
        "plan": meta["name"],
        "plan_code": new_plan_code,
        "amount": meta["amount"],
    }).eq("id", sub_id).execute()

    after = _fetch_subscription(sub_id)
    _log_admin_action(sub_id, f"change_plan_{new_plan_code}", before or {}, after or {})

    return True


def admin_undo_last(sub_id: str) -> bool:
    audit = _fetch_last_audit(sub_id)
    if not audit:
        return False

    restored = _restore_from_audit(sub_id, audit)
    if not restored:
        return False

    return True


# ---------------------------------------------------------
# MAIN ADMIN PAGE
# ---------------------------------------------------------
def render() -> None:
    require_admin()

    st.title("Subscription Management")

    status_filter = st.selectbox(
        "Filter by Status",
        ["all", "active", "pending", "expired", "failed"],
        index=0,
    )

    subs = _fetch_subscriptions(status_filter)

    if not subs:
        st.info("No subscriptions found for this filter.")
        return

    st.subheader("All Subscriptions")
    st.dataframe(subs, width='stretch', hide_index=True)

    st.subheader("Inspect Subscription")

    ids = [str(s.get("id", "")) for s in subs]
    selected_id = st.selectbox("Select Subscription ID", ids)

    selected: Optional[Dict[str, Any]] = next(
        (s for s in subs if str(s.get("id", "")) == selected_id),
        None
    )

    if not selected:
        st.warning("Subscription not found.")
        return

    st.json(selected)

    user_id = _safe_user_id(selected.get("user_id"))

    st.markdown("---")
    st.subheader("Admin Actions")

    col1, col2, col3, col4, col5 = st.columns(5)

    # ACTIVATE
    if col1.button("Activate"):
        if not user_id:
            st.error("Invalid user_id for this subscription.")
        else:
            admin_activate(selected_id, user_id)
            st.success("Subscription activated successfully")

    # EXPIRE
    if col2.button("Expire"):
        if not user_id:
            st.error("Invalid user_id for this subscription.")
        else:
            admin_expire(selected_id, user_id)
            st.warning("Subscription expired")

    # EXTEND
    extend_days = col3.number_input("Extend (days)", min_value=1, max_value=365, value=30)
    if col3.button("Apply Extension"):
        admin_extend(selected_id, extend_days)
        st.success(f"Extended by {extend_days} days")

    # CHANGE PLAN
    new_plan = col4.selectbox("New Plan", ["Monthly", "Yearly"])
    new_plan_code = "MTH99" if new_plan == "Monthly" else "YR999"
    if col4.button("Change Plan"):
        admin_change_plan(selected_id, new_plan, new_plan_code)
        st.success(f"Plan changed to {new_plan}")

    # UNDO LAST ACTION
    if col5.button("Undo Last Action"):
        if admin_undo_last(selected_id):
            st.success("Last admin action undone.")
        else:
            st.error("No undo available for this subscription.")
