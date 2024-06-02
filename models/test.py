from main import *  
import cv2 
import json

# prd = classification_prediction(image = "./random2.png")
# # print(prd)
# df = display_nutrition(prd)
# print(df)

tst = recommendation_for_spesific_user()
print(tst)
# print(tst)


image_links = read_image_link() 

tst = get_final_recomendation(tst, image_links)
print(tst[2]['image'])
