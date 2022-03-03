import alsaaudio
import struct
import os

card = "input_card2"
device = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, card)
device.setchannels(2)
device.setrate(44100)
device.setformat(alsaaudio.PCM_FORMAT_S16_LE)
device.setperiodsize(1024)

# out_card = "output_card2"
# out_device = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, alsaaudio.PCM_NORMAL, out_card)
# out_device.setchannels(2)
# out_device.setrate(48000)
# out_device.setformat(alsaaudio.PCM_FORMAT_S16_LE)
# out_device.setperiodsize(1024)

path = "./audio"
os.mkfifo(path, 0o600)
fifo = open(path, 'wb')

while True:
    length, buf = device.read()
    samples = len(buf) / 2  # each sample is a short (16-bit)
    values = struct.unpack('<%dh' % samples, buf)
    fifo.write(buf)
    