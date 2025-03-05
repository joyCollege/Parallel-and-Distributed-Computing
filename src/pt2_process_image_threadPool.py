import concurrent.futures
from skimage.filters import sobel, gabor, hessian, prewitt
from skimage.filters.rank import entropy
from skimage.morphology import disk
from scipy import ndimage as nd
from time import time
from tqdm import tqdm

def process_single_image(image):
    """Apply multiple filters to a single image."""
    return {
        'Original': image,
        'Entropy': entropy(image, disk(2)),
        'Gaussian': nd.gaussian_filter(image, sigma=1),
        'Sobel': sobel(image),
        'Gabor': gabor(image, frequency=0.9)[1],
        'Hessian': hessian(image, sigmas=range(1, 100, 1)),
        'Prewitt': prewitt(image)
    }

def process_images_threaded(images):
    """Run process_single_image concurrently in threads."""
    results = []
    # Choose an appropriate max_workers (often = number_of_cpu_cores).
    # But you can experiment with different values.
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        # executor.map returns an iterator, so we wrap with tqdm to track progress
        for result in tqdm(executor.map(process_single_image, images), total=len(images)):
            results.append(result)
    return results

def threaded_run(yes_images, no_images):
    start_time = time()

    yes_processed = process_images_threaded(yes_images)
    no_processed = process_images_threaded(no_images)

    end_time = time()
    execution_time_pooling = end_time - start_time

    print(f"ThreadPooling execution time: {execution_time_pooling} seconds")
    return (execution_time_pooling, yes_processed, no_processed)

