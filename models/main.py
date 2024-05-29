
import numpy as np
import tensorflow as tf 
import pandas as pd
import random
import cv2
import numpy as np
# load model function 
def load_model(model_dir): 
    model = tf.keras.models.load_model(model_dir)
    return model
def read_food_dataset(): 
    return pd.read_excel("./data/recommendartion_data/final_data.xlsx")

def preproccess_image(image): 
    # img = tf.io.decode_jpeg(image, channels=3)
    # img_decode = tf.io.decode_jpeg(img, channels=3)
    # image_reshape = cv2.resize(image, (150, 150))
    # print(f'hasil {image_reshape.shape}')
    # img_normalized = tf.cast(image_reshape / 255, tf.float32) 
    # img_resize = tf.image.resize(img_normalized , [150, 150], preserve_aspect_ratio=False)

    image_resized = cv2.resize(image, (150, 150))
    image_resized = [image_resized]
    # print(f'hasil {image_resized.shape}')
    img_normalized = tf.cast(image_resized, tf.float32) / 255.0  # Normalisasi intensitas piksel

    print(img_normalized)
    # return img_normalized
    
    return img_normalized




# gett the prediction
def prediction_for_spesific_user(): 
    # random user_id
    user_id = random.randint(a = 9999, b = 99999)
    all_prediction = []
    # recipe_id_uniques = np.unique(df.loc[:, 'resep_id'])9
    model = load_model()
    df = read_food_dataset()
    for i in range(df.shape[0]): 
        print(f'product id : {i}')
        all_prediction.append(model.predict(np.array([[user_id, i]]))[0][0] * 5)
    # this will sort the ratings from higher to lower
    all_prediction = np.argsort(all_prediction)[::-1]
    return all_prediction 

def classification_prediction(image): 
    model= tf.keras.models.load_model("../models/food_classifier.keras")
    img_pred = preproccess_image(image)
    print(np.argmax(np.array(model.predict(img_pred)).flatten()))
    print(model.predict(img_pred))
    return np.argmax(model.predict(img_pred))




# model = 