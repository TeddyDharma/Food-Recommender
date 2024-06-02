import streamlit as st
from main import * 
from PIL import Image
import requests

st.markdown("""
    <style>
    /* Mengubah alignment konten utama */
    .main > div {
        max-width: 900px;
        margin-left: 0; /* Align content to the left */
        padding-left: 50px; /* Adjust the left padding to your preference */
    }
            
    h1 {
        font-size: 48px;
    }
    </style>
    """, unsafe_allow_html=True)

st.header("Best Indonesian Foods and Drinks For You !", divider = "gray")

tst = recommendation_for_spesific_user()


image_links = read_image_link() 
products = get_final_recomendation(tst, image_links)
product_selected = ""
columns_per_row = 4

for i in range(0, len(products), columns_per_row):
    cols = st.columns(columns_per_row, gap = "medium")
    for col, product in zip(cols, products[i:i + columns_per_row]):
        with col:
            with st.container():
                response = requests.get(product['image'], stream=True)
                image = Image.open(response.raw)
                resized_image = image.resize((200, 200), Image.Resampling.NEAREST)
           
                st.image(resized_image, use_column_width=True)
                st.text(f"Protein: {product['protein']} g")
                st.text(f"Energi: {product['energi']} g")
                st.text(f"Karbohidrat: {product['karbohidrat']} g")
                st.text(f"Lemak: {product['lemak']} g")
                st.caption(product["name"])
 