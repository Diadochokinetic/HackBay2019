from skimage import io, img_as_float, filters, data, color
from sklearn.decomposition import PCA
from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np
from PIL import Image
from sklearn.linear_model import LogisticRegression
from joblib import dump, load


test_true = "test_data_true/"
test_true_resized = "test_data_true_resized/"
test_false = "test_data_false/"
test_false_resized = "test_data_false_resized/"
images_true = []
images_false = []

basewidth = 100

"""true images"""
for file in [f for f in listdir(test_true) if isfile(join(test_true, f))]:
    #images.append(color.rgb2grey(io.imread(test_dir+file)))
    with open (test_true+file, 'rb') as img:
        img = Image.open(test_true+file)
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        img.save(test_true_resized+file)
        images_true.append(color.rgb2grey(io.imread(test_true_resized+file)))
#print(images[0])

df_true = pd.DataFrame({})

if images_true:
    for dim1 in range(images_true[0].shape[0]):
        for dim2 in range(images_true[0].shape[1]):
            df_true[str(dim1)+str(dim2)] = pd.Series([images_true[i][dim1][dim2] for i in range(len(images_true))])
else:
    print('keine Bilder')

"""false images"""
for file in [f for f in listdir(test_false) if isfile(join(test_false, f))]:
    #images.append(color.rgb2grey(io.imread(test_dir+file)))
    with open (test_false+file, 'rb') as img:
        img = Image.open(test_false+file)
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        img.save(test_false_resized+file)
        images_false.append(color.rgb2grey(io.imread(test_false_resized+file)))
#print(images[0])

df_false = pd.DataFrame({})

if images_false:
    for dim1 in range(images_false[0].shape[0]):
        for dim2 in range(images_false[0].shape[1]):
            df_false[str(dim1)+str(dim2)] = pd.Series([images_false[i][dim1][dim2] for i in range(len(images_false))])
else:
    print('keine Bilder')

df = pd.concat([df_true, df_false], join='inner', axis=0)
df.reset_index(inplace=True,drop=True)

df_y_true = pd.Series(np.ones(len(images_true)))
df_y_false = pd.Series(np.zeros(len(images_false)))
df_y = pd.concat([df_y_true, df_y_false], join='inner', axis=0)
df_y.reset_index(inplace=True,drop=True)
#print(df_y)

 
clf = LogisticRegression()
clf.fit(df,df_y)
test = clf.predict(df)
print(test)

dump(clf, 'model/model.joblib')


#basewidth = 500
#for img in images:
#    wpercent = (basewidth/float(img.shape[0]))
#    hsize = int((float(img.shape[1])*float(wpercent)))
#    img = img.resize((basewidth, hsize), Image.ANTIALIAS)

#print(images[0].shape)
#print(images[0][0][0][0])
#print(data.camera().shape)
#print(images[0])


#if images:
#    for dim1 in range(images[0].shape[0]):
#        for dim2 in range(images[0].shape[1]):
#            for dim3 in range(images[0].shape[2]):
#                df[dim1+dim2+dim3] = pd.Series([images[i][dim1][dim2][dim3] for i in range(len(images))])
#else:
#    print('no images')




#df = pd.DataFrame.from_records(images)
#print(df)

#for i in images:
#    print(i.dtype)

"""
files = [f for f in listdir("test_data/") if isfile(join("test_data/", f))]

for file in files:
    with open("test_data/"+file, "rb") as img_file:
        my_string = base64.b64encode(img_file.read())
        img_file.close()
    #print(my_string)
"""