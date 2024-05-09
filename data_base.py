import h5py
import numpy as np
import os




class dataBase:
    def __init__(self, filename='file6.hdf5', initial_size=1000):
        # Create directory if it doesn't exist
        directory = os.path.join("data", "data_base")
        os.makedirs(directory, exist_ok=True)
        
        # Set the full filename including directory
        self.file_name = os.path.join(directory, filename)
        
        self.vector_dataset_name = "vectors"
        self.name_dataset_name = "names"
        self.image = 'image'
        self.lbp_image = "lbp_image"
        self.gray_image = "gray_image"
        self.vector_dataset_name = "vectors"

        

    def add_image(self,image_name, image,lbp_image,gray_image):
        if os.path.exists(self.file_name):       
            with h5py.File(self.file_name,'a') as hdf:
                g1 = hdf.create_group(image_name)
                g1.create_dataset(name=self.image,data=image)
                g1.create_dataset(name=self.lbp_image,data=lbp_image)
                g1.create_dataset(name=self.gray_image,data=gray_image)
        else:
            with h5py.File(self.file_name,'w') as hdf:
                g1 = hdf.create_group(image_name)
                g1.create_dataset(name=self.image,data=image)
                g1.create_dataset(name=self.lbp_image,data=lbp_image)
                g1.create_dataset(name=self.gray_image,data=gray_image)

    def get_group_names(self):
        with h5py.File(self.file_name,'r') as hdf:
            print(hdf.keys())
            return hdf.keys()
        # # Initialize HDF5 file and datasets if they don't exist
        # with h5py.File(self.filename, "a") as file:
        #     if self.vector_dataset_name not in file:
        #         file.create_dataset(self.vector_dataset_name,  dtype='float16', chunks=True)
        #     if self.name_dataset_name not in file:
        #         file.create_dataset(self.name_dataset_name, shape=(initial_size,), dtype=h5py.string_dtype(encoding='utf-8'), chunks=True)






    # def add_image(self, image):
    #     """
    #     Add a new image to the database.
        
    #     Args:
    #         name (str): The name or identifier of the image.
    #         vector (numpy.ndarray): The feature vector of the image.
            
    #     """
    #     image = np.array(image)
    #     with h5py.File(self.filename, "a") as file:
    #         # Append new vector to the 'vectors' dataset
    #         vectors_dataset = file[self.vector_dataset_name]
    #         vectors_dataset.resize((len(vectors_dataset) + 1, len(image)))
    #         vectors_dataset[-1] = image
            
    #         # Append the name to the 'names' dataset
    #         # names_dataset = file[self.name_dataset_name]
    #         # names_dataset.resize((len(names_dataset) + 1,))
    #         # names_dataset[-1] = name

    def find_image_by_name(self, name):
        """
        Retrieve the feature vector of an image by its name.
        
        Args:
            name (str): The name or identifier of the image.
        
        Returns:
            numpy.ndarray or None: The feature vector of the image, or None if the name is not found.
        """
        with h5py.File(self.filename, "r") as file:
            names_dataset = file[self.name_dataset_name]
            if name in names_dataset:
                index = np.where(names_dataset[:] == name)[0][0]
                vectors_dataset = file[self.vector_dataset_name]
                return vectors_dataset[index]
            else:
                return None


