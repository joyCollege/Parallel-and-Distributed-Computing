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

def compute_hessian(image, sigmas):
    with Pool(processes=None) as pool: 
        results = pool.map(compute_hessian_for_sigma, [(image, s) for s in sigmas])
    return results

def process_single_image(image, output_list, lock):
    filtered_images = {
        'Original': image,
        'Entropy': entropy(image, disk(2)),
        'Gaussian': nd.gaussian_filter(image, sigma=1),
        'Sobel': sobel(image),
        'Gabor': gabor(image, frequency=0.9)[1],
        'Hessian': compute_hessian(image, sigmas=range(1, 100, 1)),  # Parallelized Hessian
        'Prewitt': prewitt(image)
    }
    
    with lock:  
        output_list.append(filtered_images)

def process_images_threaded(images, output_list):
    threads = []
    lock = Lock()  # Ensure thread safety

    for image in tqdm(images):
        thread = Thread(target=process_single_image, args=(image, output_list, lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()  # Wait for all threads to complete

def hessian_run2(yes_images, no_images):
    start_time = time()

    yes_processed = []
    no_processed = []

    t1 = Thread(target=process_images_threaded, args=(yes_images, yes_processed))
    t2 = Thread(target=process_images_threaded, args=(no_images, no_processed))

    # Start both at the same time
    t1.start()
    t2.start()

    t1.join()  
    t2.join()  

    end_time = time()
    execution_time = end_time - start_time

    print(f"Hessian execution time: {execution_time:.2f} seconds (combined threading)")
    return execution_time, yes_processed, no_processed
