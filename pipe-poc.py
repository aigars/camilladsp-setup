import alsaaudio
import struct

card = "input_card2"
device = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, card)
device.setchannels(2)
device.setrate(48000)
device.setformat(alsaaudio.PCM_FORMAT_S16_LE)
device.setperiodsize(1024)

out_card = "output_card2"
out_device = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, alsaaudio.PCM_NORMAL, out_card)
out_device.setchannels(2)
out_device.setrate(48000)
out_device.setformat(alsaaudio.PCM_FORMAT_S16_LE)
out_device.setperiodsize(1024)

while True:
    length, buf = device.read()
    samples = len(buf) / 2  # each sample is a short (16-bit)
    values = struct.unpack('<%dh' % samples, buf)
    print(out_device.write(buf))
    