
import streamlit as st
import pytesseract
from PIL import Image
import numpy as np
import re

def extract_field(pattern, text, group=None):
    match = re.search(pattern, text)
    if not match:
        return ''
    return match.group(group) if group is not None else match.group(0)

def parse_email_text(text):
    name = extract_field(r"Name:\s*(.*)", text, group=1)
    address_line_1 = extract_field(r"\d+\s+[^,\n]+", text)
    suburb = extract_field(r"\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)\b(?=\s+(VIC|NSW|QLD|WA|SA|TAS|NT|ACT))", text, group=1)
    state = extract_field(r"\b(VIC|NSW|QLD|WA|SA|TAS|NT|ACT)\b", text, group=1)
    postcode = extract_field(r"\b(\d{4})\b", text, group=1)
    phone = extract_field(r"(04\d{8}|\+614\d{8})", text, group=1)
    email = extract_field(r"([\w.-]+@[\w.-]+\.[A-Za-z]{2,})", text, group=1)
    product_match = re.findall(r"Design:.*?\n|Material:.*?\n", text)
    product = ' '.join([line.strip() for line in product_match])

    row = [
        "\"Natty & Polly Wallpapers\"", "\"Wallpaper\"", "", "", "\"Aus Post\"",
        f"\"{product}\"", f"\"{name}\"", "", f"\"{address_line_1}\"", f"\"{suburb}\"",
        f"\"{state}\"", f"\"{postcode}\"", f"\"{email}\"", f"\"{phone}\"", ""
    ]
    return ','.join(row)

st.set_page_config(page_title="Email to CSV Row Generator")
st.title("📩 Email to CSV Row Generator")

uploaded_file = st.file_uploader("Upload an email screenshot", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Email", use_column_width=True)
    st.write("Processing with OCR…")

    with st.spinner("Extracting text..."):
        text = pytesseract.image_to_string(image)
        csv_row = parse_email_text(text)

    st.text_area("CSV Row Output", value=csv_row, height=100)
    st.download_button("Download CSV Row", csv_row, file_name="order_row.csv")
