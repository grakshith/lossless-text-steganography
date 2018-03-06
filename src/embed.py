import sys
import random
import struct

def get_spaces(filename):
    i = 0
    indices = []
    file_string = None
    with open(filename) as file:
        file_string = file.read()
        file.seek(0)
        for line in file:
            for char in line:
                if(char == ' '):
                    indices.append(i)
                i += 1
    return indices, file_string


def randomize_indices(indices):
    random.seed(60)
    random.shuffle(indices)
    return indices

def embed(indices, message, file_string):
    indices = indices[:len(message)]
    message = list(message)
    file_string = list(file_string)
    with open('embedded/stego.txt', 'w') as file:
        for index in indices:
            if(message[0]=="1"):
                file_string[index] = struct.pack('B', 0)
        print ''.join(file_string)
        # file.write(''.join(file_string).encode('ascii'))
        file_string = ''.join(file_string)
        file.write(file_string)

if __name__ == '__main__':
    if(len(sys.argv)) < 2:
        print "One argument is required"
        exit(0)
    message = "1010111101110001010000"
    indices, file_string = get_spaces(str(sys.argv[1:2][0]))
    if len(indices)<len(message):
        print "Number of empty characters in the cover text is very small"
        exit(0)
    random_indices = randomize_indices(indices)
    embed(random_indices, message, file_string)

