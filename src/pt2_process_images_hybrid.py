import concurrent.futures
import os
from math import ceil
from skimage.filters.rank import entropy
from skimage.morphology import disk
from scipy import ndimage as nd
from skimage.filters import sobel, gabor, hessian, prewitt
from time import time
from tqdm import tqdm

NUM_PROCESSES = 6
NUM_THREADS = 4  # or however many you want per process

def process_single_image(image):
    """Apply multiple filters to a single image."""
    return {
        'Original': image,
        'Entropy': entropy(image, disk(2)),
        'Gaussian': nd.gaussian_filter(image, sigma=1),
        'Sobel': sobel(image),
        'Gabor': gabor(image, frequency=0.9)[1],
        'Hessian': hessian(image, sigmas=range(1, 100, 1)),  # The slow one
        'Prewitt': prewitt(image),
    }

def process_images_in_process(images):
    """
    This function is the target for each process.
    It can internally spin up threads to handle the images in parallel.
    """
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        # Executor map returns an iterator over results
        for result in executor.map(process_single_image, images):
            results.append(result)
    return results

def chunk_list(lst, n):
    """Simple helper to chunk a list into n roughly equal parts."""
    chunk_size = ceil(len(lst) / n)
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

def process_images_hybrid(images):
    """
    Main driver function:
    1) Split all images into 6 chunks
    2) Dispatch each chunk to a separate process
    3) Within each process, use a ThreadPool to process those images
    """
    # If fewer than 6 processes, or you want exactly 6, up to you:
    n_processes = min(NUM_PROCESSES, len(images))  # or just = 6 if you insist on 6
    image_chunks = list(chunk_list(images, n_processes))

    results = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=n_processes) as executor:
        # Each chunk gets processed in a separate process
        future_to_chunk = {executor.submit(process_images_in_process, chunk): chunk for chunk in image_chunks}

        # Collect results
        for future in concurrent.futures.as_completed(future_to_chunk):
            results.extend(future.result())

    return results

def hybrid_run(yes_images, no_images):
    """
    Runs image processing using a hybrid approach and measures execution time.

    Args:
        yes_images (list of ndarray): List of positive-class images.
        no_images (list of ndarray): List of negative-class images.

    Returns:
        tuple: Execution time, processed positive-class images, processed negative-class images.
    """

    start_time = time()

    yes_processed = process_images_hybrid(yes_images)
    no_processed = process_images_hybrid(no_images)

    end_time = time()
    execution_time_pooling = end_time - start_time

    print(f"Hybrid execution time: {execution_time_pooling} seconds")
    return (execution_time_pooling, yes_processed, no_processed)
