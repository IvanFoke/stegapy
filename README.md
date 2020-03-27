# Steganography with Python
StegaPy is a simple Python library for dealing with basic steganographic algorithms.
This library is exclusively educational, it carries only the goal of showing 
that steganography is very interesting, especially if you  work with it 
using Python programming language.

## Modes
**1. StegaBmp**\
This module helps you to encode text data in 24-bit BMP image.
The idea is to take every byte of image and replace some smaller bits with
your data. After this action image will look like original if you replace small amount
of bits.

**2. StegaTxt**\
This module helps you to encode text data in another text file using letters 
that look similar in both english and russian alphabets.\
Encoded bit 1 - english letter is replaced with russian.\
Encoded bit 0 - english letter is not replaced.

**3. StegaWav**\
This module helps you to encode text data in WAV audio file.
The idea is to take every sample (2 bytes) from audio and replace some smaller bits with
your data. After this action audio will look like original if you replace small amount
of bits.

## Usage
```python
from stegapy.stegatxt import encode_text, decode_text
import os


text_file = "to_encode.txt"
encode_text(text_file, "letters_source.txt", "encoded.txt")

to_read = os.stat(text_file).st_size
decode_text("encoded.txt", "decoded.txt", to_read)
```

Check 'examples' folder to see another examples.

