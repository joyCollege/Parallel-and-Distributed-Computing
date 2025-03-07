from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from numpy import array_split, concatenate
from skimage.filters.rank import entropy
from skimage.morphology import disk
from scipy import ndimage as nd
from skimage.filters import sobel, gabor, hessian, prewitt
from time import time
from tqdm import tqdm
import numpy as np

# 6-core VM
NUM_WORKERS = 6

def compute_hessian_for_chunk(chunk):
    """
    Applies the Hessian filter to a chunk of the image using sigma values from 1 to 99.
    """
    return hessian(chunk, sigmas=range(1, 100, 1))

def compute_hessian(image):
    """
    Splits the image into NUM_WORKERS chunks and computes the Hessian filter
    on each chunk in parallel using ProcessPoolExecutor.
    The results are then concatenated into a full image.
    """
    # Split the image into nearly equal parts (typically along rows)
    chunks = array_split(image, NUM_WORKERS)
    
    with ProcessPoolExecutor(max_workers=NUM_WORKERS) as executor:
        # Process each chunk in parallel and collect the results
        chunk_results = list(executor.map(compute_hessian_for_chunk, chunks))
    
    # Concatenate the processed chunks back into a full image
    hessian_img = concatenate(chunk_results)
    return hessian_img

def process_single_image(image):
    filtered_images = {
        'Original': image,
        'Entropy': entropy(image, disk(2)),
        'Gaussian': nd.gaussian_filter(image, sigma=1),
        'Sobel': sobel(image),
        'Gabor': gabor(image, frequency=0.9)[1],
        'Hessian': compute_hessian(image), 
        'Prewitt': prewitt(image)
    }
    return filtered_images

def process_images(images):
    """
    Processes a list of images in parallel using ThreadPoolExecutor.
    Each image is processed concurrently.
    """
    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        processed = list(tqdm(executor.map(process_single_image, images), total=len(images)))
    return processed

def thread_run(yes_images, no_images):
    """
    Processes yes_images and no_images sequentially.
    Returns the total execution time along with the processed results for each set.
    """
    start_time = time()
    
    yes_processed = process_images(yes_images)
    no_processed = process_images(no_images)
    
    end_time = time()
    execution_time = end_time - start_time
    print(f"Hessian thread execution time: {execution_time} seconds")
    return execution_time, yes_processed, no_processed




