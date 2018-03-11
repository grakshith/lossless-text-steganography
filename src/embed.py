import sys
import random
import struct
import io
from fpdf import FPDF
import cPickle as pickle


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
    seed = random.randint(0, 100)
    random.seed(seed)
    random.shuffle(indices)
    with open('keys','a+b') as fp:
        pickle.dump(seed,fp)
    return indices

def embed(indices, message, file_string):
    indices = indices[:len(message)]
    message = list(message)
    file_string = list(file_string)
    null_chars = [' ', u'\u2008']
    with open('keys','a+b') as fp:
        pickle.dump(null_chars,fp)
    with io.open('embedded/stego.txt', 'w', encoding='utf-8') as file:
        for index,m in zip(indices,message):
            print index
            print m
            if(m=="1"):
                file_string[index] = u'\u2008'.encode('utf-8')
            
            
        # file.write(''.join(file_string).encode('ascii'))
        # file_string = ''.join(file_string)
        print file_string
        s=u''
        for x in file_string:
            # print type(x.decode('utf-8'))
            file.write(x.decode('utf-8'))
            s += x.decode('ISO-8859-1')
    
    
def embed_in_text_file(filename, message):
    indices, file_string = get_spaces(filename)
    if len(indices)<len(message):
        print "Number of empty characters in the cover text is very small"
        exit(0)
    random_indices = randomize_indices(indices)
    embed(random_indices, message, file_string)



def de_embed(filename, seed, length):
    with io.open(filename, 'r', encoding='utf-8') as file:
    # with open(filename) as file:
        i=0
        message_dict = {}
        empty_chars = []
        
        for line in file:
            for char in line:
                
                if char == u'\u2008':
                    message_dict[i] = 1 
                    empty_chars.append(i)
                if char == ' ':
                    message_dict[i] = 0
                    empty_chars.append(i)
                    
                i+=1    
    
    random.seed(seed)
    random.shuffle(empty_chars)
    decoded_message = ''
    for i in range(0, length):
        decoded_message += str(message_dict[empty_chars[i]])

    print decoded_message 
    return decoded_message

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
    de_embed('embedded/stego.txt', 60 ,len(message))
