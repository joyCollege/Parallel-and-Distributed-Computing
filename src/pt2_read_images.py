
from glob import glob
from cv2 import imread, IMREAD_GRAYSCALE
from re import search, IGNORECASE

def read_images(images_path):
    """
    Reads all images from a specified path using OpenCV.

    Parameters:
        - images_path (str): The path to the directory containing the images.
    Returns:
        - images (list): A list of images read from the directory.
    """
    images = []
    for file_path in images_path:
        image = imread(file_path, IMREAD_GRAYSCALE)
        if image is not None:
                images.append(image)
    return images

def read_path():
    """
    Reads image file paths from the dataset directories and loads the images.

    Returns:
        tuple: Lists of loaded images from the 'yes' and 'no' categories.
    """
    dataset_path = './data/brain_tumor_dataset/'

    # List all image files in the 'yes' and 'no' directories
    yes_images = [img for img in glob(dataset_path + 'yes/*') if search(r'\.jpg$', img, IGNORECASE)]
    no_images = [img for img in glob(dataset_path + 'no/*') if search(r'\.jpg$', img, IGNORECASE)]

    # yes_images = glob(dataset_path + 'yes/*.jpg')
    # no_images = glob(dataset_path + 'no/*.jpg')
    
    print(f"Number of 'yes' images: {len(yes_images)}")
    print(f"Number of 'no' images: {len(no_images)}\n")
    return (read_images(yes_images),  read_images(no_images))
