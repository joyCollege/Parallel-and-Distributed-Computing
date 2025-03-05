from skimage.filters.rank import entropy
from skimage.morphology import disk
from scipy import ndimage as nd
from skimage.filters import sobel, gabor, hessian, prewitt
from multiprocessing import Pool, cpu_count
from time import time
from tqdm import tqdm

# Function to apply Hessian filter on a given range of sigma values
def apply_hessian(image, sigma_range):
    return hessian(image, sigmas=sigma_range)

def process_images(images):
    processed_images = []
    num_workers = min(cpu_count(), len(images))  # Use available cores but not exceeding image count
    
    with Pool(num_workers) as pool:
        for image in tqdm(images):
            sigma_ranges = [range(i, i + 10) for i in range(1, 100, 10)]  # Split sigma range into chunks
            hessian_results = pool.starmap(apply_hessian, [(image, sigma) for sigma in sigma_ranges])
            
            filtered_images = {
                'Original': image,
                'Entropy': entropy(image, disk(2)),
                'Gaussian': nd.gaussian_filter(image, sigma=1),
                'Sobel': sobel(image),
                'Gabor': gabor(image, frequency=0.9)[1],
                'Hessian': hessian_results,  # Aggregated parallel Hessian results
                'Prewitt': prewitt(image)
            }
            processed_images.append(filtered_images)
    
    return processed_images

def range_run(yes_images, no_images):
    start_time = time()
    yes_processed_range = process_images(yes_images)
    no_processed_range = process_images(no_images)
    end_time = time()

    execution_time_range = end_time - start_time
    print(f"Hessian rangee: {execution_time_range} seconds")
    return execution_time_range, yes_processed_range, no_processed_range
