
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



keras.saving.get_custom_objects().clear()
# register the custom layer 
@keras.saving.register_keras_serializable(package="RecomendationLayer")
class RecommenderNet(tf.keras.Model):
    def __init__(self, num_users, num_fooods, embedding_size, **kwargs):
        super().__init__(**kwargs)
        self.num_users = num_users
        self.num_fooods = num_fooods
        self.embedding_size = embedding_size
        # first hidden layer
        self.dense1 = tf.keras.layers.Dense(128, activation="relu")
        #  second hidden layer
        self.dense2 = tf.keras.layers.Dense(64, activation="relu")
        # third hidden layer
        self.dense3 = tf.keras.layers.Dense(1, activation="sigmoid")
        # embedding layer for user vector
        self.user_embedding = tf.keras.layers.Embedding(
            num_users,
            # embedding size = user vector
            embedding_size,
            # set the weight to standart normalization and thhe output shape of array will sane like num_users.embedidng size
            embeddings_initializer="he_normal",
            embeddings_regularizer=tf.keras.regularizers.l2(1e-6),
        )
        # adding user_bias
        self.user_bias = tf.keras.layers.Embedding(num_users, 1)
        # embedding layer for food vector
        self.food_embedding = tf.keras.layers.Embedding(
            num_fooods,
            embedding_size,
            # set the weight to standart normalization and thhe output shape of array will sane like num_users.embedidng size
            embeddings_initializer="he_normal",
            embeddings_regularizer= tf.keras.regularizers.l2(1e-6),
        )
        self.food_bias = tf.keras.layers.Embedding(num_fooods, 1)
    
    def call(self, inputs):
        # user vector
        user_vector = self.user_embedding(inputs[:, 0])
        # user bias
        user_bias = self.user_bias(inputs[:, 0])
        food_vector = self.food_embedding(inputs[:, 1])
        food_bias = self.food_bias(inputs[:, 1])
        # set the dfimension to 2D dimensio
        dot_user_movie = tf.tensordot(user_vector, food_vector, 2)
        # Add all the components (including bias)
        x = dot_user_movie + user_bias + food_bias
        #  first dense layer
        dense_layer1 = self.dense1(x)
        dense_layer2 = self.dense2(dense_layer1)
        # return the output layer
        return self.dense3(dense_layer2)
    
    #  adding some config
    def get_config(self):
        #  call the main config
        config = super().get_config()
        # update to config, to initialize the self.num_users = num_users, self.num_fooods = num_fooods self.embedding_size = embedding_size
        config.update({
            # all the configuration forr new config
            "num_users": self.num_users,
            "num_fooods": self.num_fooods,
            "embedding_size": self.embedding_size,
        })
        #  return the config
        return config
    
    # for class method
    @classmethod
    def from_config(cls, config):
        return  cls( **config)


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



def read_image_link(): 
    data_image_link  = pd.read_excel("../data/recommendartion_data/food_image_links_fix.xlsx")
    data_image_link.drop(data_image_link.columns[data_image_link.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
    return data_image_link

# gett the prediction
def recommendation_for_spesific_user(): 
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

def get_final_recomendation(recommendations_json, data_image_link : pd.DataFrame): 
    products = []
    data_per_product = {}
    recommendation_json_load = json.loads(recommendations_json)['recommendation']
    iter = 1
    for idx, _ in enumerate(recommendation_json_load): 
        data_per_product["name"] = recommendation_json_load[idx]
        data_per_product["price"] = "$10"
        data_per_product['description'] = f'This is {recommendation_json_load[idx]}'


        for food_idx in range(data_image_link.shape[0]):
            if str(recommendation_json_load[idx]).lower() in  str(data_image_link.loc[food_idx, "nama_makaan"]).lower(): 
                data_per_product['image'] =  data_image_link.loc[food_idx, "gambar"]
                iter += 1
        products.append(data_per_product)
        data_per_product = {}

    return products


# model = 