
import numpy as np
import tensorflow as tf 
import pandas as pd

# load model function 
def load_model(model_dir): 
    model = tf.keras.models.load_model(model_dir)
    return model


# gett the prediction
def prediction_for_spesific_user(model, df: pd.DataFrame): 
    # random user_id
    user_id = random.randint(a = 9999, b = 99999)
    all_prediction = []
    # recipe_id_uniques = np.unique(df.loc[:, 'resep_id'])
    model = load_model()
    for i in range(df.shape[0]): 
        print(f'product id : {i}')
        all_prediction.append(model.predict(np.array([[user_id, i]]))[0][0] * 5)
    # this will sort the ratings from higher to lower
    all_prediction = np.argsort(all_prediction)[::-1]
    return all_prediction 
