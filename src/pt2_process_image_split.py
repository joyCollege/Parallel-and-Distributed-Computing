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
    Splits the image into NUM_WORKERS chunks and computes the Hessian filter on each chunk
    in parallel using a ProcessPoolExecutor. The results are then concatenated into a full image.
    """
    chunks = array_split(image, NUM_WORKERS)
    with ProcessPoolExecutor(max_workers=NUM_WORKERS) as executor:
        chunk_results = list(executor.map(compute_hessian_for_chunk, chunks))
    hessian_img = concatenate(chunk_results)
    return hessian_img

def process_single_image(image):
    """
    Applies various filters to a single image concurrently using ThreadPoolExecutor.
    The Hessian filter is processed separately using a ProcessPoolExecutor.
    """
    result = {}
    result['Original'] = image

    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        futures = {
            'Entropy': executor.submit(entropy, image, disk(2)),
            'Gaussian': executor.submit(nd.gaussian_filter, image, 1),
            'Sobel': executor.submit(sobel, image),
            'Gabor': executor.submit(lambda img: gabor(img, frequency=0.9)[1], image),
            'Prewitt': executor.submit(prewitt, image),
            'Hessian': executor.submit(compute_hessian, image),
        }

        for key, future in futures.items():
            result[key] = future.result()

    return result

def process_images(images):
    """
    Processes a list of images in parallel using a ProcessPoolExecutor.
    Each image is processed concurrently using process_single_image.
    """
    with ProcessPoolExecutor(max_workers=NUM_WORKERS) as executor:
        processed = list(tqdm(executor.map(process_single_image, images), total=len(images)))
    return processed

def split_run(yes_images, no_images):
    """
    Processes yes_images and no_images sequentially.
    Returns the total execution time along with the processed results for each set.
    """
    start_time = time()
    yes_processed = process_images(yes_images)
    no_processed = process_images(no_images)
    total_time = time() - start_time
    print(f"Splitting thread execution time: {total_time} seconds")
    return total_time, yes_processed, no_processed

