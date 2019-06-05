from skimage import io, img_as_float, filters, data, color
img = color.rgb2grey(io.imread('/Users/Fabian/Projects/HackBay2019/hail_model/test_data_true/my_car_with_damage1.jpg', 'rb'))