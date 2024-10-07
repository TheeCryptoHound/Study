# Obtained from: https://github.com/LeoMartinezTAMUK/K-Rail_Fence_Cipher_Encryption-Decryption
import argparse
import os

# Function to read an environment variable
def read_env_variable(var_name):
    return os.getenv(var_name)

# Method for performing K-Rail Fence Encryption on given plaintext
def encryptRailFence(plaintext, key):
    # Filter out spaces from the plaintext (spaces are ignored for encipherment)
    plaintext = "".join(plaintext.split())

    # Creation of the matrix 'rail' filled with placeholders (ph)
    rail = [['ph' for i in range(len(plaintext))] # length of plaintext = number of columns
            for j in range(key)] # key = number of rows

    # Initialized information for sense of direction and values of row/col
    direction_down = False
    col = 0
    row = 0
    for i in range(len(plaintext)):
        # Check the direction of flow (is it the first row or last row?)
        if (row == 0) or (row == key - 1):
            direction_down = not direction_down # Invert direction if yes

        # Begin filling the cipher matrix
        rail[row][col] = plaintext[i]
        col += 1

        # Change rows based on the flag variable 'direction_down' logic
        if direction_down:
            row += 1
        else:
            row -= 1

    # After the matrix has been filled, we can now extract that information to create the ciphertext
    ciphertext = []
    for i in range(key): # Rows
        for j in range(len(plaintext)): # Columns
            if rail[i][j] != 'ph': # If the value is not a placeholder, append it to the ciphertext list
                ciphertext.append(rail[i][j])
    return "".join(ciphertext) # Convert the ciphertext list into a singular string

#-------------------------------------------------------------------------------
# Decryption

# Method for performing n-Rail Fence Decryption on given ciphertext
def decryptRailFence(ciphertext, key):

    # Creation of the matrix 'rail' filled with placeholders (similar to encryption algorithm)
    rail = [['*' for i in range(len(ciphertext))]
            for j in range(key)]

    ## Initialized information for sense of direction and values of row/col
    direction_down = None
    col = 0
    row = 0

    # Create markers on the matrix with 'mkr'
    for i in range(len(ciphertext)):
        if row == 0: # Highest level row
            direction_down = True
        if row == key - 1: # Lowest level row
            direction_down = False

        # Begin filling the matrix with markers based on the key and length of text
        rail[row][col] = 'mkr'
        col += 1

        # Change row index based on the flag variable 'direction_down' logic
        if direction_down:
            row += 1
        else:
            row -= 1

    # For loop to begin filling marked spots with characters from the ciphertext
    # idx = indexing for ciphertext, i = row index, j = col index
    idx = 0
    for i in range(key):
        for j in range(len(ciphertext)):
            if ((rail[i][j] == 'mkr') and
                    (idx < len(ciphertext))):
                rail[i][j] = ciphertext[idx]
                idx += 1

    # Begin reading the filled rail matrix in a zigzag manner
    plaintext = []
    col = 0
    row = 0
    for i in range(len(ciphertext)):
        if row == 0: # Highest level row
            direction_down = True
        if row == key - 1: # Lowest level row
            direction_down = False

        # Begin constructing the plaintext
        plaintext.append(rail[row][col])
        col += 1

        # Change rows based on the flag variable 'direction_down' logic
        if direction_down:
            row += 1
        else:
            row -= 1
    return "".join(plaintext) # Convert the plaintext list into a singular string

def main():
    parser = argparse.ArgumentParser()

    choice = read_env_variable('TYPE')
    text = read_env_variable('TEXT')
    try:
        key = int(read_env_variable('KEY'))
    except TypeError:
        key = None

    if choice:
        parser.add_argument('--type', choices=['encrypt', 'decrypt'], help='Choice of action. encrypt / decrypt', required=False, default=choice)
    else:
        parser.add_argument('--type', required=True, choices=['encrypt', 'decrypt'], help='Choice of action. encrypt / decrypt')

    if text:
        parser.add_argument('--text', help='Plaintext to encrypt / cipher text to decrypt', required=False, default=text)
    else:
        parser.add_argument('--text', required=True, help='Plaintext to encrypt / cipher text to decrypt')

    if key:
        parser.add_argument('--key', type=int, help='Key used to encrypt / decrypt', required=False, default=int(key))
    else:
        parser.add_argument('--key', type=int, required=True, help='Key used to encrypt / decrypt')

    args = parser.parse_args()
    choice = args.type
    text = args.text
    key = args.key

    if choice == 'encrypt':
        print(f'Encrypting {text} with key {key}\n')
        cipher = encryptRailFence(text, key)
        print(cipher)
    else:
        print(f'Decrypting {text} with key {key}\n')
        plaintext = decryptRailFence(text, key)
        print(plaintext)

if __name__ == '__main__':
    main()