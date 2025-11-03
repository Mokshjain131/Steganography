# Least significant bit (LSB) steganography
from PIL import Image
import numpy as np

def encode_lsb(arr: np.ndarray, msg: str, channels: tuple[int, ...] = (0,1,2)) -> np.ndarray:
    print('encoding function')
    # accessing the bits of the image
    print(arr.dtype, arr.shape) # data type and shape
    r = arr[:,:,0]
    g = arr[:,:,1]
    b = arr[:,:,2]
    lsb_planes = arr & 1 # lsb of 3 planes for every pixel 
    # print(r)
    # print(g)
    # print(b)
    # print(r.shape)
    # print(lsb_planes)
    # print(lsb_planes[:,:,0])
    # print(lsb_planes[:,:,0].shape)
    flat_planes = lsb_planes[:,:,channels].reshape(-1)
    # print(flat_planes)

    bits = np.unpackbits(np.frombuffer(msg, dtype=np.uint8), bitorder='big') # converting message to bits
    # print(len(bits))
    # print(bits.shape)

    header = np.unpackbits(np.frombuffer((len(bits) // 8).to_bytes(4, 'big'), dtype=np.uint8), bitorder='big') # making the header
    # print(len(header))
    # print(header.shape)

    payload = np.concatenate([header, bits]) # merging both header and message bits
    # print(len(payload))
    # print(payload.shape)

    flat_planes[:payload.size] = payload 
    mask = np.uint8(0xFE) # ~1 representation
    # changing the image array and using message encoded lsb flat array
    arr[:,:,channels] = (arr[:,:,channels] & mask) | flat_planes.reshape(arr.shape[0], arr.shape[1], len(channels))

    return arr

def decode_lsb(stego_arr: np.ndarray, channels: tuple[int, ...] = (0,1,2)) -> str:
    print('decoding function')
    flat = stego_arr[:,:,channels].reshape(-1) # accessing flattened bytes of all channels for all pixels
    bits = flat & 1 # getting the lsb for all bytes in the flattened array

    if bits.size < 32:
        raise ValueError('no header present') # when the bits size is less than the header
    length_bytes = np.packbits(bits[:32], bitorder='big') # header bits
    msg_len = int.from_bytes(length_bytes.tobytes(), 'big') # convert header bits to int (message length)

    total_bits = msg_len * 8
    start = 32
    end = start + total_bits # message location
    if end > bits.size:
        raise ValueError('message truncated') # when message length is greater than the image length
    msg_bits = bits[start:end] # accessing the message bits

    msg_bytes = np.packbits(msg_bits, bitorder='big').tobytes() # converting message bits to bytes

    return msg_bytes.decode('utf-8') # decoding based on utf-8 standard

def main():
    # importing the image
    print('This is LSB encoding')
    img = Image.open('data/input.png').convert('RGB') # reading image through pillow library
    arr = np.array(img) # converting to a numpy array

    msg = b'I love dogs' # message to encode
    # print(msg)

    stego = encode_lsb(arr, msg, channels=(0,1,2)) # encoding the message in the image
    Image.fromarray(stego).save('data/stego.png') # saving the modified image

    stego_arr = np.array(Image.open('data/stego.png').convert('RGB'))
    message = decode_lsb(stego_arr, channels=(0,1,2)) # decoding the message
    print(message)

if __name__ == "__main__":
    main()
