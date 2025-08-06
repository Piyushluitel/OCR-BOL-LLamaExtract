# app.py

import streamlit as st
import tempfile
import os
from main import extract_transaction_data
from PIL import Image
import json

st.set_page_config(page_title="OCR on Bol using LLAMA EXTRACT", layout="wide")

st.title("📄 OCR on Bol using LLAMA EXTRACT")
st.write("Upload a BOL image (JPG or PNG) to extract structured transaction data.")

# Only allow image files
uploaded_file = st.file_uploader("Upload BOL Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_file_path = tmp_file.name

    # Show the image
    image = Image.open(temp_file_path)
    st.image(image, caption="Uploaded Document", use_container_width=True)

    # Perform extraction
    with st.spinner("🔍 Extracting data using LlamaExtract..."):
        try:
            extracted_data = extract_transaction_data(temp_file_path)
            st.success("✅ Extraction Successful!")
            st.subheader("📤 Extracted JSON Output:")
            st.json(extracted_data)
        except Exception as e:
            st.error(f"❌ Extraction failed: {str(e)}")

    # Cleanup
    os.unlink(temp_file_path)
