
import streamlit as st
from PIL import Image
import easyocr
import numpy as np
import re

reader = easyocr.Reader(['en'], gpu=False)

def extract_field(pattern, text, group=1):
    match = re.search(pattern, text)
    return match.group(group) if match else ''

def parse_email_text(text):
    name = extract_field(r"Name:\s*(.*)", text)
    address_line_1 = extract_field(r"\d+\s+[^,\n]+", text)
    suburb = extract_field(r"\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)\b(?=\s+(VIC|NSW|QLD|WA|SA|TAS|NT|ACT))", text)
    state = extract_field(r"\b(VIC|NSW|QLD|WA|SA|TAS|NT|ACT)\b", text)
    postcode = extract_field(r"\b(\d{4})\b", text)
    phone = extract_field(r"(04\d{8}|\+614\d{8})", text)
    email = extract_field(r"([\w.-]+@[\w.-]+\.[A-Za-z]{2,})", text)
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
        result = reader.readtext(np.array(image), detail=0)
        text = "\n".join(result)
        csv_row = parse_email_text(text)

    st.text_area("CSV Row Output", value=csv_row, height=100)
    st.download_button("Download CSV Row", csv_row, file_name="order_row.csv")
