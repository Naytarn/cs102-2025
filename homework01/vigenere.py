"""
Functions encrypt_vigenere and decrypt_vigenere accept text to cypher/decypher and a keyword,
each letter's index indicating the shift to be performed, return encrypted/decrypted text
"""
ALPHABET_LENGTH = 26


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    indx = 0
    for char in plaintext:
        if char.isalpha():
            if char.islower():
                start = ord("a")
            else:
                start = ord("A")
            keyletter = keyword[indx % len(keyword)]
            shift = ord(keyletter) - start
            shifted_char = chr(((ord(char) + shift - start) % ALPHABET_LENGTH) + start)
            ciphertext += shifted_char
        else:
            ciphertext += char
        indx += 1
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    indx = 0
    for char in ciphertext:
        if char.isalpha():
            if char.islower():
                start = ord("a")
            else:
                start = ord("A")
            keyletter = keyword[indx % len(keyword)]
            shift = ord(keyletter) - start
            shifted_char = chr(((ord(char) - shift - start) % ALPHABET_LENGTH) + start)
            plaintext += shifted_char
        else:
            plaintext += char
        indx += 1
    return plaintext
