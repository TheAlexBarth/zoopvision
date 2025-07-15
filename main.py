from utils import image_to_hash
import pandas as pd

if __name__ == "__main__":
    # Path to the image file
    image_path = "data/fish_image_sample/Paragobiodon lacunicolus copy.jpeg"

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
