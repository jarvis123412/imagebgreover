import os
import streamlit as st
from PIL import Image
from rembg import remove, new_session
import io

# Limit CPU threads (Render free tier friendly)
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

# Page setup
st.set_page_config(
    page_title="AI Background Remover",
    page_icon="🖼️",
    layout="centered"
)

st.title("AI Background Remover")
st.write("Upload an image and remove its background instantly.")

# Cache AI model session
@st.cache_resource
def get_session():
    return new_session()

session = get_session()

# Resize function
def resize_image(img, max_size=800):
    if max(img.size) > max_size:
        img.thumbnail((max_size, max_size))
    return img

# File uploader
uploaded_file = st.file_uploader(
    "Upload image...",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:

    img = Image.open(uploaded_file).convert("RGBA")
    img = resize_image(img)

    st.subheader("Original Image")
    st.image(img)

    with st.spinner("Removing background..."):
        output_img = remove(img, session=session)

    st.subheader("Background Removed")
    st.image(output_img)

    buf = io.BytesIO()
    output_img.save(buf, format="PNG")

    st.download_button(
        "⬇ Download",
        data=buf.getvalue(),
        file_name="bg_removed.png",
        mime="image/png"
    )

    st.success("Done!")

else:
    st.info("Please upload an image.")