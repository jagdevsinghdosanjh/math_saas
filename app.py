import streamlit as st
from math_saas.admin.admin_app import run_admin

st.set_page_config(page_title="math-saas", layout="wide")

run_admin()
