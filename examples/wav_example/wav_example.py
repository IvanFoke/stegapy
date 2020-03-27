from stegapy.stegawav import encode_wav, decode_wav
import os


def main():
    degree = 4
    text_file = f"txt{degree}.txt"
    encode_wav("hp+.wav", f"hp+{degree}.wav", text_file, degree)
    print(f"Encoded WAV with degree {degree}")

    to_read = os.stat(text_file).st_size
    decode_wav(f"hp+{degree}.wav", f"output{degree}.txt", degree, to_read)
    print(f"Decoded WAV with degree {degree}")


if __name__ == "__main__":
    main()

