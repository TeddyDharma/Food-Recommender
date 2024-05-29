import streamlit as st
from PIL import Image
from io import BytesIO


st.set_page_config(page_title='NutriMate', page_icon='🥗')
st.title('🥗 NutriMate')

with st.expander('About this app'):
  st.markdown('**What can this app do?**')
  st.info('NutriMate is a food image classifier application that assists users in easily obtaining food descriptions. Leveraging the Convolutional Neural Network (CNN) concept with a pretrained architecture and weights from MobileNet V2, NutriMate can identify food types from uploaded images and provide users with accurate nutritional information.')

  st.markdown('**How to use the app?**')
  st.warning('To engage with the app, go to the sidebar and Input a data set. As a result, this would initiate the Deep Learning model building process, display the model results, and provide the recommendation system for food classification. You will then be able to view the classification results, nutritional information of the identified food, and receive personalized food recommendations based on your preferences and dietary requirements.')

  st.markdown('**Under the hood**')
  st.markdown('Data sets:')
  st.code('''- Indonesian Food data set
  ''', language='markdown')
  

# File uploader diletakkan di dalam sidebar

with st.sidebar:
 
    st.page_link("app.py", label="Home", icon="🏠")
    st.page_link("../front end/pages/recomendation_page.py", label="Recomendation", icon="1️⃣")


    
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
else:
    st.warning('👈 Upload your image to get started!')
