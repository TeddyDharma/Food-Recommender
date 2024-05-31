from main import *  
import cv2 
import json

# prd = classification_prediction(image = "./random2.png")
# # print(prd)
# df = display_nutrition(prd)
# print(df)

tst = recommendation_for_spesific_user()
# print(tst)

# print(json.loads(tst)['recommendation'][0]) 

# print(json.loads(tst)['recommendation']) 

image_links = read_image_link() 

print(get_final_recomendation(tst, image_links))