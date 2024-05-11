from PIL import Image
import numpy as np
import cv2 as cv
import os
from rembg import remove
from data_base import dataBase
from skimage.filters.rank import entropy
from skimage.morphology import disk
# VGG16
# from urllib.request import urlopen
# from PIL import Image
# import timm
class CBIREngine:

    def __init__(self,directory='./data',w_h = (256,256)):
        self.cbir_db=dataBase()
        self.images_dict = {}  # Dictionary to store images with file names
        self.color_mean = {}
        self.gray_images_dict = {}
        self.LBP_imgs = {}
        self.ent_attrs = {}
        self.LBP_attrs = {}
        self.images_attrs_vector = {}
        self.w_h = w_h

        for filename in os.listdir(directory):
            if self.cbir_db.get_group_names() is not None:
                if filename not in self.cbir_db.get_group_names():

                    if filename.endswith((".jpg", ".png", ".jpeg")):
                        img = Image.open(os.path.join(directory, filename))
                        img = img.convert("RGB")
                        img = remove(img)
                        self.images_dict[filename] = img
            else:
                if filename.endswith((".jpg", ".png", ".jpeg")):
                    img = Image.open(os.path.join(directory, filename))
                    img = img.convert("RGB")
                    img = remove(img)
                    self.images_dict[filename] = img
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

        return np.array(resized_gray_image)


    def getLBPimage(self, gray_images):
        for key, img in gray_images.items():
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
                
            self.LBP_imgs[key]= imgLBP
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
    




    def vector_creator(self):

        for key in self.images_dict.keys():
            custum_features = np.array([self.color_mean[key][0],
                                        self.color_mean[key][1],
                                        self.color_mean[key][2],
                                        self.ent_attrs[key][0],
                                        self.ent_attrs[key][1],
                                        self.LBP_attrs[key][0],
                                        self.LBP_attrs[key][1],])

            self.images_attrs_vector[key] = custum_features

    def cosine_similarity(self,vector_a, vector_b):
        dot_product = np.dot(vector_a, vector_b)
        norm_a = np.linalg.norm(vector_a)
        norm_b = np.linalg.norm(vector_b)
        similarity = dot_product / (norm_a * norm_b)
        return similarity

    def image_color_mean_attrs(self):

        for key ,img in self.images_dict.items():
            b,g,r,d = Image.Image.split(img)
            mask = (np.array(d) > 0)
            stuff_r = np.array(r)[mask]
            stuff_g = np.array(g)[mask]
            stuff_b = np.array(b)[mask]
            mean_r = stuff_r.mean()
            mean_g = stuff_g.mean()
            mean_b = stuff_b.mean()
            self.color_mean[key] = [mean_r, mean_g, mean_b]
        return self.color_mean
    
    def gray_image_entropy_attrs(self):
        for key ,img in self.gray_images_dict.items():
            entropy_image = entropy(img,disk(8))
            ent_mean = entropy_image.mean()
            ent_std = entropy_image.std()
            self.ent_attrs[key] = [ent_mean,ent_std]
        return self.ent_attrs

    def LBP_image_attrs(self):
        for key ,img in self.LBP_imgs.items():
            img = np.array(img)
            ent_mean = img.mean()
            ent_std = img.std()
            self.LBP_attrs[key] = [ent_mean,ent_std]      
        return self.LBP_attrs

    def vector_comparison(self,vector):
        vector_comparison_dic = {}
        for key in self.cbir_db.get_group_names():
            key_vector = self.cbir_db.get_vector_by_group_name(key)
            similarity = self.cosine_similarity(vector,key_vector)
            vector_comparison_dic[key] = similarity
        sorted_vector_comparison_dic = dict(sorted(vector_comparison_dic.items(), key=lambda item: item[1]))
        return sorted_vector_comparison_dic
    # def fourier_transform(self):
    #     for key ,img in self.images_dict.items():
    #             np.
# class VGG16Classifier:
