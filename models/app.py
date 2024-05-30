import streamlit as st
from PIL import Image
from io import BytesIO
from main import * 

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
    st.page_link("pages/recomendation_page.py", label="Recomendation", icon="1️⃣")


    
uploaded_file = st.file_uploader("Choose a file", type=['png', 'jpeg'])

if uploaded_file is not None:

    # note : run using command streamlit run app.py --server.enableXsrfProtection false
    bytes_data = uploaded_file.read()
    # Mengonversi ke objek gambar PIL
    image = Image.open(BytesIO(bytes_data))
    st.write("Uploaded Image:")
    st.image(image)

    pred = classification_prediction(bytes_data)
    nutritions, description= get_nutritions_and_descriptions(pred)
    
    df  =  pd.DataFrame(np.expand_dims(nutritions, axis = 0), columns = ['Kalori (kcal)', 'Lemak', 'Karbohidrat', 'Protein', 'Kolesterol (mg)', 'Serat', 'Vitamin A (IU)', 'Vitamin E (mg)', 'Vitamin K (mcg)','Vitamin C (mg)', 'Natrium (mg)' ])
    st.write_stream(stream_data(description, df))
    st.table(df)


else:
    st.warning('👈 Upload your image to get started!')
