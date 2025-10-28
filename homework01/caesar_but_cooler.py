"""
Functions encrypt_growing_shift and decrypt_growing_shift accept text to cypher/decypher an integer
indicating the shift to be performed and another integer indicating growth of the shift on each
step, return encrypted/decrypted text
"""

ALPHABET_LOWER = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
ALPHABET_UPPER = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"


def encrypt_growing_shift(plaintext: str, start: int, delta: int) -> str:
    """
    Encrypts with shift = start + delta * current char index
    """
    ciphertext = ""
    current_indx = 0
    for char in plaintext:
        if char in ALPHABET_LOWER:
            final_index = (ALPHABET_LOWER.index(char) + start + (delta * current_indx)) % 33
            shifted_char = ALPHABET_LOWER[final_index]
            ciphertext += shifted_char
            current_indx += 1
        elif char in ALPHABET_UPPER:
            final_index = (ALPHABET_UPPER.index(char) + start + (delta * current_indx)) % 33
            shifted_char = ALPHABET_UPPER[final_index]
            ciphertext += shifted_char
            current_indx += 1
        else:
            ciphertext += char
    return ciphertext


def decrypt_growing_shift(ciphertext: str, start: int, delta: int) -> str:
    """
    Encrypts with shift = start + delta * current char index
    """
    plaintext = ""
    current_indx = 0
    for char in ciphertext:
        if char in ALPHABET_LOWER:
            final_index = (ALPHABET_LOWER.index(char) - start - -(delta * current_indx)) % 33
            shifted_char = ALPHABET_LOWER[final_index]
            plaintext += shifted_char
            current_indx += 1
        elif char in ALPHABET_UPPER:
            final_index = (ALPHABET_UPPER.index(char) - start - -(delta * current_indx)) % 33
            shifted_char = ALPHABET_UPPER[final_index]
            plaintext += shifted_char
            current_indx += 1
        else:
            plaintext += char
    return plaintext
