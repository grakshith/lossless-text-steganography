import wave
import struct
import random   
import math
import cPickle as pickle
SHIFT = 32768
EMBEDDING_ERRORS = []
E_N_VALS = [5]
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
    hex_channel = struct.pack('<%ih' % (total_samples/num_channels), *channels[0])
    return channels, sample_rate, hex_channel, raw_data, total_samples,params

def write_wav(filename, hex_channel, input_file):
    inp = wave.open(input_file)
    params = inp.getparams()
    inp.close()
    stream = wave.open(filename,"wb")
    stream.setparams(params)
    stream.writeframes(hex_channel)
    stream.close()

def set_bit(value, bit):
    return value | (1<<bit)

def clear_bit(value, bit):
    return value & ~(1<<bit)

def embed_LSB(channel, message, depth, E_N):
    channel = [i+SHIFT for i in channel]
    i=0
    spread_factor = len(channel)/len(message)
    with open('pickled/keys','a+b') as fp:
            pickle.dump(spread_factor,fp)
    indices = [i for i in range(1, len(channel), spread_factor) ]
    
    ctr=0
    for i, index in zip(range(len(message)), indices[0:len(message)]):
        if message[i] == '1' and not (channel[index] & (1 << depth-1)):
            old_channel = channel[index]
            EMBEDDING_ERRORS.append(E_N)
            ctr+=1
            channel[index] = set_bit(channel[index], depth-1)

            if channel[index] & (1 << depth-2):
                for d in range(0, depth-1):
                    channel[index] = clear_bit(channel[index], d)
            else :
                for d in range(0, depth-1): #0, 1, 2 (last 3 bits)
                    channel[index] = set_bit(channel[index], d)
                for d in range(depth, 16): # 4, 5, ....15 
                    if channel[index] & (1 << d):
                        channel[index] = clear_bit(channel[index], d)
                        break
                    else:
                        channel[index] = set_bit(channel[index], d)
            print "Changing {0} ({0:016b}) to {1} ({1:016b})".format(old_channel,channel[index])


        elif message[i] == '0' and (channel[index] & (1 << depth-1)):
            old_channel = channel[index]
            EMBEDDING_ERRORS.append(-E_N)
            ctr+=1
            channel[index] = clear_bit(channel[index], depth-1)
            if not (channel[index] & (1 << depth-2)):
                for d in range(0, depth-1):
                    channel[index] = set_bit(channel[index], d)
            else:
                for d in range(0, depth-1): #0, 1, 2 (last 3 bits)
                    channel[index] = clear_bit(channel[index], d)
                for d in range(depth, 16): # 4, 5, ....15 
                    if not (channel[index] & (1 << d)):
                        channel[index] = set_bit(channel[index], d)
                        break
                    else:
                        channel[index] = clear_bit(channel[index], d)
            print "Changing {0} ({0:016b}) to {1} ({1:016b})".format(old_channel,channel[index])
        else:
            EMBEDDING_ERRORS.append(0)
        if len(EMBEDDING_ERRORS) != 0:
            for j in range(1, depth):
                channel[index+j] += int(math.floor(EMBEDDING_ERRORS[i]/j))
    channel = [i-SHIFT for i in channel]
    print "Changed {} bits".format(ctr)
    return channel


def embed_to_file(input_file, message, E_N=5):
    channels, sample_rate, hex_channel, raw_data,total_samples, params = pcm_channels(input_file)
    new_channel = embed_LSB(channels[0], message, 10, E_N)
    hex_channel = struct.pack('<%ih' % (total_samples/params[0]), *new_channel)
    filename = input_file.replace('/', ' ').replace('.', ' ').split()[-2]
    write_wav('stego_audio/{}.wav'.format(filename), hex_channel, input_file)

    
if __name__ == '__main__':
    input_file = 'cover_audio/violin2.wav'
    channels, sample_rate, hex_channel, raw_data,total_samples, params = pcm_channels(input_file)
    for E_N in E_N_VALS:
        new_channel = embed_LSB(channels[0], message, 10, E_N)
        channels, sample_rate, hex_channel, raw_data,total_samples, params = pcm_channels(input_file)

        hex_channel = struct.pack('<%ih' % (total_samples/params[0]), *new_channel)

        write_wav('test_{}.wav'.format(E_N), hex_channel, input_file)
        EMBEDDING_ERRORS = []
