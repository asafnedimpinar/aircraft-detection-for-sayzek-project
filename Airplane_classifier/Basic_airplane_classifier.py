import cv2
import numpy as np
from keras.models import load_model

model = load_model("C:/Users/ASAF/Desktop/project_codes/project/uses_modles/efficientnet_aircraft_model.h5")
class_names = ["F16", "Boeing737", "Mig29", "A320"]

def classify_aircraft(cropped_img):
    try:
        img = cv2.resize(cropped_img, (224, 224))
        img = img.astype("float32") / 255.0
        img = np.expand_dims(img, axis=0)
        preds = model.predict(img, verbose=0)
        return class_names[np.argmax(preds)]
    except:
        return "Tespit Edilemedi
