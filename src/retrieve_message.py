import wave
import struct
import random   
import cPickle as pickle
import RSA

def pcm_channels(wave_file):
    """Given a file-like object or file path representing a wave file,
    decompose it into its constituent PCM data streams.

    Input: A file like object or file path
    Output: A list of lists of integers representing the PCM coded data stream channels
        and the sample rate of the channels (mixed rate channels not supported)
    """
    stream = wave.open(wave_file,"rb")

    num_channels = stream.getnchannels()
    sample_rate = stream.getframerate()
    sample_width = stream.getsampwidth()
    num_frames = stream.getnframes()

    raw_data = stream.readframes( num_frames ) # Returns byte data

    stream.close()

    total_samples = num_frames * num_channels

    if sample_width == 1: 
        fmt = "%iB" % total_samples # read unsigned chars
    elif sample_width == 2:
        fmt = "%ih" % total_samples # read signed 2 byte shorts
    else:
        raise ValueError("Only supports 8 and 16 bit audio formats.")

    integer_data = struct.unpack(fmt, raw_data)
    # del raw_data # Keep memory tidy (who knows how big it might be)

    channels = [ [] for time in range(num_channels) ]

    for index, value in enumerate(integer_data):
        bucket = index % num_channels
        channels[bucket].append(value)
    hex_channel = struct.pack('<%ih' % (total_samples), *channels[0])
    return channels, sample_rate, hex_channel, raw_data, total_samples


def retrieve_message(message_length, channels, depth, spread_factor):
    message = ''
    indices = [i for i in range(1, len(channels[0]), spread_factor) ]
    for i in indices[0:message_length]:
        if channels[0][i] & (1 << depth-1):
            message+='1'
        else:
            message+='0'

    return message


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
    
    filename = raw_input("Enter the stego file name:")
    channels, sample_rate, hex_channel, raw_data, total_samples = pcm_channels(filename)

    with open('pickled/keys','rb') as fp:
        d_codewords = pickle.load(fp)
        message_length = pickle.load(fp)
        spread_factor = pickle.load(fp)
    message = retrieve_message(message_length, channels, 10, spread_factor)
    print "Message in binary - {}".format(message)
    decoded = decode(message, d_codewords)
    print "Huffman decoded message - {}".format(decoded)
    with open('pickled/RSA_Keys','rb') as fp:
        key = pickle.load(fp)

    print "After decrypting with RSA"   
    print "Message - {}".format(''.join(map(chr,RSA.decrypt(key[1], decoded))))

