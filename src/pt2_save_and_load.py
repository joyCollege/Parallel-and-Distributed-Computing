import pickle

def save_processed_images(processed_images, filename):
    """
    Saves processed images to a file using pickle.

    Args:
        processed_images (list): List of processed images.
        filename (str): File path to save the images.
    """
    with open(filename, 'wb') as f:
        pickle.dump(processed_images, f)
    print(f"Processed images saved to {filename}")

def load_processed_images(filename):
    """
    Loads processed images from a pickle file.

    Args:
        filename (str): File path to load the images from.

    Returns:
        list: Loaded processed images.
    """
    with open(filename, 'rb') as f:
        processed_images = pickle.load(f)
    print(f"Processed images loaded from {filename}")
    return processed_images
