from stegapy.stegatxt import encode_text, decode_text
import os


def main():
    text_file = "to_encode.txt"
    encode_text(text_file, "letters_source.txt", "encoded.txt")
    print("Encoded text")

    to_read = os.stat(text_file).st_size
    decode_text("encoded.txt", "decoded.txt", to_read)
    print("Decoded text")


if __name__ == "__main__":
    main()

