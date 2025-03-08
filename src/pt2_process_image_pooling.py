from skimage.filters.rank import entropy
from skimage.morphology import disk
from scipy import ndimage as nd
from skimage.filters import sobel, gabor, hessian, prewitt

from multiprocessing import Pool
from time import time
from tqdm import tqdm

def process_single_image(image):
    """
    Applies multiple filters to an image and returns a dictionary of results.

    Args:
        image (ndarray): Input grayscale image.

    Returns:
        dict: Processed images with various filters applied.
    """
    filtered_images = {
        'Original': image,
        'Entropy': entropy(image, disk(2)),
        'Gaussian': nd.gaussian_filter(image, sigma=1),
        'Sobel': sobel(image),
        'Gabor': gabor(image, frequency=0.9)[1],
        'Hessian': hessian(image, sigmas=range(1, 100, 1)), 
        'Prewitt': prewitt(image)
    }
    return filtered_images

def process_images_pooling(images):
    """
    Processes a list of images in parallel using multiprocessing.

    Args:
        images (list of ndarray): List of grayscale images.

    Returns:
        list: Processed images with applied filters.
    """
    with Pool() as pool:
        processed_images = list(tqdm(pool.imap(process_single_image, images), total=len(images)))
    return processed_images

def pooling_run(yes_images, no_images):
    """
    Runs image processing in parallel for two datasets and measures execution time.

    Args:
        yes_images (list of ndarray): List of positive-class images.
        no_images (list of ndarray): List of negative-class images.

    Returns:
        tuple: Execution time, processed positive-class images, processed negative-class images.
    """
    start_time = time()

    yes_processed_pooling = process_images_pooling(yes_images)
    no_processed_pooling = process_images_pooling(no_images)

    end_time = time()
    execution_time_pooling = end_time - start_time

    print(f"Pooling execution time: {execution_time_pooling} seconds")
    return (execution_time_pooling, yes_processed_pooling, no_processed_pooling)
