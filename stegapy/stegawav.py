import os

WAV_HEADER_SIZE = 44


def encode_wav(input_wav_name, output_wav_name, text_file, degree):
    """
    This function reads text from the text_file file and encodes it
    by bits from input_wav_name to output_wav_name.
    Single portion of data can be written only in 2 bytes by one so maximum
    information portion size is 16 bits.
    Thus text size should be less than (data_size * degree / 16)

    :param input_wav_name: name of WAV input audio file
    :param output_wav_name: name of WAV output audio file
    :param text_file: name of input text file
    :param degree: number of bits from 2 bytes (1/2/4/8/16) that are taken to encode text data in audio.
    :return: True if function succeeds else False
    """
    if degree not in [1, 2, 4, 8, 16]:
        print("Degree value can be only 1/2/4/8/16")
        return False

    input_wav = open(input_wav_name, 'rb')
    text_len = os.stat(text_file).st_size

    wav_header = input_wav.read(WAV_HEADER_SIZE)
    data_size = int.from_bytes(wav_header[40:44], byteorder='little')

    if text_len > data_size * degree / 16:
        print("Too big text to encode")
        input_wav.close()
        return False

    text = open(text_file, 'r')
    output_wav = open(output_wav_name, 'wb')
    output_wav.write(wav_header)

    data = input_wav.read(data_size)
    text_mask, sample_mask = create_masks(degree)

    while True:
        txt_symbol = text.read(1)
        if not txt_symbol:
            break

        txt_symbol = ord(txt_symbol)
        txt_symbol <<= 8

        if degree == 16:
            another_symbol = text.read(1)
            if not another_symbol:
                another_symbol = 0b0
            else:
                print("another {0}, bin {1:b}".format(another_symbol, ord(another_symbol)))
                another_symbol = ord(another_symbol)

            txt_symbol |= another_symbol

        for step in range(0, 16, degree):
            if step == 8 and not txt_symbol:
                break

            sample = int.from_bytes(data[:2], byteorder='little') & sample_mask
            data = data[2:]

            bits = txt_symbol & text_mask
            bits >>= (16 - degree)

            sample |= bits

            output_wav.write(sample.to_bytes(2, byteorder='little'))
            txt_symbol = (txt_symbol << degree) % 65536

    output_wav.write(data)
    output_wav.write(input_wav.read())

    input_wav.close()
    output_wav.close()

    return True


def decode_wav(input_wav_name, text_file, degree, symbols_to_read):
    """
    This function takes symbols_to_read bytes from encoded WAV audio file and
    retrieves hidden information from them with a given degree.
    Single portion of data can be written only in 2 bytes by one so maximum
    information portion size is 16 bits.
    Thus text size should be less than (data_size * degree / 16)

    :param input_wav_name: name of WAV input audio file
    :param text_file: name of input text file
    :param degree: number of bits from 2 bytes (1/2/4/8/16) that are taken to encode text data in audio.
    :param symbols_to_read:
    :return: True if function succeeds else False
    """
    if degree not in [1, 2, 4, 8, 16]:
        print("Degree value can be only 1/2/4/8/16")
        return False

    input_wav = open(input_wav_name, 'rb')

    wav_header = input_wav.read(WAV_HEADER_SIZE)
    data_size = int.from_bytes(wav_header[40:44], byteorder='little')

    if symbols_to_read >= data_size * degree / 16:
        print("Too many symbols to read")
        input_wav.close()
        return False

    text = open(text_file, 'w', encoding='utf-8')

    _, sample_mask = create_masks(degree)
    sample_mask = ~sample_mask

    data = input_wav.read(data_size)

    read = 0
    while read < symbols_to_read:
        two_symbols = 0
        for step in range(0, 16, degree):
            sample = int.from_bytes(data[:2], byteorder='little') & sample_mask
            data = data[2:]

            two_symbols <<= degree
            two_symbols |= sample

        first_symbol = two_symbols >> 8
        text.write(chr(first_symbol))
        read += 1

        if chr(first_symbol) == '\n' and len(os.linesep) == 2:
            read += 1

        if symbols_to_read - read > 0:
            second_symbol = two_symbols & 0b0000000011111111
            text.write(chr(second_symbol))
            read += 1

            if chr(second_symbol) == '\n' and len(os.linesep) == 2:
                read += 1

    text.close()
    input_wav.close()
    return True


def create_masks(degree):
    """
    Create masks for taking bits from text bytes and
    putting them to image bytes.

    :param degree: number of bits from byte that are taken to encode text data in audio
    :return:  mask for a text and a mask for a sample
    """
    text_mask = 0b1111111111111111
    sample_mask = 0b1111111111111111

    text_mask <<= (16 - degree)
    text_mask %= 65536
    sample_mask >>= degree
    sample_mask <<= degree

    return text_mask, sample_mask
