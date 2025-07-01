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


if __name__ == "__main__":
    # Path to the image file
    image_path = "image_sample/Paragobiodon lacunicolus.jpeg"

    # Generate the image hash
    hash_code = image_to_hash(image_path)

    # Display the image with the hash code as the title
    import matplotlib.image as mpimg
    import matplotlib.pyplot as plt

    img = mpimg.imread(image_path)
    plt.imshow(img)
    plt.title(hash_code)
    plt.axis("off")  # Hide axes for better visualization
    plt.show()
