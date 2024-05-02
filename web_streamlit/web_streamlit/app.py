import streamlit as st
from PIL import Image
from io import BytesIO

# File uploader diletakkan di dalam sidebar
with st.sidebar:
    uploaded_file = st.file_uploader("Choose a file", type=['png', 'jpeg'])

if uploaded_file is not None:
    # Membaca file sebagai bytes
    bytes_data = uploaded_file.getvalue()

    # Mengonversi ke objek gambar PIL
    image = Image.open(BytesIO(bytes_data))
    st.write("Uploaded Image:")
    st.image(image)

    # Mengonversi ke string menggunakan BytesIO
    stringio = BytesIO(bytes_data)
    st.write("BytesIO object:", stringio)

