import io
import random
import cPickle as pickle
import RSA

def de_embed(filename, seed, length, null_chars):
    with io.open(filename, 'r', encoding='utf-8') as file:
    # with open(filename) as file:
        i=0
        message_dict = {}
        empty_chars = []
        
        for line in file:
            for char in line:
                
                # if char == u'\u2008':
                if char == null_chars[1]:
                    message_dict[i] = 1 
                    empty_chars.append(i)
                if char == null_chars[0]:
                    message_dict[i] = 0
                    empty_chars.append(i)
                    
                i+=1    
    
    random.seed(seed)
    random.shuffle(empty_chars)
    decoded_message = ''
    for i in range(0, length):
        decoded_message += str(message_dict[empty_chars[i]])

    return decoded_message


def decode(message, d_codewords):
        i=0
        j=0
        decoded = []
        while i < len(message):
            if d_codewords.get(message[i:i+j]):
                decoded.append(d_codewords.get(message[i:i+j]))
                i=i+j
                j=0
            else:
                j = j+1
        message = decoded
        return message

if __name__ == '__main__':
    with open('received/keys','rb') as fp:
        d_codewords = pickle.load(fp)
        message_length = pickle.load(fp)
        seed = pickle.load(fp)
        null_chars = pickle.load(fp)
    filename = raw_input("Enter the stego file name\n")
    bin_message = de_embed(filename, seed, message_length ,null_chars)
    print "The retrieved binary message from file is : {}".format(bin_message)
    decoded =  decode(bin_message, d_codewords)
    print "The message after Huffman Decoding is : {}".format(decoded)
    with open('received/RSA_Keys','rb') as fp:
        key = pickle.load(fp)
       
    
    print 'The RSA decrypted message is : '+''.join(map(chr,RSA.decrypt(key[1], decoded)))
