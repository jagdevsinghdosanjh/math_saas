import re

def fix_math_rendering(text: str) -> str:
    """Converts malformed math expressions into proper LaTeX syntax for Streamlit rendering."""
    text = re.sub(r"\[\s*(.*?)\s*\]", r"$$\1$$", text)
    text = re.sub(r"\(\\frac(.*?)\)", r"\\(\\frac\1\\)", text)
    text = re.sub(r"\((\d+\/\d+)\)", r"\\(\1\\)", text)
    text = re.sub(r"sqrt\((.*?)\)", r"\\(\\sqrt{\1}\\)", text)
    text = re.sub(r"([a-zA-Z0-9])\^(\d+)", r"\\(\1^{\2}\\)", text)
    text = re.sub(r"sum_?\{(.*?)\}\^\{(.*?)\}", r"\\(\\sum_{\1}^{\2}\\)", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text
