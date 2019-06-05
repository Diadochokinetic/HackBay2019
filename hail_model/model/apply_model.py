from skimage import io, img_as_float, filters, data, color
from sklearn.decomposition import PCA
from os import listdir, remove
from os.path import isfile, join
import pandas as pd
import numpy as np
from PIL import Image
from sklearn.neural_network import MLPClassifier
from joblib import dump, load
from flask import Flask, request
import json

def apply_model(test_dir = "model/data/", test_dir_resized = "model/data_resized/"):

    images = []

    basewidth = 100
    for file in [f for f in listdir(test_dir) if isfile(join(test_dir, f))]:
        #images.append(color.rgb2grey(io.imread(test_dir+file)))
        with open (test_dir+file, 'rb') as img:
            img = Image.open(test_dir+file)
            wpercent = (basewidth/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((basewidth, hsize), Image.ANTIALIAS)
            img.save(test_dir_resized+file)
            images.append(color.rgb2grey(io.imread(test_dir_resized+file)))
    #print(images[0])

    df = pd.DataFrame({})

    if images:
        for dim1 in range(images[0].shape[0]):
            for dim2 in range(images[0].shape[1]):
                df[str(dim1)+str(dim2)] = pd.Series([images[i][dim1][dim2] for i in range(len(images))])
    else:
        print('keine Bilder')

    model = load('model/model.joblib')

    output = pd.Series(model.predict(df)).apply(lambda x: True if x == 1 else False)
    #print(output)

    out_dict = {}
    counter=0
    for file in [f for f in listdir(test_dir) if isfile(join(test_dir, f))]:
        out_dict[file] = str(output[counter])
        counter+=1
        remove(test_dir+file)

    for file in [f for f in listdir(test_dir) if isfile(join(test_dir, f))]:
        remove(test_dir+file)

    for file in [f for f in listdir(test_dir_resized) if isfile(join(test_dir_resized, f))]:
        remove(test_dir_resized+file)

    return json.dumps(out_dict)
    
#print(apply_model())