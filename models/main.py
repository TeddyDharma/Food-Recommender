
import numpy as np
import tensorflow as tf 
import pandas as pd
import random
import cv2
import numpy as np
import os
import json
import time 
import keras



# load model function 
def load_model(model_dir): 
    model = tf.keras.models.load_model(model_dir)
    return model



def preproccess_image(image): 
    img_height, img_width = 150, 150
    img = tf.io.decode_jpeg(image, channels=3)
    image_resized = tf.image.resize(img, [img_height, img_width])
    return tf.expand_dims(image_resized, 0)


def classification_prediction(image): 
    model_path = os.path.abspath("./food_classifier.keras")
    model= tf.keras.models.load_model(model_path)
    img_pred = preproccess_image(image)
    classes = os.listdir("../data/images/train")
    pred  = {"prediction": classes[np.argmax(model.predict(img_pred)[0])]}
    return json.dumps(pred)


def get_nutritions_and_descriptions(model_prediction):
    json_load = json.loads(model_prediction)['prediction']
    print(str(json_load).lower())
    df_nutrition = pd.read_excel("../data/nutrition data/Dataset makanan per 100 gram.xlsx") 
    df_description  = pd.read_excel("../data/nutrition data/description_food.xlsx") 
    for idx, _ in enumerate(df_nutrition['Makanan']): 
        if str(df_nutrition.loc[idx, "Makanan"]).lower() == str(json_load).lower(): 
            nutritions = df_nutrition.iloc[idx, 1:].to_list()
            descriptions  = df_description.loc[idx, "Description"]
    return nutritions, descriptions


    
def stream_data(description : str, nutritions_pd :  pd.DataFrame): 
    for word in description.split(" "): 
        yield word + " "
        time.sleep(0.05)
        nutritions_pd

    

# gett the prediction
def prediction_for_spesific_user(): 
    reconstructed_model = keras.models.load_model(
    "./recommendation_model.keras",
    )
    df = pd.read_excel("./final_data.xlsx")
    df.drop_duplicates(subset=['resep_id'], inplace = True)
    df.reset_index(drop=True, inplace = True)
    df = df.iloc[:100, :]
    user_id = random.randint(a = 9999, b = 99999)
    all_prediction = []
    for i in range(df.shape[0]): 
        print(f'product id : {i}')
        all_prediction.append(reconstructed_model.predict(np.array([[user_id, i]]))[0][0] * 5)
    # this will sort the ratings from higher to lower
    all_prediction = np.argsort(all_prediction)[::-1].tolist()
    pred_temp = []
    for foods in all_prediction: 
        pred_temp.append(df.loc[int(foods), "nama_makanan"])
    recommendation = {"recommendation": pred_temp}
    return json.dumps(recommendation)


# model = 