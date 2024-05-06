import h5py
import numpy as np




class dataBase:
    def __init__(self, filename):
        self.filename = filename
        self.vector_dataset_name = "vectors"
        self.name_dataset_name = "names"
        
        # Initialize HDF5 file and datasets if they don't exist
        with h5py.File(self.filename, "a") as file:
            if self.vector_dataset_name not in file:
                file.create_dataset(self.vector_dataset_name, dtype='float32', maxshape=(None, None))
            if self.name_dataset_name not in file:
                file.create_dataset(self.name_dataset_name, dtype=h5py.string_dtype(encoding='utf-8'), maxshape=(None,))

    def add_image(self, name, vector):
        """
        Add a new image to the database.
        
        Args:
            name (str): The name or identifier of the image.
            vector (numpy.ndarray): The feature vector of the image.
        """
        with h5py.File(self.filename, "a") as file:
            # Append new vector to the 'vectors' dataset
            vectors_dataset = file[self.vector_dataset_name]
            vectors_dataset.resize((len(vectors_dataset) + 1, len(vector)))
            vectors_dataset[-1] = vector
            
            # Append the name to the 'names' dataset
            names_dataset = file[self.name_dataset_name]
            names_dataset.resize((len(names_dataset) + 1,))
            names_dataset[-1] = name

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

