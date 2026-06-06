import streamlit as st
from math_saas.admin.admin_app import run_admin
from math_saas.student.student_app import run_student

st.set_page_config(page_title="math-saas", layout="wide")

run_admin()
