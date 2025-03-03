from skimage.filters.rank import entropy
from skimage.morphology import disk
from scipy import ndimage as nd
from skimage.filters import sobel, gabor, hessian, prewitt

from time import time
from tqdm import tqdm

def process_images(images):
    processed_images = []
    for image in tqdm(images):
        filtered_images = {
            'Original': image,
            'Entropy': entropy(image, disk(2)),
            'Gaussian': nd.gaussian_filter(image, sigma=1),
            'Sobel': sobel(image),
            'Gabor': gabor(image, frequency=0.9)[1],
            'Hessian': hessian(image, sigmas=range(1, 100, 1)),
            'Prewitt': prewitt(image)
        }
        processed_images.append(filtered_images)
    return processed_images

def sequential_run(yes_images, no_images):
    start_time = time()
    yes_processed_sequential = process_images(yes_images)
    no_processed_sequential = process_images(no_images)
    end_time = time()

    execution_time_sequential = end_time - start_time
    print(f"Sequential execution time: {execution_time_sequential} seconds")
    return (execution_time_sequential, yes_processed_sequential, no_processed_sequential)