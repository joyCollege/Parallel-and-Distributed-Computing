import numpy as np
import pandas as pd
import skimage.feature as feature
import time
from multiprocessing import Pool

# Function to compute GLCM features for an image
def compute_glcm_features(image, filter_name):
    """
    Computes GLCM (Gray Level Co-occurrence Matrix) features for an image.
    The image is converted to uint8, the GLCM is computed over four angles,
    and six properties are extracted.
    """
    # Convert the image from float to uint8 (0-255)
    image = (image * 255).astype(np.uint8)
    
    # Compute the GLCM using a distance of 1 for four angles (0, π/4, π/2, 3π/4)
    graycom = feature.graycomatrix(image, [1], [0, np.pi/4, np.pi/2, 3*np.pi/4],
                                   levels=256, symmetric=True, normed=True)
    
    # Compute GLCM properties and store them with keys that include the filter name
    features = {}
    for prop in ['contrast', 'dissimilarity', 'homogeneity', 'energy', 'correlation', 'ASM']:
        values = feature.graycoprops(graycom, prop).flatten()
        for i, value in enumerate(values):
            features[f'{filter_name}_{prop}_{i+1}'] = value
    return features

# Helper function to process a single filtered-images dictionary.
def process_single_filtered_image(filtered_images, tumor_presence):
    """
    Processes one dictionary of filtered images by computing GLCM features
    for each filter result, then adding a 'Tumor' key.
    """
    glcm_features = {}
    for key, image in filtered_images.items():
        glcm_features.update(compute_glcm_features(image, key))
    glcm_features['Tumor'] = tumor_presence
    return glcm_features

# Parallelized process_images function using a Pool with starmap.
def process_images_parallel(images_list, tumor_presence, num_processes=None):
    """
    Processes a list of filtered-images dictionaries in parallel, computes GLCM
    features for each, and adds a 'Tumor' key indicating presence (1) or absence (0).
    """
    start_time = time.time()
    # Prepare tasks as tuples: (filtered_images, tumor_presence)
    tasks = [(img_dict, tumor_presence) for img_dict in images_list]
    
    with Pool(processes=num_processes) as pool:
        # starmap applies the function to each tuple of arguments
        glcm_features_list = pool.starmap(process_single_filtered_image, tasks)
    
    end_time = time.time()
    print(f"Feature extraction with Pool took: {end_time - start_time:.2f} seconds")
    return glcm_features_list

def feature_extraction(yes_inputs, no_inputs):
    # Process the images with tumor presence (1) and absence (0)
    yes_glcm_features = process_images_parallel(yes_inputs, 1)
    no_glcm_features  = process_images_parallel(no_inputs, 0)

    # Combine the features into a single list and create a DataFrame
    all_glcm_features = yes_glcm_features + no_glcm_features
    dataframe = pd.DataFrame(all_glcm_features)

    print("DataFrame shape:", dataframe.shape)
    print(dataframe.head())
    return dataframe.sample(frac=1).reset_index(drop=True)