
import numpy as np
import tensorflow as tf 
import pandas as pd
import random

# load model function 
def load_model(model_dir): 
    model = tf.keras.models.load_model(model_dir)
    return model
def read_food_dataset(): 
    return pd.read_excel("./data/recommendartion_data/final_data.xlsx")

def preproccess_image(image): 
    image_read = tf.io.read_file(image)
    img_decode =  tf.io.decode_jpg(image_read)
    img_resize = tf.image.resize(img_decode, [224, 224])
    return [img_resize]


# gett the prediction
def prediction_for_spesific_user(): 
    # random user_id
    user_id = random.randint(a = 9999, b = 99999)
    all_prediction = []
    # recipe_id_uniques = np.unique(df.loc[:, 'resep_id'])
    model = load_model()
    df = read_food_dataset()
    for i in range(df.shape[0]): 
        print(f'product id : {i}')
        all_prediction.append(model.predict(np.array([[user_id, i]]))[0][0] * 5)
    # this will sort the ratings from higher to lower
    all_prediction = np.argsort(all_prediction)[::-1]
    return all_prediction 

def classification_prediction(image): 
    model= tf.keras.models.load_model("./classificaiton_model.h5")
    img_pred = preproccess_image(image)
    return np.argmax[model.predict(img_pred)]




# model = 