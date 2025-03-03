import pickle

def save_processed_images(processed_images, filename):
    with open(filename, 'wb') as f:
        pickle.dump(processed_images, f)
    print(f"Processed images saved to {filename}")

def load_processed_images(filename):
    with open(filename, 'rb') as f:
        processed_images = pickle.load(f)
    print(f"Processed images loaded from {filename}")
    return processed_images
