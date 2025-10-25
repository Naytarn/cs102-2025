"""
Functions encrypt_caesar and decrypt_caesar accept text to cypher/decypher and an integer indicating
the shift to be performed, return encrypted/decrypted text
"""


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for char in plaintext:
        if "a" <= char <= "z":
            start = ord("a")
            shifted_char = chr(((ord(char) + shift - start) % 26) + start)
            ciphertext += shifted_char
        elif "A" <= char <= "Z":
            start = ord("A")
            shifted_char = chr(((ord(char) + shift - start) % 26) + start)
            ciphertext += shifted_char
        else:
            ciphertext += char
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for char in ciphertext:
        if "a" <= char <= "z":
            start = ord("a")
            shifted_char = chr(((ord(char) - shift - start) % 26) + start)
            plaintext += shifted_char
        elif "A" <= char <= "Z":
            start = ord("A")
            shifted_char = chr(((ord(char) - shift - start) % 26) + start)
            plaintext += shifted_char
        else:
            plaintext += char
    return plaintext
