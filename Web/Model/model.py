#Actor: Eduardo Pereira
from tensorflow.keras.models import load_model
from cv2 import cvtColor, imread, resize,COLOR_BGR2RGB
from numpy import array
from tensorflow.keras import backend as K

#define metrics
def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))

def MakePredictionWithImage(input_image):
  #Import image
  image = imread(input_image)
  image = cvtColor(image, COLOR_BGR2RGB)
  image = resize(image, (128, 128))

  #Normalazing image array
  image = array([image]) / 255.0

  #load model
  model= load_model('Model/covid_detector_v4', custom_objects={"precision_m": precision_m,"recall_m":recall_m,"f1_m":f1_m})

  #make prediction
  result= model.predict(image)

  #save percents
  normal,covid= [('{:.2f}'.format(result[0][0]*100)),('{:.2f}'.format(result[0][1]*100))]
  result= (0 if result[0][0] > result[0][1] else 1)

  #Create List with data
  List= {
      "Result": 'Normal' if result == 0 else "Covid",
      "NormalProbPercent":normal,
      "CovidProbPercent": covid 
  }
  return List
