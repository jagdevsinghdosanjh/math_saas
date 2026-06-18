import streamlit as st
import razorpay

def get_razorpay_keys():
    r = st.secrets.get("razorpay", {})
    key_id = r.get("key_id")
    key_secret = r.get("key_secret")
    return key_id, key_secret

def get_razorpay_client():
    key_id, key_secret = get_razorpay_keys()
    if not key_id or not key_secret:
        return None
    return razorpay.Client(auth=(key_id, key_secret))
