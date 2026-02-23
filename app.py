import os
import streamlit as st
from PIL import Image
from rembg import remove, new_session
import io

# Render optimization
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

# Page config
st.set_page_config(
    page_title="AI Background Remover",
    page_icon="🖼️",
    layout="centered"
)

# Title
st.title("AI Background Remover")
st.write("Upload an image to remove background")

# Load AI model safely
@st.cache_resource
def load_model():
    return new_session()

session = load_model()

# File uploader
uploaded_file = st.file_uploader(
    "Upload Image",
    type=["png", "jpg", "jpeg"]
)

# Process image
if uploaded_file is not None:

    input_image = Image.open(uploaded_file).convert("RGBA")

    st.subheader("Original Image")
    st.image(input_image)

    with st.spinner("Removing background..."):
        output_image = remove(input_image, session=session)

    st.subheader("Result Image")
    st.image(output_image)

    buf = io.BytesIO()
    output_image.save(buf, format="PNG")

    st.download_button(
        "Download Image",
        buf.getvalue(),
        "bg_removed.png",
        "image/png"
    )

else:
    st.info("Please upload an image to begin")