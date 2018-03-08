import wave
import struct
import random   

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

def write_wav(filename, hex_channel):
    inp = wave.open('male.wav')
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



if __name__ == '__main__':
    message =  [str(random.randint(0,2)) for x in range(100000)] 
    # message = "1001011111111111111111111111111111111111111111111111111111111111111111111111111111110000000000000000000000000000000000000000000000000001000000000000000000"
    # message = '0000111100001111'
    input_file = 'male.wav'
    channels, sample_rate, hex_channel, raw_data,total_samples, params = pcm_channels(input_file)
    print channels[0][0:10]
    for i in range(len(message)):
        if message[i] == '1':
            channels[0][i] |= 1
        else:
            channels[0][i] &= ~1
    

    hex_channel = struct.pack('<%ih' % (total_samples/params[0]), *channels[0])
    write_wav('test.wav', hex_channel)