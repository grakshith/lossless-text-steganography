import wave
import struct
import random   
import math

SHIFT = 32768
EMBEDDING_ERRORS = []
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
    params = stream.getparams()
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
    # hex_channel = ([hex(channels[0][i] & (2**16-1)) for i in range(num_frames)])
    hex_channel = struct.pack('<%ih' % (total_samples/num_channels), *channels[0])
    # print hex_channel[0:10]
    # print channels[0]
    # print channels[0][0:10],'\n',hex_channel[0:10]
    return channels, sample_rate, hex_channel, raw_data, total_samples,params

# pcm_channels('AudioSteganography/opera.wav')
# pcm_channels('0063.wav')

def write_wav(filename, hex_channel, input_file):
    inp = wave.open(input_file)
    params = inp.getparams()
    inp.close()
    stream = wave.open(filename,"wb")
    stream.setparams(params)

    # a, b, c,d = pcm_channels('0063.wav')

    # print len(c), len(d)
    # print type(c)
    # print d[0:10]
    stream.writeframes(hex_channel)
    stream.close()

# write_wav('test.wav')


def set_bit(value, bit):
    return value | (1<<bit)

def clear_bit(value, bit):
    return value & ~(1<<bit)


def embed_LSB(channel, message, depth):
    channel = [i+SHIFT for i in channel]
    ctr=0
    for i in range(len(message)):
        print channel[i]
        if message[i] == '1' and not (channel[i] & (1 << depth-1)):
            EMBEDDING_ERRORS.append(1)
            print "Setting bit to 1"
            ctr+=1
            channel[i] = set_bit(channel[i], depth-1)

            if channel[i] & (1 << depth-2):
                for d in range(0, depth-1):
                    channel[i] = clear_bit(channel[i], d)
            else :
                for d in range(0, depth-1): #0, 1, 2 (last 3 bits)
                    channel[i] = set_bit(channel[i], d)
                for d in range(depth, 16): # 4, 5, ....15 
                    if channel[i] & (1 << d):
                        channel[i] = clear_bit(channel[i], d)
                        break
                    else:
                        channel[i] = set_bit(channel[i], d)


        elif message[i] == '0' and (channel[i] & (1 << depth-1)):
            print "Setting bit to 0"
            EMBEDDING_ERRORS.append(-1)
            ctr+=1
            channel[i] = clear_bit(channel[i], depth-1)
            if not (channel[i] & (1 << depth-2)):
                for d in range(0, depth-1):
                    channel[i] = set_bit(channel[i], d)
            else:
                for d in range(0, depth-1): #0, 1, 2 (last 3 bits)
                    channel[i] = clear_bit(channel[i], d)
                for d in range(depth, 16): # 4, 5, ....15 
                    if not (channel[i] & (1 << d)):
                        channel[i] = set_bit(channel[i], d)
                        break
                    else:
                        channel[i] = clear_bit(channel[i], d)
        else:
            EMBEDDING_ERRORS.append(0)
        # Embedding error correction
        # print len(EMBEDDING_ERRORS), i
        # if len(EMBEDDING_ERRORS) != 0:
        #     for j in range(1, depth):
        #         # print i+j
        #         channel[i+j] += int(math.floor(EMBEDDING_ERRORS[i]/j))
        #         # print channel[i+1]
    channel = [i-SHIFT for i in channel]
    print "Changed {} bits".format(ctr)
    return channel

# print embed_LSB([-9], "1", 4)


if __name__ == '__main__':
    # message =  [str(random.randint(0,2)) for x in range(200000)] 
    # message = "1001011111111111111111111111111111111111111111111111111111111111111111111111111111110000000000000000000000000000000000000000000000000001000000000000000000"
    message = '0000111100001111'
    input_file = 'male.wav'
    channels, sample_rate, hex_channel, raw_data,total_samples, params = pcm_channels(input_file)
    # print channels[0][0:10]
    new_channel = embed_LSB(channels[0], message, 4)
    # print new_channel[0:100]
    channels, sample_rate, hex_channel, raw_data,total_samples, params = pcm_channels(input_file)
    # for i, j in zip(channels[0][0:100], new_channel[0:100]):
    #     print i, j
    # for i in range(len(message)):
    #     if message[i] == '1':
    #         channels[0][i] |= 1
    #     else:
    #         channels[0][i] &= ~1
    # embed_LSB(channels[0], message)

    hex_channel = struct.pack('<%ih' % (total_samples/params[0]), *new_channel)
    write_wav('test.wav', hex_channel, input_file)