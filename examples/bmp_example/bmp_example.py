from stegapy.stegabmp import encode_image, decode_image
import os


def main():
    text_file = "sample.txt"
    degree = 4
    encode_image("start.bmp", "encoded.bmp", text_file, degree)
    print("Encoded image with degree 4")

    to_read = os.stat(text_file).st_size
    decode_image("encoded.bmp", "result.txt", to_read, degree)
    print("Decoded image with degree 4")


if __name__ == "__main__":
    main()
