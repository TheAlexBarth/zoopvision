import imagehash
from PIL import Image


def image_to_hash(image_path):
    """
    Compute the perceptual hash (phash) of an image given its file path.
    Args:
        image_path (str): Path to the image file.
    Returns:
        str: The perceptual hash of the image as a string.
    """
    image = Image.open(image_path)
    hash_code = imagehash.phash(image)
    return str(hash_code)
