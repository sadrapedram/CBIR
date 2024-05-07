from PIL import Image
import numpy as np
import cv2 as cv
import os
from rembg import remove


# VGG16
# from urllib.request import urlopen
# from PIL import Image
# import timm
class CBIREngine:
    def __init__(self,directory='./data',w_h = (256,256)):
        self.images = []
        self.gray_images_list = []
        self.LBP_imgs = []

        self.w_h = w_h
        for filename in os.listdir(directory):
            if filename.endswith((".jpg", ".png", ".jpeg")):
                img = Image.open(os.path.join(directory, filename))
                img = img.convert("RGB")
                img = remove(img)
                self.images.append(img)
        return None
    def _resize_image(self, image, w_h):

        # pil_image = Image.open(image)
        # Convert PIL image to NumPy array
        np_image = np.array(image)
        resize_image = cv.resize(np_image,w_h)
        return resize_image
    

    def gray_images(self,image):
        # pil_image = Image.open(image)
        np_image = np.array(image)
        gray_image_one_channel = cv.cvtColor(np_image,cv.COLOR_RGB2GRAY)
        resized_gray_image = self._resize_image(gray_image_one_channel,self.w_h)
        print("chaneel number:",resized_gray_image.shape)

        return resized_gray_image


    def getLBPimage(self, gray_images):
        for img in gray_images:
            imgLBP = np.zeros_like(img)
            neighboor = 3
            for ih in range(0, img.shape[0] - neighboor):
                for iw in range(0, img.shape[1] - neighboor):
                    # Step 1: Extract a 3x3 region from the image
                    img_patch = img[ih:ih+neighboor, iw:iw+neighboor]
                    
                    # Step 2: Compute binary LBP values
                    center = img_patch[1, 1]
                    img_binary = (img_patch >= center).astype(np.uint8)
                    
                    # Step 3: Convert binary LBP values to decimal
                    img_binary_flattened = img_binary.flatten()
                    img_binary_flattened = np.delete(img_binary_flattened, 4)

                    img_decimal = np.sum(img_binary_flattened * (2 ** np.arange(8))).astype(np.uint8)
                    
                    # Assign the decimal value to the corresponding pixel
                    imgLBP[ih+1, iw+1] = img_decimal
                
            self.LBP_imgs.append(imgLBP)
        return self.LBP_imgs


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
