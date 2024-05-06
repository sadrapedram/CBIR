from PIL import Image
import numpy as np
import cv2 as cv
import os
# VGG16
# from urllib.request import urlopen
# from PIL import Image
# import timm
class CBIREngine:
    def __init__(self,directory='./data'):
        self.images = []
        for filename in os.listdir(directory):
            if filename.endswith((".jpg", ".png", ".jpeg")):
                img = Image.open(os.path.join(directory, filename))
                img = img.convert("RGB")
                self.images.append(img)
        return None
    def resize_image(self, image, w_h):

        pil_image = Image.open(image)
        # Convert PIL image to NumPy array
        np_image = np.array(pil_image)
        resize_image = cv.resize(np_image,w_h)
        return resize_image
    

    def gray_images(self,image):
        pil_image = Image.open(image)
        np_image = np.array(pil_image)
        gray_image_one_channel = cv.cvtColor(np_image,cv.COLOR_RGB2GRAY)
        print("chaneel number:",gray_image_one_channel.shape)

        return gray_image_one_channel
    
    def mean_filter(self, image,pixel):
        pil_image = Image.open(image)
        np_image = np.array(pil_image)
        gray_image = cv.cvtColor(np_image, cv.COLOR_RGB2GRAY)
        filtered_image = cv.blur(gray_image,(pixel,pixel))
        return filtered_image
    
    def custum_compute_sobel(self, image):
        # Sobel operators for computing gradients
        sobel_x = np.array([[-.1, 0, .1],
                            [-.2, 0, .2],
                            [-.1, 0, .1]])
        
        sobel_y = np.array([[-.1, -.2, -.1],
                            [ 0,  0,  0],
                            [ .1,  .2,  .1]])
        
        # Convolve image with Sobel operators
        gradient_x = self._convolve2d(image, sobel_x)
        gradient_y = self._convolve2d(image, sobel_y)
        
        # Compute magnitude of the gradient
        magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
        magnitude = (255/magnitude.max())*magnitude 
        # print(magnitude)
        return magnitude.astype(np.uint8) 
    
    def vector_creator():
        pass



# class VGG16Classifier:
