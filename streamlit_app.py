import boto3
import tempfile
import os
import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from utils import extract_transaction_data, LLAMA_CLOUD_API_KEY


# Function to get the filenames from the local s3_filenames.txt file
def get_local_filenames(file_path: str) -> list:
    try:
        # Open and read the s3_filenames.txt file locally
        with open(file_path, 'r') as file:
            filenames = [line.strip() for line in file.readlines()]

        # If the file is empty, we can return an empty list
        if not filenames:
            st.warning("⚠️ No filenames found in the s3_filenames.txt file.")
        
        return filenames

    except FileNotFoundError:
        st.error(f"❌ The file {file_path} was not found locally. Please ensure it's in the correct directory.")
        return []
    
    except Exception as e:
        st.error(f"❌ Error reading filenames from {file_path}: {e}")
        return []


# Function to get a pre-signed URL to access the file directly from S3
def get_s3_presigned_url(bucket_name: str, file_key: str, expiration: int = 3600) -> str:
    s3_client = boto3.client('s3')
    try:
        # Generate a presigned URL to access the file from S3
        url = s3_client.generate_presigned_url('get_object',
                                               Params={'Bucket': bucket_name, 'Key': file_key},
                                               ExpiresIn=expiration)
        return url
    except Exception as e:
        st.error(f"❌ Error generating pre-signed URL for {file_key} from S3: {e}")
        return None


# Set up the page configuration
st.set_page_config(page_title="OCR on Bol using LLAMA EXTRACT", layout="wide")

# Session state initialization for login
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False


# Authentication page
if not st.session_state.authenticated:
    # Show login form
    st.title("Login")

    username = st.text_input("Username", type="default", value="admin")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "14c9fff37033c2fd309682ed603f8178a3e30e3a5fb16ea1bc871e6202db":
            st.session_state.authenticated = True
        else:
            st.error("❌ Invalid username or password.")

else:
    # Main app content after authentication
    st.title("📄 OCR on Bol using LLAMA EXTRACT")
    st.write("Upload a BOL image (JPG, PNG, or PDF) or select one from the S3 bucket to extract structured transaction data.")

    # Path to the local s3_filenames.txt file (update with your actual path)
    local_filename_path = 's3_filenames.txt'  # Adjust this path if needed

    # Get the list of files from the local s3_filenames.txt file
    filenames = get_local_filenames(local_filename_path)

    # Radio button to choose between file upload and local file selection
    option = st.sidebar.radio("Choose an option to proceed:", ["Upload a File", "Select from s3 bucket"])

    # Option 1: Upload a file from the user's local system
    if option == "Upload a File":
        uploaded_file = st.file_uploader("Upload BOL Image or PDF", type=["jpg", "jpeg", "png", "pdf"])

        if uploaded_file:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(uploaded_file.read())
                temp_file_path = tmp_file.name

            # Create two columns to display the image and JSON side by side
            col1, col2 = st.columns([1, 2])  # You can adjust the width ratio

            # Show the image in the first column
            with col1:
                if uploaded_file.type in ["image/jpeg", "image/png", "image/jpg"]:
                    # Show the image
                    image = Image.open(temp_file_path)  # Open the image using PIL
                    st.image(image, caption="Uploaded Document", use_container_width=True)

                elif uploaded_file.type == "application/pdf":
                    # For PDFs, show the first page as an image preview
                    try:
                        from pdf2image import convert_from_path
                        pages = convert_from_path(temp_file_path, first_page=1, last_page=1)
                        st.image(pages[0], caption="First page of PDF", use_container_width=True)
                    except Exception as e:
                        st.error(f"❌ Error displaying PDF: {e}")

            # Show the extracted JSON data in the second column
            with col2:
                # Perform extraction with api_key passed to the function
                with st.spinner("🔍 Extracting data using LlamaExtract..."):
                    try:
                        extracted_data = extract_transaction_data(temp_file_path, api_key=LLAMA_CLOUD_API_KEY)
                        st.success("✅ Extraction Successful!")
                        st.subheader("📤 Extracted JSON Output:")
                        st.json(extracted_data)
                    except Exception as e:
                        st.error(f"❌ Extraction failed: {str(e)}")

            # Cleanup
            os.unlink(temp_file_path)

    # Option 2: Select a file from the local filenames
    elif option == "Select from s3 bucket":
        # Provide a dropdown to select a file from the local filenames
        if filenames:
            selected_file = st.selectbox("Select Bill of Lading from the list:", filenames)

            if selected_file:
                # Get the S3 presigned URL to access the file directly
                s3_path = selected_file  # Direct path to the S3 file (no folder prefix needed)
                presigned_url = get_s3_presigned_url('fp-prod-s3', s3_path)

                if presigned_url:
                    # Download image from the S3 URL to process it locally
                    try:
                        # Fetch the file from the presigned URL and save it as a temporary file
                        response = requests.get(presigned_url)

                        # Create a temporary file to save the downloaded content
                        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(selected_file)[1]) as tmp_file:
                            tmp_file.write(response.content)
                            temp_file_path = tmp_file.name

                        # Show the image in the first column
                        col1, col2 = st.columns([1, 2])  # You can adjust the width ratio
                        with col1:
                            # Load the image using PIL
                            image = Image.open(temp_file_path)
                            st.image(image, caption=f"Uploaded Document from S3: {selected_file}", use_container_width=True)

                        # Show the extracted JSON data in the second column
                        with col2:
                            with st.spinner("🔍 Processing and Extracting data. This might take some time ..."):
                                try:
                                    extracted_data = extract_transaction_data(temp_file_path, api_key=LLAMA_CLOUD_API_KEY)
                                    st.success("✅ Extraction Successful!")
                                    st.subheader("📤 Final output after Post Processing:")
                                    st.json(extracted_data)
                                except Exception as e:
                                    st.error(f"❌ Extraction failed: {str(e)}")

                        # Cleanup the temporary file
                        os.unlink(temp_file_path)
                    except Exception as e:
                        st.error(f"❌ Error processing file: {e}")
