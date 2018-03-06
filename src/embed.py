import sys
import random
import struct
import io
from fpdf import FPDF

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
    with io.open('embedded/stego.txt', 'w', encoding='utf-8') as file:
        for index in indices:
            if(message[0]=="1"):
                file_string[index] = u'\u2063'.encode('utf-8')
        # file.write(''.join(file_string).encode('ascii'))
        # file_string = ''.join(file_string)
        s=u''
        for x in file_string:
            # print type(x.decode('utf-8'))
            file.write(x.decode('utf-8'))
            s += x.decode('ISO-8859-1')
    pdf = FPDF()
    pdf.add_page()
    pdf.set_xy(0, 0)
    pdf.set_font('arial', 'B', 13.0)
    pdf.multi_cell(h=5.0, align='L', w=0, txt=s, border=0)
    pdf.output('embedded/pdf.pdf', 'F')

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

