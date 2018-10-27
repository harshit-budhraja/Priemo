import keras
import librosa
import os
import pickle
import json
import librosa
import glob 
import numpy as np
import pandas as pd
from keras.models import model_from_json
from sklearn.preprocessing import LabelEncoder

#load the model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("Emotion_Voice_Detection_Model.h5")
print("Loaded model from disk")
 
opt = keras.optimizers.rmsprop(lr=0.00001, decay=1e-6)
loaded_model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

#load the input wav file and preprocess
X, sample_rate = librosa.load('output10.wav', res_type='kaiser_fast',duration=2.5,sr=22050*2,offset=0.5)
sample_rate = np.array(sample_rate)
mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=13),axis=0)
featurelive = mfccs

livedf2 = featurelive
livedf2= pd.DataFrame(data=livedf2)
livedf2 = livedf2.stack().to_frame().T

twodim= np.expand_dims(livedf2, axis=2)
livepreds = loaded_model.predict(twodim, batch_size=32, verbose=1)
livepreds1=livepreds.argmax(axis=1)
liveabc = livepreds1.astype(int).flatten()

#load the label encoder
pfile = open("labels921.pickle", 'rb')
labels = pickle.load(pfile)
pfile.close()

lb = LabelEncoder()
lb.fit(labels)
prediction = (lb.inverse_transform((liveabc)))
s_p = prediction[0].split('_')
jdata = {
  'gender' : s_p[0], 
  'emotion' : s_p[1]
}

jsonOUT = json.dumps(jdata)

with open('JSON_S2E.json', 'w') as f:
     json.dump(jsonOUT, f)
