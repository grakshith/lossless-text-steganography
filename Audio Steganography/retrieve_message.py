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
    hex_channel = struct.pack('<%ih' % (total_samples), *channels[0])
    # print hex_channel[0:10]
    # print channels[0]
    # print channels[0][0:10],'\n',hex_channel[0:10]
    return channels, sample_rate, hex_channel, raw_data, total_samples


def retrieve_message(message_length, channels):
    message = ''
    for i in range(message_length):
        if channels[0][i] % 2 == 0:
            message+='0'
        else:
            message+='1'

    return message



if __name__ == '__main__':
    
    filename = 'test.wav'
    channels, sample_rate, hex_channel, raw_data, total_samples = pcm_channels(filename)
    message_length = 100000
    retrieve_message(message_length, channels)

