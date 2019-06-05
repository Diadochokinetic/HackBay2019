import skimage
from skimage import io
from os import listdir
from os.path import isfile, join


"""directory with image files"""
file_dir = "test_data/"

"""reads uploaded files"""
images = []
for file in [f for f in listdir(file_dir) if isfile(join(file_dir, f))]:
    images.append(io.imread(file_dir+file))


"""some dummy model"""
counter = 1
def apply_model(image):
    if counter%2!=0:
        return True
    else:
        return False

"""some dummy output"""
output = []
for i in images:
    output.append(apply_model(i))
    counter+=1

if all(out == True for out in output):
    print("Alle Bilder sind okay")
else:
    element = 1
    for out in output:
        if out == False:
            print("Bild "+str(element)+" ist scheiße")
        element+=1
    