# Least significant bit (LSB) steganography
from PIL import Image
import numpy as np

# def encode_lsb(image_data, message):
     

# def decode_lsb(image_data):


def main():
    # importing the image
    print("This is LSB encoding")
    img = Image.open("data/input.jpg").convert("RGB") # reading image through pillow library
    arr = np.array(img) # converting to a numpy array
    print(arr.dtype, arr.shape) # data type and shape

    r = arr[:,:,0]
    g = arr[:,:,1]
    b = arr[:,:,2]
    lsb_planes = arr & 1
    print(r)
    # print(g)
    # print(b)
    print(lsb_planes)

if __name__ == "__main__":
    main()
