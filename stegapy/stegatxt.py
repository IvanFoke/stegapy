import os

rus_letters = "КАМОНВЕРХСТорухаес"
eng_letters = "KAMOHBEPXCTopyxaec"


def encode_text(source_txt_name, container_txt_name, output_txt_name):
    """
    This function takes symbols from container_txt_name file and splits it to bits.
    Then it searches for letter that looks looks similar in russian and english alphabets
    in source_txt_name txt file. If current bit is 1 - it replaces eng letter with rus and
    writes it to output_txt_name txt file. Otherwise it simply puts eng symbol there.
    If letter doesn't look like english it's also simply written to output_txt_name file.

    :param source_txt_name: name of txt file containing information to be encoded
    :param container_txt_name: name of txt file containing text that would hide information
    :param output_txt_name: name of txt file containing encoded data
    :return: True if function succeeds else False
    """
    source_txt = open(source_txt_name, 'r')
    container_txt = open(container_txt_name, 'r')
    output_txt = open(output_txt_name, 'w')

    letter_to_encode = 0
    encoded_bits = 8

    while True:
        symbol_from_text = container_txt.read(1)
        if not symbol_from_text:
            break

        if symbol_from_text in eng_letters:
            if encoded_bits == 8:
                letter_to_encode = source_txt.read(1)
                if not letter_to_encode:
                    output_txt.write(symbol_from_text)

                    source_txt.close()
                    container_txt.close()
                    output_txt.close()

                    return True

                letter_to_encode = ord(letter_to_encode)
                encoded_bits = 0

            bit_from_letter = (letter_to_encode & 0b10000000) >> 7

            if bit_from_letter:
                symbol_from_text = rus_letters[eng_letters.index(symbol_from_text)]

            letter_to_encode <<= 1
            letter_to_encode %= 256
            encoded_bits += 1

        output_txt.write(symbol_from_text)

    output_txt.write(source_txt.read())

    source_txt.close()
    container_txt.close()
    output_txt.close()

    return True


def decode_text(encoded_txt_name, decoded_txt_name, symbols_to_read):
    """
    This function tries to decode symbols_to_read symbols from encoded_txt_name txt file.
    It searches for letters that looks similar in russian and english alphabets.
    If symbol is english it retrieves 0 bit, otherwise - 1. After that 8 bits are connected to 1 byte
    and written to decoded_txt_name txt file.

    :param encoded_txt_name: name of txt file containing encoded data
    :param decoded_txt_name: name of txt file containing decoded data
    :param symbols_to_read: amount of encoded symbols in encoded_txt_name
    :return: True if function succeeds else False
    """
    encoded_txt = open(encoded_txt_name, 'r')
    decoded_txt = open(decoded_txt_name, 'w', encoding='utf-8')

    read = 0
    bits_read = 0
    byte = 0

    while read < symbols_to_read:
        symbol = encoded_txt.read(1)
        if not symbol:
            encoded_txt.close()
            decoded_txt.close()

            return True

        if symbol in eng_letters:
            byte <<= 1
            bits_read += 1
        elif symbol in rus_letters:
            byte <<= 1
            byte |= 1
            bits_read += 1

        if bits_read == 8:
            decoded_txt.write(chr(byte))
            read += 1
            bits_read = byte = 0

            if chr(byte) == '\n' and len(os.linesep) == 2:
                read += 1

    encoded_txt.close()
    decoded_txt.close()

    return True
