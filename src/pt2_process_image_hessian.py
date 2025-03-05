from skimage.filters.rank import entropy
from skimage.morphology import disk
from scipy import ndimage as nd
from skimage.filters import sobel, gabor, hessian, prewitt

from multiprocessing import Pool
from threading import Lock, Thread
from time import time
from tqdm import tqdm

def compute_hessian_for_sigma(args):
    image, sigma = args
    return hessian(image, sigmas=[sigma]) 

# Only one compute_hessian function using a pool
def compute_hessian(image, sigmas, pool):
    results = pool.map(compute_hessian_for_sigma, [(image, s) for s in sigmas])
    return results

# Create a global pool
global_hessian_pool = Pool(processes=6)

def process_single_image(image, output_list, lock, pool):
    filtered_images = {
        'Original': image,
        'Entropy': entropy(image, disk(2)),
        'Gaussian': nd.gaussian_filter(image, sigma=1),
        'Sobel': sobel(image),
        'Gabor': gabor(image, frequency=0.9)[1],
        'Hessian': compute_hessian(image, sigmas=range(1, 100, 1), pool=pool),
        'Prewitt': prewitt(image)
    }
    with lock:
        output_list.append(filtered_images)

def process_images_threaded(images, output_list, pool):
    threads = []
    lock = Lock()  # Ensure thread safety

    for image in tqdm(images):
        thread = Thread(target=process_single_image, args=(image, output_list, lock, pool))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()  # Wait for all threads to complete

def hessian_run(yes_images, no_images):
    start_time = time()

    # Create separate lists for processed images
    yes_processed_hessian = []
    no_processed_hessian = []

    # Start both sets of images in parallel using threads, passing the global pool
    t1 = Thread(target=process_images_threaded, args=(yes_images, yes_processed_hessian, global_hessian_pool))
    t2 = Thread(target=process_images_threaded, args=(no_images, no_processed_hessian, global_hessian_pool))

    t1.start()
    t2.start()

    t1.join()  
    t2.join() 

    end_time = time()
    execution_time_hessian = end_time - start_time

    # Properly close the pool after use
    global_hessian_pool.close()
    global_hessian_pool.join()

    print(f"Hessian execution time: {execution_time_hessian:.2f} seconds (combined threading and pooling)")
    return (execution_time_hessian, yes_processed_hessian, no_processed_hessian)